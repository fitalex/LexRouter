"""Normalize one discovery hit into the existing candidate contract.

The adapter only maps facts that are explicitly present in the hit or in a
pinned snapshot.  It never infers a legal jurisdiction from language, never
turns a license hint into a verified license, never copies full text, and never
sets a regulatory-currency date.  Unknown values become explicit unknown
states or a ``needs-evidence`` result.
"""

from __future__ import annotations

import hashlib
from urllib.parse import unquote, urlsplit

from .dedupe import source_identity
from .models import FetchStatus, SearchHit, SourceSnapshot
from .util import (
    AUTHORIZATION_STATUSES,
    BUSINESS_CATEGORIES,
    JURISDICTION_STATUSES,
    JURISDICTION_VALUES,
    RUNTIMES,
    SOURCE_FAILURE_STATUSES,
    append_note,
    clean,
    clip,
    is_calendar_date,
    is_full_sha,
    is_https_url,
    slugify,
    unique_https_urls,
)


class NormalizationError(ValueError):
    """A hit cannot become a contract-valid candidate without inventing data."""

    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"{field}: {message}")
        self.field = field
        self.message = message


def normalize(hit: SearchHit, snapshot: SourceSnapshot | None = None) -> dict[str, object]:
    """Return one candidate dict compatible with ``schemas`` candidate checks."""
    title = clean(hit.title)
    if not title:
        raise NormalizationError("title", "a non-empty title is required")
    url = clean(hit.url)
    if not is_https_url(url):
        raise NormalizationError("url", "an absolute HTTPS URL is required")
    retrieved_at = clean(hit.retrieved_at)
    if not is_calendar_date(retrieved_at):
        raise NormalizationError(
            "retrieved_at",
            "a valid YYYY-MM-DD retrieval date is required",
        )
    if snapshot is not None:
        if not isinstance(snapshot, SourceSnapshot):
            raise TypeError("snapshot must be a SourceSnapshot or None")
        if clean(snapshot.ref.source_id) != clean(hit.source_id):
            raise NormalizationError(
                "source_id",
                "snapshot and hit refer to different source IDs",
            )
        if source_identity(snapshot.ref.url) != source_identity(url):
            raise NormalizationError(
                "url",
                "snapshot and hit refer to different source entries",
            )

    categories = _categories(hit, snapshot)
    jurisdiction = _jurisdiction(hit, snapshot)
    authorization = _authorization(snapshot, url)
    source_verification = _source_verification(hit, snapshot, retrieved_at)
    runtime, runtime_evidence = _runtime(hit, snapshot)
    candidate_status = _candidate_status(source_verification, authorization, jurisdiction)

    maintainer = ""
    if snapshot is not None:
        maintainer = clean(snapshot.maintainer)
    if not maintainer:
        maintainer = clean(hit.maintainer)
    if not maintainer:
        maintainer = "未核实（搜索命中未提供公开维护账号）"

    description = clean(hit.snippet)
    if description:
        description = clip(description, 500)
    else:
        description = (
            "搜索命中的来源入口；未读取或未核实能力、授权与法律适用，待补证据。"
        )

    evidence_notes = [
        "离线 Discovery 适配器归一化结果；未执行来源 Skill，未复制未授权全文。",
    ]
    if _looks_synthetic(hit):
        evidence_notes.append("合成 fixture 数据，不是真实发现记录或法律核查证据。")
    if snapshot is None:
        evidence_notes.append("仅使用搜索命中，未读取固定版本入口。")
    elif snapshot.status is FetchStatus.METADATA_ONLY:
        evidence_notes.append("仅读取固定版本元数据，全文按授权边界保留在来源处。")
    if candidate_status == "rejected":
        evidence_notes.append("授权状态为 not-permitted，按候选契约判为 rejected。")
    evidence_notes.append(
        "candidate/needs-evidence 仅为继续整理状态，不构成法律、授权或法规时效结论。"
    )

    return {
        "candidate_id": _candidate_id(hit),
        "name": clip(title, 120),
        "description": description,
        "source_url": url,
        "maintainer": maintainer,
        "business_categories": list(categories),
        "jurisdiction": jurisdiction,
        "runtime": runtime,
        "runtime_evidence": runtime_evidence,
        "source_verification": source_verification,
        "authorization": authorization,
        "regulatory_currency": {
            "status": "not-checked",
            "as_of": None,
            "evidence_urls": [],
            "notes": (
                "自动化 Discovery 不核实法规时效；"
                "须由具备相应能力的法律专业人员独立复核。"
            ),
        },
        "candidate_status": candidate_status,
        "evidence_notes": " ".join(evidence_notes),
    }


