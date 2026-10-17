#!/usr/bin/env python3
"""Repository-native legal review workbench. AI prepares materials; humans sign decisions."""

import argparse
import base64
from copy import deepcopy
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from uuid import uuid4
from urllib.parse import quote

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CASES = 'data/reviews/cases'
TRIGGERS = ('initial-intake', 'source-update', 'regulatory-change', 'license-change',
            'scope-change', 'risk-reassessment', 'scheduled-review')
ROLES = {'professional_review': 'Legal Reviewer', 'rights_review': 'Rights Reviewer',
         'engineering_review': 'Engineering Reviewer', 'admission_decision': 'Human Maintainer'}
DECISIONS = {'professional_review': ('approved-scope', 'needs-changes', 'rejected'),
             'rights_review': ('approved-scope', 'needs-changes', 'rejected'),
             'engineering_review': ('passed', 'needs-changes', 'rejected'),
             'admission_decision': ('admitted', 'declined', 'suspended')}
GATES = {'curated-hosting': ('authorization-chain', 'hosting-scope', 'attribution-and-notices'),
         'original-development': ('independent-requirements', 'original-design', 'provenance-and-dependencies', 'synthetic-tests'),
         'external-reference': ('index-description', 'no-fulltext-copy', 'metadata-and-dedup')}
ENGINEERING_GATES = ('metadata-schema', 'dedup', 'engineering-checks')
CHECK_FIELDS = ('source_locator', 'legal_issue', 'fact_context', 'authority_refs',
                'legal_effective_period', 'transitional_rule', 'applicability_reasoning',
                'finding', 'risk_level', 'required_changes', 'limitations', 'evidence_refs', 'check_status')
SIGN_FIELDS = ('credential_evidence_ref', 'conflict_declaration', 'regulatory_as_of')
ID = re.compile(r'^RV-[A-Za-z0-9-]+$')
EVENT_URL = re.compile(r'^https://github.com/fitalex/LexRouter/pull/([1-9][0-9]*)#pullrequestreview-([1-9][0-9]*)$')


class ReviewError(ValueError):
    """Diagnostics contain fixed explanations, never untrusted field values."""


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def byte_digest(value):
    return hashlib.sha256(value).hexdigest()


def public_guard(value):
    """Limited accidental-disclosure tripwire, not privacy or rights certification."""
    content = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    patterns = (r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY', r'AKIA[A-Z0-9]{16}',
                r'(?<![A-Za-z0-9])\d{17}[0-9Xx](?![A-Za-z0-9])',
                r'(?i)\b(?:secret|token|password)\s*[=:]\s*[^\s,;]+',
                r'(?i)(?:file://|/home/|/Users/|[A-Z]:\\)', r'(?i)PRIVATE_MATERIAL')
    if any(re.search(p, content) for p in patterns):
        raise ReviewError('Public-material safety check failed; inspect locally. Input was not logged.')


def reference(value):
    if re.fullmatch(r'controlled://[A-Za-z0-9_./-]+', value):
        return
    if not re.fullmatch(r'https://[^\s?@]+', value):
        raise ReviewError('Evidence needs a public HTTPS locator without credentials/query, or opaque controlled:// index.')


def safe(root, rel):
    root, p = Path(root).resolve(), Path(rel)
    if p.is_absolute() or not p.parts or '..' in p.parts or '\\' in str(rel):
        raise ReviewError('Expected an explicit repository-relative path.')
    target = root / p
    if not target.resolve().is_relative_to(root) or any(x.is_symlink() for x in [target, *target.parents]):
        raise ReviewError('Symlinks and paths outside repository are forbidden.')
    return target


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ReviewError('Duplicate JSON keys are forbidden; input was not logged.')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def write(path, value):
    path = Path(path)
    data = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)+'\n'
    public_guard(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name+'.tmp')
    temp.write_text(data, encoding='utf-8')
    temp.replace(path)


def case_dir(root, rid):
    if not ID.fullmatch(rid):
        raise ReviewError('Invalid Review ID.')
    return safe(root, f'{CASES}/{rid}')


def load_case(root, rid):
    return read(case_dir(root, rid) / 'record.json')


def all_records(root):
    return [read(safe(root, str(p.relative_to(root))))
            for p in sorted(safe(root, CASES).glob('*/record.json'))]


def templates(root, refs):
    selected, ids, versions = {}, {}, []
    for ref in refs:
        t = read(safe(root, ref))
        versions.append({'template_id': t['template_id'], 'version': t['version'], 'sha256': fingerprint(t)})
        for c in t['checks']:
            key, cid = c['issue_key'], c['check_id']
            if cid in ids and ids[cid] != key:
                raise ReviewError('Conflicting check IDs across templates.')
            ids[cid] = key
            if key in selected and selected[key] != c:
                raise ReviewError('Conflicting definitions for one legal issue; resolve template conflict.')
            selected[key] = c
    checks = list(selected.values())
    if not {f'C{i:02}' for i in range(1, 11)} <= {c['check_id'] for c in checks}:
        raise ReviewError('All P0-05 common checks C01–C10 are required.')
    return checks, versions


def core(record):
    return {k: v for k, v in record.items() if k not in ('history', 'archived', 'archive_sha256')}


def binding(record, workbook):
    return fingerprint({'record': core(record), 'workbook_sha256': byte_digest(workbook.encode())})


