"""Route handler for /user/homes/{id}."""

from __future__ import annotations

import re
from typing import Any

from shared.context import ServerContext
from shared.http_helpers import wrap_response

from .service import home_payload


def match(path: str) -> bool:
    clean = path.rstrip("/")
    return bool(re.fullmatch(r"/(?:(?:v2|v3)/)?user/homes/[^/]+", clean))


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    return wrap_response(home_payload(ctx))

