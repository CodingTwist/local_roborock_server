"""Shared product-state services for /api/v4/product and /api/v5/product."""

from __future__ import annotations

import hashlib
from typing import Any

from shared.context import ServerContext

from ..user.homes.service import home_payload

_MODEL_PRODUCT_ID_OVERRIDES = {
    "roborock.vacuum.a87": 110,
    "roborock.vacuum.a15": 23,
    "roborock.vacuum.sc05": 10001,
}


def _as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _default_product_name(model: str) -> str:
    short_model = model.split(".")[-1].upper() if model else "VACUUM"
    return f"Roborock {short_model}"


def _stable_int(seed: str) -> int:
    return int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12], 16)


def build_product_response(ctx: ServerContext) -> dict[str, Any]:
    home_data = home_payload(ctx)
    products_value = home_data.get("products")
    products = products_value if isinstance(products_value, list) else []
    categories: dict[str, dict[str, Any]] = {}
    for product in products:
        if not isinstance(product, dict):
            continue
        raw_product_id = str(product.get("id") or "")
        category_name = str(product.get("category") or "robot.vacuum.cleaner")
        if category_name not in categories:
            category_id = len(categories) + 1
            categories[category_name] = {
                "category": {
                    "id": category_id,
                    "displayName": category_name,
                    "iconUrl": "",
                },
                "productList": [],
            }
        model = str(product.get("model") or "roborock.vacuum.a117")
        model_key = model.strip().lower()
        product_id = _MODEL_PRODUCT_ID_OVERRIDES.get(
            model_key,
            _as_int(raw_product_id, _stable_int(raw_product_id or category_name) % 1_000_000),
        )
        product_entry = {
            "id": product_id,
            "name": str(product.get("name") or _default_product_name(model)),
            "model": model,
            "packagename": f"com.roborock.{model.split('.')[-1]}",
            "ncMode": "global",
            "status": 10,
        }
        icon_url = product.get("iconUrl")
        if isinstance(icon_url, str) and icon_url:
            product_entry["picurl"] = icon_url
            product_entry["cardPicUrl"] = icon_url
            product_entry["pluginPicUrl"] = icon_url
        categories[category_name]["productList"].append(product_entry)
    return {"categoryDetailList": list(categories.values())}