def history(record, old, source, reason, snapshot=None):
    record['history'].append({'at': now(), 'source': source, 'reason': reason,
                              'from': old, 'to': record['status'],
                              'snapshot_ref': snapshot[0] if snapshot else None,
                              'snapshot_sha256': snapshot[1] if snapshot else None})


def structural_errors(root, record):
    schema = read(safe(root, 'schemas/review-record.schema.json'))
    return ['Record contract error at /'+'/'.join(map(str, e.absolute_path)) for e in
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record)]


def source_file_url(subject, path):
    pattern = subject.get('source_file_url_template')
    if pattern is None:
        match = re.match(r'https://github.com/([^/]+/[^/]+)/(?:blob|tree)/', subject['source_url'])
        if not match:
            raise ReviewError('Non-GitHub sources require source_file_url_template with {revision} and {path}.')
        pattern = 'https://github.com/'+match.group(1)+'/blob/{revision}/{path}'
    if '{revision}' not in pattern or '{path}' not in pattern:
        raise ReviewError('Fixed source links must include revision and explicit file path.')
    try:
        result = pattern.format(revision=subject['source_revision'], path=quote(path, safe='/'))
    except (KeyError, ValueError):
        raise ReviewError('Invalid source file URL template.') from None
    reference(result)
    return result


def init_review(root, subject_ref, trigger='initial-intake', parent=None, rid=None):
    subject = read(safe(root, subject_ref))
    required = ('subject_id', 'subject_type', 'source_url', 'source_revision', 'scope_manifest_ref',
                'templates', 'jurisdiction', 'track', 'review_scope', 'excluded_scope', 'public_summary_only')
    if not all(k in subject for k in required) or subject['public_summary_only'] is not True:
        raise ReviewError('Incomplete public subject descriptor; see documented subject contract.')
    reference(subject['source_url'])
    if not re.fullmatch('[a-f0-9]{40}', subject['source_revision']) or trigger not in TRIGGERS:
        raise ReviewError('A full fixed Git commit and recognized trigger are required.')
    prior = [r for r in all_records(root) if r['subject_id'] == subject['subject_id']]
    if (prior or trigger != 'initial-intake') and not parent:
        raise ReviewError('Existing subjects and update reviews require an explicit parent; never inherit approval.')
    if parent:
        p = load_case(root, parent)
        if p['subject_id'] != subject['subject_id']:
            raise ReviewError('Parent must refer to the same subject.')
        effective = {r['review_id'] for r in prior if r['status'] == 'approved-scope'}
        if effective and parent not in effective:
            raise ReviewError('Link to a prior effective scope approval when one exists.')
    checks, versions = templates(root, subject['templates'])
    manifest = read(safe(root, subject['scope_manifest_ref']))
    if manifest.get('revision') != subject['source_revision']:
        raise ReviewError('Inventory/source revision mismatch.')
    paths = []
    for f in manifest['files']:
        safe(root, f['path'])
        if not re.fullmatch('[a-f0-9]{40}', f['blob_sha']):
            raise ReviewError('Inventory requires full fixed file blob hashes.')
        paths.append(f['path'])
    allowed = {f['path'] for f in manifest['files'] if f['decision'] == 'eligible-for-scope-review'}
    selected = subject['review_scope']
    if len(paths) != len(set(paths)) or not selected or len(selected) != len(set(selected)) or not set(selected) <= allowed:
        raise ReviewError('Scope must explicitly select unique eligible inventory files; excluded files cannot be inherited.')
    rid = rid or 'RV-'+datetime.now(timezone.utc).strftime('%Y%m%d')+'-'+uuid4().hex[:12]
    d = case_dir(root, rid)
    if d.exists():
        raise ReviewError('Review ID already exists; no files were overwritten.')
    blank = []
    for c in checks:
        item = {k: '' for k in CHECK_FIELDS}
        item.update(check_id=c['check_id'], source_locator=c['source_locator'], legal_issue=c['legal_issue'],
                    authority_refs=[], evidence_refs=[], risk_level='unassessed', check_status='pending')
        blank.append(item)
    r = {k: subject[k] for k in ('subject_id', 'subject_type', 'source_revision', 'scope_manifest_ref', 'track', 'review_scope', 'excluded_scope')}
    r.update(format_version=1, review_id=rid, source_snapshot_sha256=fingerprint(subject),
             scope_manifest_sha256=fingerprint(manifest), trigger_type=trigger, parent_review_id=parent,
             template_version=versions, jurisdiction={'value': subject['jurisdiction'], 'status': 'proposed'},
             created_at=now(), assigned_reviewer=None, status='draft', next_review_date=None,
             risk_level='unassessed', checks=blank, history=[], archived=False, archive_sha256=None, suspension=None)
    for axis in ROLES:
        r[axis] = {'status': 'not-admitted' if axis == 'admission_decision' else 'pending', 'signature': None, 'gate_evidence': {}}
    history(r, 'none', 'cli:init', 'Create unsigned review with no inherited findings.')
    if structural_errors(root, r):
        raise ReviewError('Subject does not satisfy the review contract.')
    for path in selected:
        source_file_url(subject, path)
    for value in (subject, manifest, checks, r):
        public_guard(value)
    for name, value in [('subject.json', subject), ('inventory.json', manifest), ('templates.json', checks), ('record.json', r)]:
        write(d / name, value)
    prepare(root, rid)
    return rid


