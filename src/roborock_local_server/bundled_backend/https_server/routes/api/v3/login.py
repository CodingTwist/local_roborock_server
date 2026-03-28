"""Route handlers for /api/v3 login/auth endpoints."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from ...auth.service import build_login_data_response, ok

_LOGIN_SIGN_KEY = "DnNAYQHCVFIdHSKx"


def match_login_key_sign(path: str) -> bool:
    return path.rstrip("/") == "/api/v3/key/sign"


def match_login_sms_code_send(path: str) -> bool:
    return path.rstrip("/") == "/api/v3/sms/sendCode"


def match_login_password_submit(path: str) -> bool:
    clean = path.rstrip("/")
    return clean in {
        "/api/v3/auth/email/login",
        "/api/v3/auth/phone/login",
        "/api/v3/auth/mobile/login",
    }


def build_login_key_sign(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok({"k": _LOGIN_SIGN_KEY})


def build_login_sms_code_send(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok({"sent": True, "validForSec": 300})


def build_login_password_submit(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    return build_login_data_response(ctx)