def _looks_synthetic(hit: SearchHit) -> bool:
    return any(
        "synthetic" in clean(value).lower()
        for value in (hit.provider, hit.source_id, hit.url)
    )


def _candidate_id(hit: SearchHit) -> str:
    identity = source_identity(hit.url)
    digest = hashlib.sha256("\0".join(identity).encode("utf-8")).hexdigest()[:8]
    stem = clean(hit.source_id)
    if not stem:
        stem = unquote(urlsplit(hit.url).path.rstrip("/").rsplit("/", 1)[-1])
    return f"discovery-{slugify(stem, 60)}-{digest}"


def _categories(hit: SearchHit, snapshot: SourceSnapshot | None) -> tuple[str, ...]:
    raw: tuple[str, ...] = hit.business_categories
    if snapshot is not None and snapshot.business_categories:
        raw = snapshot.business_categories
    known = tuple(dict.fromkeys(
        category for category in raw if category in BUSINESS_CATEGORIES
    ))
    if not known:
        raise NormalizationError(
            "business_categories",
            "at least one known business category is required; the adapter does not guess one",
        )
    return known


def _runtime(hit: SearchHit, snapshot: SourceSnapshot | None) -> tuple[str, str]:
    runtime = ""
    evidence = ""
    if snapshot is not None:
        runtime = clean(snapshot.runtime)
        evidence = clean(snapshot.runtime_evidence)
    if runtime not in RUNTIMES:
        runtime = clean(hit.runtime)
    if runtime not in RUNTIMES:
        runtime = "other"
    if not evidence:
        evidence = clean(hit.runtime_evidence)
    if not evidence:
        evidence = "未识别运行载体；按正式枚举记为 other，待核实。"
    return runtime, evidence


def _jurisdiction(
    hit: SearchHit,
    snapshot: SourceSnapshot | None,
) -> dict[str, object]:
    data: dict[str, object] = {}
    if snapshot is not None and isinstance(snapshot.jurisdiction, dict):
        data = snapshot.jurisdiction
    value = clean(data.get("value")) or "unknown"
    status = clean(data.get("status")) or "pending-verification"
    evidence_url = clean(data.get("evidence_url"))
    notes = clean(data.get("notes"))

    if value not in JURISDICTION_VALUES:
        value = "unknown"
        status = "pending-verification"
        notes = append_note(notes, "未知法域值已记为 unknown，未据名称或语言推断。")
    if status not in JURISDICTION_STATUSES:
        status = "pending-verification"
        notes = append_note(notes, "未知法域状态已降级为 pending-verification。")
    if value == "unknown":
        status = "pending-verification"
        notes = append_note(notes, "未获得可定位的法域声明证据。")
    if status == "verified":
        # Discovery cannot perform the legal review that "verified" asserts.
        status = "source-declared"
        notes = append_note(
            notes,
            "自动化适配器不执行法律专业复核，verified 降为 source-declared。",
        )
    if not is_https_url(evidence_url):
        evidence_url = clean(hit.url)
        notes = append_note(notes, "无独立法域证据链接，仅保留命中入口，不能视为已核实。")
    if not notes:
        notes = "未获得法域声明；不做推断。"
    return {
        "value": value,
        "status": status,
        "evidence_url": evidence_url,
        "notes": notes,
    }