def new_workbook(r):
    lines = ['# 人工专业意见与独立决定工作表', '',
             '只填写允许公开的摘要和证据索引。普通文本不是签名；本人须在 GitHub Review 中签署绑定摘要。',
             '保留标题和字段名，填写冒号后内容，可换行续写；多项引用以英文分号分隔。',
             'check_status: pending / pass / needs-changes / fail / not-applicable。risk_level: unassessed / low / medium / high / critical。',
             '', '## signature', '- credential_evidence_ref: ', '- conflict_declaration: ', '- regulatory_as_of: ',
             '', '## maintenance', '- next_review_date: ', '- risk_level: unassessed', '']
    for c in r['checks']:
        lines += ['## '+c['check_id'], '']
        for key in CHECK_FIELDS:
            val = '; '.join(c[key]) if isinstance(c[key], list) else c[key]
            lines.append(f'- {key}: {val}')
        lines.append('')
    for axis in ('rights_review', 'engineering_review', 'admission_decision'):
        keys = GATES[r['track']] if axis == 'rights_review' else ENGINEERING_GATES if axis == 'engineering_review' else ('scope-and-purpose',)
        lines += ['## '+axis, '']+[f'- {k}: ' for k in keys]+['']
    return '\n'.join(lines+['## suspension', '- affected_scope: ', '- reason: ', ''])


def prepare(root, rid):
    d = case_dir(root, rid)
    r, subject, inventory, rules = [read(d / name) for name in ('record.json', 'subject.json', 'inventory.json', 'templates.json')]
    if r['archived']:
        raise ReviewError('Archived reviews are read-only; create a child review.')
    files = [f for f in inventory['files'] if f['path'] in r['review_scope']]
    matrix = ['# 问题矩阵（自动材料，不是法律意见）', '', '| 检查项 | 必须核实的问题 | 来源位置 | 官方法规/证据线索（未核实） |', '| --- | --- | --- | --- |']
    matrix += ['| '+' | '.join(str(c[k]).replace('|', '／').replace('\n', ' ') for k in ('check_id', 'legal_issue', 'source_locator', 'authority_hints'))+' |' for c in rules]
    evidence = ['# 固定证据索引', '', '通过原站固定链接只读审阅；不收录第三方全文，不运行上游代码。', '',
                f'- 固定 commit：`{r["source_revision"]}`',
                f'- 完整材料清单：[{r["scope_manifest_ref"]}](../../../../{r["scope_manifest_ref"]})',
                f'- 清单规范化 SHA-256：`{r["scope_manifest_sha256"]}`', '', '| 拟审核文件 | Git blob SHA-1 |', '| --- | --- |']
    evidence += [f'| [{f["path"]}]({source_file_url(subject, f["path"])}) | `{f["blob_sha"]}` |' for f in files]
    evidence += ['', f'未纳入/排除：{len(inventory["files"])-len(files)} 项。不得自动扩大范围。']
    packet = ['# '+rid+'｜法律 Skill 专业复核工作包', '', f'- 对象：{r["subject_id"]}（{r["subject_type"]}）',
              f'- 轨道提案：{r["track"]}', f'- 固定版本：`{r["source_revision"]}`',
              f'- 触发：{r["trigger_type"]}；前次记录：{r["parent_review_id"] or "无"}',
              f'- 拟核法域：{r["jurisdiction"]["value"]}，待专业确认',
              f'- 拟核文件：{len(files)}；排除边界：'+ '；'.join(r['excluded_scope']), '',
              '## 审核材料和人工填写', '', '- [来源固定链接与范围](evidence.md)', '- [通用/专项问题矩阵](matrix.md)',
              '- [人工专业意见区](workbook.md)', '- [结构化记录和状态](record.json)',
              '- [维护者操作指南](../../../../docs/review-workbench/MAINTAINER.md)', '', '## 已发现疑点和原始依据', '']
    packet += ['- [既有证据 '+ref+'](../../../../'+ref+')' for ref in subject.get('baseline_refs', [])]
    packet += ['- '+v for v in subject.get('known_issues', [])]
    packet += ['', '## 尚未完成事项', '', '创建时所有 C01–C10 和专项项均待人工核查，资质、利益冲突、法规时效及签署均未确认；实际后续进度见 record.json 和 status。',
               '授权链、依赖、范围/用途待独立审核；八字段元数据、去重和工程检查待执行。当前未专业复核、未获授权批准、未入库。',
               '', '## 最终决定和签署说明', '', '专业人员填写工作表后，由本人在 GitHub Review 中声明角色、决定、绑定摘要和依据。',
               '同一人可分别担任 Legal Reviewer 和 Human Maintainer，必须使用独立事件。Codex 只同步核验事件，不代签或自动批准。',
               '重大法律或授权风险须记录受影响范围、暂停决定并由维护者执行处置；历史证据不自动删除。', '']
    outputs = {'packet.md': '\n'.join(packet), 'matrix.md': '\n'.join(matrix)+'\n', 'evidence.md': '\n'.join(evidence)+'\n'}
    known = read(d / 'generated.json') if (d / 'generated.json').exists() else {}
    for name, content in outputs.items():
        p = safe(root, f'{CASES}/{rid}/{name}')
        if p.exists() and byte_digest(p.read_bytes()) != known.get(name):
            raise ReviewError('Generated material was edited: resolve conflict explicitly. Human content was preserved.')
        public_guard(content)
    workbook = safe(root, f'{CASES}/{rid}/workbook.md')
    if not workbook.exists():
        write(workbook, new_workbook(r))
    for name, content in outputs.items():
        write(d / name, content)
    write(d / 'generated.json', {k: byte_digest(v.encode()) for k, v in outputs.items()})
    if r['status'] == 'draft':
        r['status'] = 'evidence-ready'
        history(r, 'draft', 'cli:prepare', 'Prepare pointers and blank human forms, not legal findings.')
        write(d / 'record.json', r)


