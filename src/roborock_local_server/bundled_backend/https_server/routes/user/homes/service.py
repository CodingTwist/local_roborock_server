"""Shared home-state services for /user/homes endpoints."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from shared.context import ServerContext

from ..devices.service import _home_data as _base_home_data
from ..devices.service import enrich_home_data_with_cloud_snapshot
from ..devices.service import resolve_home_id

_WEB_API_INVENTORY_FILE = "web_api_inventory.json"
_DEFAULT_HOME_NAME = "Local Home"


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


def _as_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "y", "on"}:
            return True
        if lowered in {"0", "false", "no", "n", "off"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return default


def _stable_int(seed: str) -> int:
    return int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12], 16)


def _load_inventory(ctx: ServerContext) -> dict[str, Any]:
    path = ctx.http_jsonl.parent / _WEB_API_INVENTORY_FILE
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _write_inventory(ctx: ServerContext, inventory: dict[str, Any]) -> None:
    path = ctx.http_jsonl.parent / _WEB_API_INVENTORY_FILE
    try:
        path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        return


def _default_home_id(ctx: ServerContext) -> int:
    return _stable_int(f"{ctx.duid}:home")


def normalize_rooms(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    home_data = inventory.get("home")
    home = home_data if isinstance(home_data, dict) else {}
    rooms_value = _get_value(home, "rooms")
    if rooms_value is None:
        rooms_value = inventory.get("rooms")
    rooms_list = rooms_value if isinstance(rooms_value, list) else []
    rooms: list[dict[str, Any]] = []
    for index, room in enumerate(rooms_list):
        room_data = room if isinstance(room, dict) else {}
        room_id = _as_int(_get_value(room_data, "id", "room_id", default=index + 1), index + 1)
        room_name = str(_get_value(room_data, "name", default=f"Room {index + 1}"))
        rooms.append({"id": room_id, "name": room_name})
    if rooms:
        return rooms
    return [{"id": 1, "name": "Living Room"}]


def extract_home_id_from_rooms_path(ctx: ServerContext, clean_path: str) -> int:
    match = re.fullmatch(r"/user/homes/([^/]+)/rooms(?:[^/]*)", clean_path.rstrip("/"))
    if match is None:
        return _default_home_id(ctx)
    return _as_int(match.group(1), _default_home_id(ctx))


def upsert_inventory_room(ctx: ServerContext, *, home_id: int, room_name: str) -> tuple[dict[str, Any], bool]:
    inventory = _load_inventory(ctx)
    if not isinstance(inventory, dict):
        inventory = {}

    home_value = inventory.get("home")
    home = dict(home_value) if isinstance(home_value, dict) else {}
    rooms_source = home.get("rooms")
    if not isinstance(rooms_source, list):
        rooms_source = inventory.get("rooms")
    rooms = normalize_rooms({"home": {"rooms": rooms_source}}) if isinstance(rooms_source, list) else []

    normalized_name = room_name.strip() or f"Room {len(rooms) + 1}"
    existing_room = next(
        (room for room in rooms if str(room.get("name") or "").strip().casefold() == normalized_name.casefold()),
        None,
    )
    if existing_room is not None:
        room_payload = {"id": _as_int(existing_room.get("id"), 0), "name": str(existing_room.get("name") or normalized_name)}
        created = False
    else:
        next_room_id = max((_as_int(room.get("id"), 0) for room in rooms if isinstance(room, dict)), default=0) + 1
        if next_room_id <= 0:
            next_room_id = (_stable_int(f"{home_id}:{normalized_name}") % 9_000_000) + 1_000_000
        room_payload = {"id": next_room_id, "name": normalized_name}
        rooms.append(room_payload)
        created = True

    if home_id > 0:
        existing_home_id = _get_value(home, "id", "home_id", "rrHomeId", "rr_home_id")
        if existing_home_id is None:
            home["id"] = home_id
    home["rooms"] = rooms
    inventory["home"] = home
    inventory["rooms"] = rooms
    _write_inventory(ctx, inventory)
    return room_payload, created


def _device_has_runtime_did(ctx: ServerContext, duid: str) -> bool:
    runtime_credentials = getattr(ctx, "runtime_credentials", None)
    if runtime_credentials is None:
        return False
    try:
        credential_device = runtime_credentials.resolve_device(duid=duid)
    except Exception:
        return False
    if credential_device is None:
        return False
    did = str(credential_device.get("did") or "").strip()
    mqtt_user = str(credential_device.get("device_mqtt_usr") or "").strip()
    return bool(did or mqtt_user)


def _filter_home_data_to_runtime_devices(ctx: ServerContext, home_data: dict[str, Any]) -> dict[str, Any]:
    filtered_home = dict(home_data)
    allowed_product_ids: set[str] = set()

    for collection_key in ("devices", "receivedDevices", "received_devices"):
        devices_value = home_data.get(collection_key)
        devices = devices_value if isinstance(devices_value, list) else []
        filtered_devices: list[dict[str, Any]] = []
        for device in devices:
            if not isinstance(device, dict):
                continue
            duid = str(_get_value(device, "duid", "did", default="")).strip()
            if not duid or not _device_has_runtime_did(ctx, duid):
                continue
            filtered_devices.append(dict(device))
            product_id = str(_get_value(device, "productId", "product_id", default="")).strip()
            if product_id:
                allowed_product_ids.add(product_id)
        filtered_home[collection_key] = filtered_devices

    products_value = home_data.get("products")
    products = products_value if isinstance(products_value, list) else []
    filtered_products: list[dict[str, Any]] = []
    for product in products:
        if not isinstance(product, dict):
            continue
        product_id = str(_get_value(product, "id", "productId", "product_id", default="")).strip()
        if not product_id or product_id not in allowed_product_ids:
            continue
        filtered_products.append(dict(product))
    filtered_home["products"] = filtered_products
    return filtered_home


def _home_data(ctx: ServerContext) -> dict[str, Any]:
    inventory = _load_inventory(ctx)
    home_value = inventory.get("home")
    home = dict(home_value) if isinstance(home_value, dict) else {}

    home_data = dict(_base_home_data(ctx))

    lon = _get_value(home, "lon")
    if lon is not None:
        home_data["lon"] = lon
    lat = _get_value(home, "lat")
    if lat is not None:
        home_data["lat"] = lat
    geo_name = _get_value(home, "geo_name", "geoName")
    if geo_name is not None:
        home_data["geoName"] = geo_name

    home_data = enrich_home_data_with_cloud_snapshot(ctx, home_data)
    home_data = _filter_home_data_to_runtime_devices(ctx, home_data)
    home_data["id"] = resolve_home_id(home_data, home, default=_default_home_id(ctx))
    home_data["name"] = str(_get_value(home_data, "name", "home_name", default=_DEFAULT_HOME_NAME))
    return home_data


def home_payload(ctx: ServerContext) -> dict[str, Any]:
    return _home_data(ctx)


def home_rooms_payload(ctx: ServerContext) -> list[dict[str, Any]]:
    return home_payload(ctx).get("rooms", [])
