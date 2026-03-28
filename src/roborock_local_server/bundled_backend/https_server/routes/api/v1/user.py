"""Route handlers for /api/v1/user endpoints."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from ...auth.service import load_cloud_full_snapshot
from ...auth.service import load_cloud_user_data
from ...auth.service import ok

_DEFAULT_AVATAR_URL = "https://files.roborock.com/iot/default_avatar.png"
_REGION_COUNTRY_CODE = {
    "US": "1",
    "CN": "86",
    "EU": "49",
    "RU": "7",
}


def _get_value(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        return value
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


def _default_country_code_for_region(region: str) -> str:
    return _REGION_COUNTRY_CODE.get(region.upper(), "1")


def match_get_url_by_email(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/getUrlByEmail"


def match_user_info(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/userInfo"


def match_user_roles(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/user/roles"


def match_logout(path: str, method: str = "GET") -> bool:
    return method.upper() == "POST" and path.rstrip("/") == "/api/v1/logout"


def build_get_url_by_email(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    region_upper = ctx.region.upper()
    return ok(
        {
            "url": f"https://{ctx.api_host}",
            "countrycode": _default_country_code_for_region(region_upper),
            "country": region_upper,
        }
    )


def build_user_info(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    cloud_user_data = load_cloud_user_data(ctx) or {}
    snapshot = load_cloud_full_snapshot(ctx) or {}
    meta_value = snapshot.get("meta")
    meta = meta_value if isinstance(meta_value, dict) else {}
    username = str(meta.get("username") or "").strip()

    email = str(_get_value(cloud_user_data, "email", default="") or "").strip()
    mobile = str(_get_value(cloud_user_data, "mobile", default="") or "").strip()
    if not email and "@" in username:
        email = username
    if not mobile and username.isdigit():
        mobile = username

    region_upper = ctx.region.upper()
    country = str(_get_value(cloud_user_data, "country", default=region_upper) or region_upper)
    countrycode = str(
        _get_value(
            cloud_user_data,
            "countrycode",
            default=_default_country_code_for_region(region_upper),
        )
        or _default_country_code_for_region(region_upper)
    )
    nickname = str(_get_value(cloud_user_data, "nickname", default="Local User") or "Local User")
    avatarurl = str(_get_value(cloud_user_data, "avatarurl", "avatarUrl", default="") or "")
    if not avatarurl:
        avatarurl = _DEFAULT_AVATAR_URL

    return ok(
        {
            "email": email,
            "mobile": mobile,
            "countrycode": countrycode,
            "country": country,
            "nickname": nickname,
            "hasPassword": _as_bool(_get_value(cloud_user_data, "hasPassword", default=True), True),
            "avatarurl": avatarurl,
        }
    )


def build_user_roles(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok([])


def build_logout(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok(True)