def parse_workbook(content):
    public_guard(content)
    sections, section, field = {}, None, None
    for line in content.splitlines():
        if line.startswith('## '):
            section = line[3:].strip()
            if section in sections:
                raise ReviewError('Duplicate workbook section.')
            sections[section], field = {}, None
        elif line.startswith('- ') and section:
            pair = line[2:].split(':', 1)
            if len(pair) != 2 or pair[0] in sections[section]:
                raise ReviewError('Malformed or duplicate workbook field.')
            field, value = pair
            sections[section][field] = value.strip()
        elif line.strip() and section and field:
            sections[section][field] += '\n'+line.strip()
    return sections


def split_refs(value):
    return [x.strip() for x in value.split(';') if x.strip()]


def apply_professional(record, content, decision):
    sections = parse_workbook(content)
    expected = {'signature', 'maintenance', 'rights_review', 'engineering_review', 'admission_decision', 'suspension'} | {c['check_id'] for c in record['checks']}
    if set(sections) != expected:
        raise ReviewError('Missing or unexpected workbook sections.')
    checks = []
    for old in record['checks']:
        values = sections[old['check_id']]
        if set(values) != set(CHECK_FIELDS):
            raise ReviewError('Missing or unknown legal judgment fields.')
        item = {'check_id': old['check_id'], **values}
        for key in ('authority_refs', 'evidence_refs'):
            item[key] = split_refs(item[key])
            for value in item[key]:
                reference(value)
        checks.append(item)
    record['checks'] = checks
    if decision == 'approved-scope':
        for c in checks:
            if c['check_status'] not in ('pass', 'not-applicable') or c['required_changes'].strip():
                raise ReviewError('Unresolved, failed or incomplete checks block scope approval.')
            needed = ('source_locator', 'legal_issue', 'fact_context', 'finding', 'applicability_reasoning', 'limitations', 'legal_effective_period', 'transitional_rule')
            if any(not c[k].strip() for k in needed) or not c['evidence_refs'] or c['risk_level'] == 'unassessed':
                raise ReviewError('Each check needs actual facts, reasoning, time applicability, limitations and evidence.')
            if c['check_status'] == 'pass' and not c['authority_refs']:
                raise ReviewError('Passing checks require verified authority references; explain non-applicability separately.')
        record['jurisdiction']['status'] = 'professionally-confirmed'
    return sections


def github_api(path):
    try:
        proc = subprocess.run(['gh', 'api', path], capture_output=True, text=True, timeout=30, check=True)
        return json.loads(proc.stdout)
    except (OSError, subprocess.SubprocessError, ValueError):
        raise ReviewError('Authenticated GitHub evidence lookup failed; no approval was imported.') from None


def verify_event(url, expected_binding, rid, api=github_api):
    match = EVENT_URL.fullmatch(url)
    if not match:
        raise ReviewError('Use a canonical repository GitHub pull-request review event URL.')
    number, eid = match.groups()
    prefix = 'repos/fitalex/LexRouter'
    event = api(f'{prefix}/pulls/{number}/reviews/{eid}')
    pr = api(f'{prefix}/pulls/{number}')
    if event.get('id') != int(eid) or event.get('html_url') != url or event.get('state') not in ('COMMENTED', 'APPROVED', 'CHANGES_REQUESTED') or not event.get('submitted_at'):
        raise ReviewError('Review event is missing, pending, dismissed or mismatched.')
    user = event.get('user', {})
    if user.get('type') != 'User' or not user.get('login') or user['login'].endswith('[bot]'):
        raise ReviewError('Bot or unverified actor cannot sign a human decision.')
    if pr.get('base', {}).get('repo', {}).get('full_name') != 'fitalex/LexRouter' or pr.get('base', {}).get('ref') != 'main':
        raise ReviewError('Decision event must target repository main.')
    if event.get('commit_id') != pr.get('head', {}).get('sha'):
        raise ReviewError('Decision event is stale relative to the reviewed PR head.')
    base = pr['base']['sha']
    config = api(f'{prefix}/contents/data/reviews/reviewers.json?ref={base}')
    try:
        policy = json.loads(base64.b64decode(config['content']))
    except (KeyError, ValueError):
        raise ReviewError('Trusted base reviewer policy is unavailable.') from None
    fields = {}
    for line in event.get('body', '').splitlines():
        if ': ' in line:
            key, value = line.split(': ', 1)
            if key in fields:
                raise ReviewError('Duplicate signature payload field.')
            fields[key] = value.strip()
    axis, decision = fields.get('Role'), fields.get('Decision')
    if fields.get('LexRouter-Review') != rid or fields.get('Binding-SHA256') != expected_binding or fields.get('Policy-Base') != base or not fields.get('Reason'):
        raise ReviewError('Human event does not bind this exact review, opinion, policy and prior decisions.')
    if axis not in ROLES or decision not in DECISIONS[axis]:
        raise ReviewError('Unknown decision role or result.')
    if policy.get('repository') != 'fitalex/LexRouter' or ROLES[axis] not in policy.get('reviewers', {}).get(user['login'], []):
        raise ReviewError('Actor role is not authorized by policy on the trusted PR base.')
    permission = api(f'{prefix}/collaborators/{user["login"]}/permission')
    if permission.get('permission') not in ('admin', 'maintain', 'write'):
        raise ReviewError('Actor lacks repository decision permission.')
    return {'axis': axis, 'decision': decision, 'login': user['login'], 'submitted_at': event['submitted_at'],
            'reason': fields['Reason'], 'url': url, 'binding_sha256': expected_binding,
            'policy_base_sha': base, 'reviewed_commit_sha': event['commit_id']}


