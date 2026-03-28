"""Route handler for /api/v5/product."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from ...auth.service import ok
from ..product_service import build_product_response


def match(path: str) -> bool:
    return path.rstrip("/") == "/api/v5/product"


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    return ok(build_product_response(ctx))
