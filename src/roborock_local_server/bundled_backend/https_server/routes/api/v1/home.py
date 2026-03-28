"""Route handlers for /api/v1/home endpoints."""

from __future__ import annotations

import re
from typing import Any

from shared.context import ServerContext

from ...auth.service import ok
from ...user.homes.service import home_payload


def _get_value(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        return value
    return default


def _as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def match_get_home_detail(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/getHomeDetail"


def match_home_devices_order(path: str) -> bool:
    clean = path.rstrip("/")
    return bool(re.fullmatch(r"/api/v1/home/[^/]+/devices/order", clean))


def build_get_home_detail(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    home_data = home_payload(ctx)
    devices_value = home_data.get("devices")
    devices = devices_value if isinstance(devices_value, list) else []
    device_order = [
        str(_get_value(device, "duid", "did", default="")).strip()
        for device in devices
        if isinstance(device, dict) and str(_get_value(device, "duid", "did", default="")).strip()
    ]
    home_id = _as_int(_get_value(home_data, "id", "rr_home_id", "rrHomeId", "home_id", default=0), 0)
    home_name = str(_get_value(home_data, "name", "home_name", default=""))
    return ok(
        {
            "id": home_id,
            "name": home_name,
            "deviceListOrder": device_order,
            "rrHomeId": home_id,
            "rrHomeName": home_name,
            "tuyaHomeId": 0,
            "homeId": home_id,
        }
    )


def build_home_devices_order(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    home_data = home_payload(ctx)
    devices_value = home_data.get("devices")
    devices = devices_value if isinstance(devices_value, list) else []
    device_order = [
        str(_get_value(device, "duid", "did", default="")).strip()
        for device in devices
        if isinstance(device, dict) and str(_get_value(device, "duid", "did", default="")).strip()
    ]
    return ok(device_order)
