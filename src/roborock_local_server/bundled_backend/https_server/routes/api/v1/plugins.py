"""Route handler for /api/v1/plugins."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from ...plugin.common import CATEGORY_PLUGIN_LIST, proxied_plugin_records


def _ok(data: Any) -> dict[str, Any]:
    return {"code": 200, "msg": "success", "data": data}


def match(path: str) -> bool:
    clean = path.rstrip("/")
    return clean in {"/api/v1/plugins", "api/v1/plugins"}


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    return _ok({"categoryPluginList": proxied_plugin_records(ctx, CATEGORY_PLUGIN_LIST)})