def verify_archived_event(ev, rid, api):
    match = EVENT_URL.fullmatch(ev['url'])
    if not match:
        raise ReviewError('Invalid signed event URL.')
    number, _ = match.groups()
    prefix = 'repos/fitalex/LexRouter'
    pr = api(f'{prefix}/pulls/{number}')
    ancestry = api(f'{prefix}/compare/{ev["policy_base_sha"]}...main')
    if ancestry.get('status') not in ('ahead', 'identical'):
        raise ReviewError('Historical reviewer policy was not accepted into main.')
    def historical(path):
        if path == f'{prefix}/pulls/{number}':
            adjusted = deepcopy(pr)
            adjusted['head']['sha'], adjusted['base']['sha'] = ev['reviewed_commit_sha'], ev['policy_base_sha']
            return adjusted
        return api(path)
    if verify_event(ev['url'], ev['binding_sha256'], rid, historical) != ev:
        raise ReviewError('Human event changed or its permission was revoked.')


def admission_ready(r):
    return (r['professional_review']['status'] == 'approved-scope'
            and r['rights_review']['status'] == 'approved-scope'
            and r['engineering_review']['status'] == 'passed' and not r['suspension'])


def apply_event(root, before, content, event):
    axis, decision, url = event['axis'], event['decision'], event['url']
    if axis not in ROLES or decision not in DECISIONS[axis]:
        raise ReviewError('Unknown signed role or decision.')
    if before['status'] in ('approved-scope', 'rejected') and axis == 'professional_review':
        raise ReviewError('Final professional opinions require a new child review.')
    if before['admission_decision']['status'] == 'admitted' and axis != 'admission_decision':
        raise ReviewError('Admitted scope requires a new update review; maintainer may independently suspend it.')
    r, sections = deepcopy(before), parse_workbook(content)
    if axis == 'professional_review':
        if before['status'] != 'in-review' or before['assigned_reviewer'] != event['login']:
            raise ReviewError('Start/re-submit and assign this human reviewer before professional judgment.')
        sections = apply_professional(r, content, decision)
        r['status'] = decision
    elif axis in ('rights_review', 'engineering_review'):
        keys = GATES[r['track']] if axis == 'rights_review' else ENGINEERING_GATES
        gates = sections.get(axis, {})
        if set(gates) != set(keys):
            raise ReviewError('Track-specific gate fields are missing or unknown.')
        if decision in ('approved-scope', 'passed'):
            for key in keys:
                if not gates[key].strip():
                    raise ReviewError('Required track-specific evidence is missing.')
                for value in split_refs(gates[key]):
                    reference(value)
        r[axis]['gate_evidence'] = gates
    else:
        if decision == 'admitted' and not admission_ready(r):
            raise ReviewError('Admission blocked: independent rights, professional and engineering gates must all pass.')
        gates = sections.get(axis, {})
        if set(gates) != {'scope-and-purpose'} or not gates['scope-and-purpose'].strip():
            raise ReviewError('Maintainer must independently document scope and purpose.')
        r[axis]['gate_evidence'] = gates
        if decision == 'suspended':
            values = sections.get('suspension', {})
            affected = split_refs(values.get('affected_scope', ''))
            if not affected or not set(affected) <= set(r['review_scope']) or not values.get('reason'):
                raise ReviewError('Suspension requires explicit affected scope and reason.')
            r['suspension'] = {'affected_scope': affected, 'reason': values['reason'], 'source': url, 'at': event['submitted_at']}
    sigfields = sections.get('signature', {})
    if set(sigfields) != set(SIGN_FIELDS) or not sigfields['credential_evidence_ref'] or not sigfields['conflict_declaration']:
        raise ReviewError('Signer must supply credential evidence index and conflict declaration.')
    reference(sigfields['credential_evidence_ref'])
    regulatory = sigfields['regulatory_as_of'] or None
    if regulatory and regulatory > event['submitted_at'][:10]:
        raise ReviewError('Regulatory as-of cannot be later than actual review.')
    if axis == 'professional_review' and decision == 'approved-scope' and not regulatory:
        raise ReviewError('Actual regulatory review date is required.')
    if axis == 'professional_review':
        maintenance = sections.get('maintenance', {})
        r['next_review_date'], r['risk_level'] = maintenance.get('next_review_date') or None, maintenance.get('risk_level', 'unassessed')
    sig = {**sigfields, 'regulatory_as_of': regulatory, 'reviewer_public_id': event['login'],
           'reviewer_role': ROLES[axis], 'reviewed_at': event['submitted_at'], 'decision': decision,
           'signature_evidence_ref': url, 'binding_sha256': event['binding_sha256'], 'reason': event['reason']}
    r[axis].update(status=decision, signature=sig)
    if structural_errors(root, r):
        raise ReviewError('Human form violates the record contract; no record was changed.')
    return r


