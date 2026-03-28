"""Route handler for bootstrap location resolution."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext
from shared.http_helpers import wrap_response


def match(path: str) -> bool:
    return "location" in path


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    return wrap_response({"country": ctx.region.upper(), "timezone": "America/New_York"})

