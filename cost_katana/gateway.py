"""
AI Gateway helpers — HTTP headers and dashboard APIs aligned with Cost Katana gateway defaults.

The hosted gateway enables input firewall (LLM security) and output moderation by default.
Send explicit ``false`` headers only to opt out.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

# Relative to API origin (e.g. https://api.costkatana.com)
GATEWAY_API_PREFIX = "/api/gateway"


def gateway_request_headers(
    *,
    llm_security_enabled: Optional[bool] = None,
    output_moderation_enabled: Optional[bool] = None,
) -> Dict[str, str]:
    """
    Extra HTTP headers for direct ``POST /api/gateway/v1/...`` calls (e.g. with httpx).

    Server defaults: both protections ON. Pass ``False`` to opt out.

    Args:
        llm_security_enabled: If False, sets ``CostKatana-LLM-Security-Enabled: false``.
        output_moderation_enabled: If False, sets ``CostKatana-Output-Moderation-Enabled: false``.
    """
    h: Dict[str, str] = {}
    if llm_security_enabled is False:
        h["CostKatana-LLM-Security-Enabled"] = "false"
    if output_moderation_enabled is False:
        h["CostKatana-Output-Moderation-Enabled"] = "false"
    return h
