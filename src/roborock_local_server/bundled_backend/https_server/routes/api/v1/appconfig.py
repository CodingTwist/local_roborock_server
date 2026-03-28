"""Route handler for /api/v1/appconfig."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from ...auth.service import ok
from ..appconfig_service import app_config_common_payload


def match(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/appconfig"


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok(app_config_common_payload())