def resumed_core(previous, current):
    result = deepcopy(previous)
    if result['status'] == 'needs-changes' and current['status'] == 'in-review':
        result['status'], result['assigned_reviewer'] = 'in-review', current['assigned_reviewer']
    return result


def validate_record(root, r, online=False, api=github_api):
    errors = structural_errors(root, r)
    if errors:
        return errors
    try:
        public_guard(r)
        d = case_dir(root, r['review_id'])
        subject, inventory, rules = [read(d / name) for name in ('subject.json', 'inventory.json', 'templates.json')]
        content = (d / 'workbook.md').read_text(encoding='utf-8')
        public_guard(content)
        if fingerprint(subject) != r['source_snapshot_sha256'] or fingerprint(inventory) != r['scope_manifest_sha256']:
            errors.append('Fixed source metadata or inventory digest changed.')
        if fingerprint(read(safe(root, r['scope_manifest_ref']))) != r['scope_manifest_sha256']:
            errors.append('Referenced inventory changed; create an update review.')
        for key in ('subject_id', 'subject_type', 'source_revision', 'scope_manifest_ref', 'track', 'review_scope', 'excluded_scope'):
            if subject[key] != r[key]:
                errors.append('Review scope differs from fixed descriptor.')
        if inventory['revision'] != r['source_revision']:
            errors.append('Source/inventory version mismatch.')
        allowed = {x['path'] for x in inventory['files'] if x['decision'] == 'eligible-for-scope-review'}
        if not set(r['review_scope']) <= allowed:
            errors.append('Scope includes excluded or unreviewed files.')
        actual, versions = templates(root, subject['templates'])
        if actual != rules or versions != r['template_version'] or {c['check_id'] for c in rules} != {c['check_id'] for c in r['checks']} or len(r['checks']) != len({c['check_id'] for c in r['checks']}):
            errors.append('Template versions or unique legal check coverage changed.')
        snapshots, previous = [], 'none'
        permitted = {('none', 'draft'), ('draft', 'evidence-ready'), ('evidence-ready', 'in-review'),
                     ('needs-changes', 'in-review'), ('in-review', 'approved-scope'),
                     ('in-review', 'needs-changes'), ('in-review', 'rejected')}
        for h in r['history']:
            if h['from'] != previous or (h['from'] != h['to'] and (h['from'], h['to']) not in permitted):
                errors.append('Invalid or discontinuous state history.')
            if h['from'] == 'in-review' and h['to'] in DECISIONS['professional_review'] and not h['snapshot_ref']:
                errors.append('Human professional transition needs signed evidence.')
            previous = h['to']
            if not h['snapshot_ref']:
                continue
            if not h['snapshot_ref'].startswith(f'{CASES}/{r["review_id"]}/history/'):
                raise ReviewError('History must remain within this review.')
            snap = read(safe(root, h['snapshot_ref']))
            if fingerprint(snap) != h['snapshot_sha256']:
                errors.append('Signed history snapshot changed.')
            ev = snap['event']
            if ev['binding_sha256'] != binding(snap['before'], snap['workbook']) or ev['url'] != h['source']:
                errors.append('Signature binding mismatch.')
            if snapshots:
                if resumed_core(snapshots[-1]['after'], snap['before']) != core(snap['before']):
                    errors.append('Signed decisions do not form a continuous chain.')
            elif any(snap['before'][axis]['signature'] or snap['before'][axis]['status'] not in ('pending', 'not-admitted') for axis in ROLES):
                errors.append('First signature inherits unproven decisions.')
            if core(apply_event(root, snap['before'], snap['workbook'], ev)) != snap['after']:
                errors.append('Signed decision does not replay to recorded result.')
            if online:
                verify_archived_event(ev, r['review_id'], api)
            snapshots.append(snap)
        listed = [h['snapshot_ref'] for h in r['history'] if h['snapshot_ref']]
        actual_history = {str(p.relative_to(root)) for p in (d / 'history').glob('*.json')}
        if len(listed) != len(set(listed)) or set(listed) != actual_history:
            errors.append('Orphan, missing or duplicate signed history file; inspect interrupted operation.')
        if previous != r['status']:
            errors.append('Current status is not last recorded transition.')
        if snapshots and resumed_core(snapshots[-1]['after'], r) != core(r):
            errors.append('Current record differs from last signed snapshot.')
        if r['professional_review']['status'] == 'approved-scope':
            check = deepcopy(r)
            apply_professional(check, content, 'approved-scope')
            if check['checks'] != r['checks']:
                errors.append('Approved legal judgments changed; create a new review.')
        for axis in ROLES:
            dim = r[axis]
            pending = 'not-admitted' if axis == 'admission_decision' else 'pending'
            if dim['status'] not in (pending, *DECISIONS[axis]):
                errors.append('Invalid independent dimension status.')
            evidence = [x for x in snapshots if x['event']['axis'] == axis]
            if dim['signature']:
                if not evidence or evidence[-1]['after'][axis] != dim or dim['signature']['decision'] != dim['status'] or dim['signature']['reviewer_role'] != ROLES[axis]:
                    errors.append('Decision lacks matching human snapshot and role.')
            elif dim['status'] != pending:
                errors.append('Unsigned decisions are forbidden.')
        if r['status'] in DECISIONS['professional_review'] and r['professional_review']['status'] != r['status']:
            errors.append('Professional lifecycle/dimension mismatch.')
        if r['professional_review']['status'] == 'pending' and (r['jurisdiction']['status'] != 'proposed' or any(c['check_status'] != 'pending' or c['finding'] or c['authority_refs'] for c in r['checks'])):
            errors.append('Unsigned initial records cannot claim findings or confirmed law.')
        if r['admission_decision']['status'] == 'admitted' and not admission_ready(r):
            errors.append('Admission gates are not satisfied.')
        seen, parent = {r['review_id']}, r['parent_review_id']
        if r['trigger_type'] != 'initial-intake' and not parent:
            errors.append('Update reviews require a parent.')
        while parent:
            if parent in seen:
                errors.append('Cyclic review history.')
                break
            seen.add(parent)
            p = load_case(root, parent)
            if p['subject_id'] != r['subject_id'] or p['created_at'] > r['created_at']:
                errors.append('Invalid parent identity or chronology.')
            parent = p['parent_review_id']
        for name, digest in read(d / 'generated.json').items():
            if name not in ('packet.md', 'matrix.md', 'evidence.md') or byte_digest((d / name).read_bytes()) != digest:
                errors.append('Generated material conflict; resolve human edits explicitly.')
        if (d / 'archive.json').exists() != r['archived'] or (not r['archived'] and r['archive_sha256'] is not None):
            errors.append('Archive file and lifecycle marker disagree.')
        if r['archived']:
            bundle = read(d / 'archive.json')
            if fingerprint(bundle) != r['archive_sha256'] or bundle['record'] != {**r, 'archived': False, 'archive_sha256': None} or bundle['workbook'] != content:
                errors.append('Archived original changed.')
    except (ReviewError, KeyError, TypeError, OSError, ValueError):
        errors.append('Review dependency, public-material or signature validation failed (input redacted).')
    return errors


