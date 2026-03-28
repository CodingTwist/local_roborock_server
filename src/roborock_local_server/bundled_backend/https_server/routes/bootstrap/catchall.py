"""Catchall bootstrap route handler."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext
from shared.http_helpers import wrap_response


def match(path: str) -> bool:
    _ = path
    return True


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params
    return wrap_response({"ok": True, "route": clean_path})