def _authorization(
    snapshot: SourceSnapshot | None,
    hit_url: str,
) -> dict[str, object]:
    if snapshot is None:
        return {
            "status": "pending-verification",
            "license": "not-identified",
            "evidence_urls": [hit_url],
            "notes": "未读取固定版本许可文本；所列链接仅为待核查入口，不是许可证据。",
        }

    status = clean(snapshot.authorization_status) or "pending-verification"
    license_name = clean(snapshot.license) or "not-identified"
    evidence_urls = unique_https_urls(snapshot.authorization_evidence_urls)
    has_real_evidence = bool(evidence_urls)
    notes = clean(snapshot.authorization_notes)

    if snapshot.status not in {FetchStatus.OK, FetchStatus.METADATA_ONLY}:
        if status == "verified":
            status = "pending-verification"
            notes = append_note(notes, "固定版本读取失败，不能维持 verified 授权状态。")
    if status not in AUTHORIZATION_STATUSES:
        notes = append_note(
            notes,
            f"未知授权状态 {status!r} 已降级为 pending-verification。",
        )
        status = "pending-verification"
    if status == "verified":
        if license_name in {"", "not-identified", "unknown"} or not has_real_evidence:
            status = "pending-verification"
            notes = append_note(
                notes,
                "verified 缺可识别许可名称或 HTTPS 许可证据，降级为 pending-verification。",
            )
    if not evidence_urls:
        # The candidate contract requires a non-empty evidence array; the source
        # entry is a pending location, not a license finding.
        evidence_urls = (hit_url,)
        notes = append_note(
            notes,
            "未提供独立许可证据；仅保留来源入口作为待核查位置。",
        )
    if not notes:
        notes = "未核对固定版本许可文本及复制/再分发范围。"
    return {
        "status": status,
        "license": license_name,
        "evidence_urls": list(evidence_urls),
        "notes": notes,
    }


def _source_verification(
    hit: SearchHit,
    snapshot: SourceSnapshot | None,
    retrieved_at: str,
) -> dict[str, object]:
    if snapshot is None:
        revision = hit.revision if is_full_sha(hit.revision) else "unresolved"
        return {
            "status": "unverified",
            "checked_at": retrieved_at,
            "revision": revision,
            "evidence_urls": [hit.url],
            "notes": "仅搜索命中，未读取固定版本入口；来源、版本与内容均待核。",
        }

    checked_at = snapshot.retrieved_at if is_calendar_date(snapshot.retrieved_at) else retrieved_at
    revision = snapshot.revision if is_full_sha(snapshot.revision) else ""
    if not revision:
        revision = hit.revision if is_full_sha(hit.revision) else "unresolved"
    evidence_urls = unique_https_urls([*snapshot.evidence_urls, hit.url])
    if not evidence_urls:
        evidence_urls = (hit.url,)
    notes = clean(snapshot.notes)

    if snapshot.status in {FetchStatus.OK, FetchStatus.METADATA_ONLY}:
        status = "verified-public" if revision != "unresolved" else "unverified"
        if snapshot.status is FetchStatus.METADATA_ONLY:
            notes = append_note(
                notes,
                "固定版本元数据已读取；全文未复制，需回到来源处核读。",
            )
        else:
            notes = append_note(notes, "固定版本与证据链接已读取（离线 fixture）。")
    elif snapshot.status in SOURCE_FAILURE_STATUSES:
        if snapshot.status in {FetchStatus.NOT_FOUND, FetchStatus.TRANSPORT_ERROR}:
            status = "unavailable"
        else:
            status = "unverified"
        notes = append_note(
            notes,
            f"固定版本读取失败：{snapshot.status.value}；未以搜索摘要替代来源核查。",
        )
    else:
        status = "unverified"
        notes = append_note(notes, "未知读取状态，按 unverified 保留。")

    if not notes:
        notes = "未提供来源核查备注。"
    return {
        "status": status,
        "checked_at": checked_at,
        "revision": revision,
        "evidence_urls": list(evidence_urls),
        "notes": notes,
    }


def _candidate_status(
    source_verification: dict[str, object],
    authorization: dict[str, object],
    jurisdiction: dict[str, object],
) -> str:
    if authorization["status"] == "not-permitted":
        return "rejected"
    if (
        source_verification["status"] == "verified-public"
        and authorization["status"] == "verified"
        and jurisdiction["value"] == "CN-Mainland"
        and jurisdiction["status"] in {"source-declared", "verified"}
    ):
        return "candidate"
    return "needs-evidence"
