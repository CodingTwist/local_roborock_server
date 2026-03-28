"""Route handler for /api/v1/appfeatureplugin."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from ...plugin.common import APP_FEATURE_PLUGIN_LIST, proxied_plugin_records


def _ok(data: Any) -> dict[str, Any]:
    return {"code": 200, "msg": "success", "data": data}


def match(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/appfeatureplugin"


def build(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    return _ok({"plugins": proxied_plugin_records(ctx, APP_FEATURE_PLUGIN_LIST)})