def sync_event(root, rid, url, api=github_api):
    d = case_dir(root, rid)
    before = read(d / 'record.json')
    if before['archived']:
        raise ReviewError('Archived reviews are read-only.')
    if validate_record(root, before):
        raise ReviewError('Resolve validation errors before importing any decision.')
    if url in [h['source'] for h in before['history']]:
        return False
    content = (d / 'workbook.md').read_text(encoding='utf-8')
    event = verify_event(url, binding(before, content), rid, api)
    r = apply_event(root, before, content, event)
    snap = {'before': before, 'after': core(r), 'workbook': content, 'event': event}
    ref = f'{CASES}/{rid}/history/{len(r["history"]):04}.json'
    if safe(root, ref).exists():
        raise ReviewError('History path conflict; refuse overwrite.')
    public_guard(snap)
    history(r, before['status'], url, event['axis']+': '+event['decision']+'; '+event['reason'], (ref, fingerprint(snap)))
    write(safe(root, ref), snap)
    write(d / 'record.json', r)
    return True


def start(root, rid, reviewer, reason, source):
    d = case_dir(root, rid)
    r = read(d / 'record.json')
    if r['archived'] or r['status'] not in ('evidence-ready', 'needs-changes') or validate_record(root, r):
        raise ReviewError('Only valid evidence-ready or corrected needs-changes reviews can be submitted.')
    if not re.fullmatch('[A-Za-z0-9-]+', reviewer) or not reason.strip():
        raise ReviewError('A public reviewer login and submission reason are required.')
    public_guard(reason)
    reference(source)
    old = r['status']
    r.update(status='in-review', assigned_reviewer=reviewer)
    history(r, old, source, reason)
    write(d / 'record.json', r)


def archive(root, rid):
    d = case_dir(root, rid)
    r = read(d / 'record.json')
    if r['archived']:
        return
    if validate_record(root, r) or r['status'] not in ('approved-scope', 'rejected'):
        raise ReviewError('Only a valid signed final professional record can be archived.')
    if (d / 'archive.json').exists():
        raise ReviewError('Archive already exists; refuse overwrite.')
    history(r, r['status'], 'cli:archive', 'Preserve signed original; no admission implied.')
    bundle = {'record': r, 'workbook': (d / 'workbook.md').read_text(encoding='utf-8')}
    write(d / 'archive.json', bundle)
    r.update(archived=True, archive_sha256=fingerprint(bundle))
    write(d / 'record.json', r)


def diff_reviews(root, old_id, new_id, authority=None):
    old, new = load_case(root, old_id), load_case(root, new_id)
    if old['subject_id'] != new['subject_id']:
        raise ReviewError('Diff requires the same subject.')
    def inventory(r):
        return {x['path']: x['blob_sha'] for x in read(case_dir(root, r['review_id']) / 'inventory.json')['files']}
    a, b = inventory(old), inventory(new)
    changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    rules = read(case_dir(root, new_id) / 'templates.json')
    all_ids = {c['check_id'] for c in new['checks']}
    if authority:
        hits = {c['check_id'] for c in rules if authority.casefold() in json.dumps(c, ensure_ascii=False).casefold()}
        hits |= {c['check_id'] for c in old['checks'] if authority.casefold() in json.dumps(c['authority_refs'], ensure_ascii=False).casefold()}
        impacted = sorted(hits or all_ids)
    else:
        impacted = sorted(all_ids)  # Conservative: prose locators cannot safely prove non-impact.
    return {'subject_id': new['subject_id'], 'old_review_id': old_id, 'new_review_id': new_id,
            'changed_files': changed, 'added_scope': sorted(set(new['review_scope'])-set(old['review_scope'])),
            'removed_scope': sorted(set(old['review_scope'])-set(new['review_scope'])), 'authority_query': authority,
            'checks_requiring_confirmation': impacted, 'confirmation_status': 'pending-professional-confirmation',
            'prior_evidence_for_reference_only': {c['check_id']: c['evidence_refs'] for c in old['checks'] if c['check_id'] not in impacted}}


