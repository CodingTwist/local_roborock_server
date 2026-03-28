"""Route handler for bootstrap time resolution."""

from __future__ import annotations

import time
from typing import Any

from shared.context import ServerContext
from shared.http_helpers import wrap_response


def match(path: str) -> bool:
    return "time" in path


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return wrap_response(int(time.time()))

