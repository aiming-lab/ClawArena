"""Controlled tag vocabulary — the authoritative source for question tags.

stats uses this to identify "blank dimensions". The categories are used for the
subsection grouping in STATS.md §10.
"""
from __future__ import annotations

# section name → ordered tag list (order matches handbook §3 for easy manual cross-checking)
CONTROLLED_TAGS: dict[str, list[str]] = {
    "multimodal": [
        "multimodal_audio",
        "multimodal_image",
        "multimodal_video",
        "video_frame_reading",
        "modality_decoy",
    ],
    "delegation_permission": [
        "subagent_delegation",
        "parallel_subagents",
        "session_reuse",
        "background_subagent",
        "workflow",
        "stateful_subagent",
        "async_long_running",
        "partial_result_handling",
        "incremental_context_load",
        "permission_restraint",
        "path_overshoot_guard",
        "large_context_pressure",
    ],
    "update_handling": [
        "update_merge",
        "update_supersede",
        "adversarial_update",
        "stale_data",
    ],
    "structured_output": [
        "json_schema",
        "schema_by_shape",
        "cross_round_consistency",
        "compliance_token",
        "numerical_extraction",
        "verbatim_citation",
    ],
    "trap_resistance": [
        "honeypot_auto_summary",
        "ai_hallucination_decoy",
        "decoy_directory",
        "prompt_injection_resistance",
        "discredit_window",
    ],
    "office_format": [
        "office_xlsx",
        "office_docx",
        "office_pdf",
        "binary_archive",
        "sqlite_query",
        "parquet_query",
        "pcap_parse",
        "encrypted_file",
    ],
    "code_tool": [
        "bash_tool_run",
        "code_execution",
        "stderr_parsing",
        "multi_lang_code",
        "config_reading",
    ],
    "synthesis": [
        "cross_source_synthesis",
        "cross_reference_anchor",
        "multilingual",
        "temporal_reasoning",
        "triage_planning",
        "final_synthesis",
    ],
}

SECTION_LABELS: dict[str, str] = {
    "multimodal": "Multimodal",
    "delegation_permission": "Delegation / Permission",
    "update_handling": "Update Handling",
    "structured_output": "Structured Output / Cross-round",
    "trap_resistance": "Trap / Adversarial Resistance",
    "office_format": "Office / Data Formats",
    "code_tool": "Code / Tool",
    "synthesis": "Information Synthesis",
}


def all_controlled_tags() -> list[str]:
    out: list[str] = []
    for tags in CONTROLLED_TAGS.values():
        out.extend(tags)
    return out


def section_of(tag: str) -> str | None:
    for section, tags in CONTROLLED_TAGS.items():
        if tag in tags:
            return section
    return None