def immutable_history(root, base):
    errors = []
    def git(*args):
        return subprocess.run(['git', *args], cwd=root, capture_output=True, check=True).stdout
    try:
        paths = git('ls-tree', '-r', '--name-only', base, '--', CASES).decode().splitlines()
        for rel in paths:
            fixed = '/history/' in rel or rel.endswith(('/archive.json', '/subject.json', '/inventory.json', '/templates.json'))
            p = safe(root, rel)
            if fixed and (not p.exists() or p.read_bytes() != git('show', f'{base}:{rel}')):
                errors.append('Previously recorded evidence was changed or removed.')
            if rel.endswith('/record.json'):
                old = json.loads(git('show', f'{base}:{rel}'))
                if not p.exists():
                    errors.append('Historical review was removed.')
                    continue
                new = read(p)
                if new['history'][:len(old['history'])] != old['history'] or (old['archived'] and new != old):
                    errors.append('Historical transitions or archived record were rewritten.')
    except (OSError, subprocess.SubprocessError, ValueError, KeyError):
        errors.append('Cannot verify review immutability against Git baseline.')
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('init', help='create an unsigned review from public metadata')
    p.add_argument('--subject', required=True)
    p.add_argument('--trigger', choices=TRIGGERS, default='initial-intake')
    p.add_argument('--parent')
    p.add_argument('--review-id')
    for name in ('prepare', 'digest', 'archive'):
        sub.add_parser(name).add_argument('review_id')
    p = sub.add_parser('start', help='assign/submit for human review, never approve')
    p.add_argument('review_id')
    p.add_argument('--reviewer', required=True)
    p.add_argument('--reason', required=True)
    p.add_argument('--source', required=True)
    p = sub.add_parser('sync', help='import a verified HUMAN GitHub Review event, not an approval command')
    p.add_argument('review_id')
    p.add_argument('--event-url', required=True)
    p = sub.add_parser('validate', help='offline structure/history; --online also authenticates human events')
    p.add_argument('--online', action='store_true')
    p.add_argument('--base-ref')
    p = sub.add_parser('status')
    p.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    p = sub.add_parser('diff')
    p.add_argument('old_review_id')
    p.add_argument('new_review_id')
    p.add_argument('--authority')
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        if args.command == 'init':
            print(init_review(root, args.subject, args.trigger, args.parent, args.review_id))
        elif args.command == 'prepare':
            prepare(root, args.review_id)
            print('Prepared; human opinions preserved.')
        elif args.command == 'start':
            start(root, args.review_id, args.reviewer, args.reason, args.source)
            print('Submitted; no approval granted.')
        elif args.command == 'digest':
            d = case_dir(root, args.review_id)
            print(binding(read(d / 'record.json'), (d / 'workbook.md').read_text(encoding='utf-8')))
        elif args.command == 'sync':
            print('Imported human event.' if sync_event(root, args.review_id, args.event_url) else 'Already imported; unchanged.')
        elif args.command == 'archive':
            archive(root, args.review_id)
            print('Signed original archived; no admission implied.')
        elif args.command == 'diff':
            print(json.dumps(diff_reviews(root, args.old_review_id, args.new_review_id, args.authority), ensure_ascii=False, indent=2))
        elif args.command == 'status':
            print('Review | subject | legal | rights | engineering | admission | remaining | due | archive')
            for r in all_records(root):
                public_guard(r)
                todo = [c['check_id'] for c in r['checks'] if c['check_status'] in ('pending', 'needs-changes', 'fail')]
                due = bool(r['next_review_date'] and date.fromisoformat(r['next_review_date']) <= args.as_of)
                print(' | '.join(str(x) for x in (r['review_id'], r['subject_id'], r['status'], r['rights_review']['status'], r['engineering_review']['status'], r['admission_decision']['status'], len(todo), due, r['archived'])))
                print('  TODO: '+', '.join(todo)+'; dimensions: '+', '.join(x for x in ROLES if r[x]['status'] in ('pending', 'not-admitted', 'needs-changes')))
        else:
            records = all_records(root)
            errors = [e for r in records for e in validate_record(root, r, args.online)]
            if any(p.is_dir() and not (p / 'record.json').exists() for p in safe(root, CASES).iterdir()):
                errors.append('Incomplete review directory; inspect interrupted initialization.')
            if args.base_ref:
                errors += immutable_history(root, args.base_ref)
            if len(records) != len({r['review_id'] for r in records}):
                errors.append('Duplicate Review IDs.')
            if errors:
                print('\n'.join(errors), file=sys.stderr)
                return 1
            events = sum(bool(h['snapshot_ref']) for r in records for h in r['history'])
            print(f'PASS: {len(records)} reviews; '+(f'{events} human event(s) verified online; no legal approval inferred.' if args.online else 'offline structure/history only, not human identity or legal correctness.'))
    except ReviewError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        print('Review operation failed safely; check contracts, public-material policy and GitHub access. Input was not logged.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
