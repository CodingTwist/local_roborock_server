"""Route handler for /user/scene/home/{id}."""

from __future__ import annotations

import re
from typing import Any

from shared.context import ServerContext
from shared.http_helpers import wrap_response

from .service import list_scenes_for_home


def match(path: str) -> bool:
    clean = path.rstrip("/")
    return bool(re.fullmatch(r"/user/scene/home/[^/]+", clean))


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params
    requested_home_id = clean_path.rstrip("/").split("/")[-1]
    return wrap_response(list_scenes_for_home(ctx, requested_home_id))

