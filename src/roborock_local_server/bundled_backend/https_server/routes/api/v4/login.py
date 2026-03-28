"""Route handlers for /api/v4 login/auth endpoints."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from ...auth.service import build_login_data_response, ok

_LOGIN_CAPTCHA_CONTENT = (
    "mRHPW0lkX2AwKYqCEKDEiq6AAUd6T1sL+RQQUbSWLiVnyBfv2t4+IllIDtglVdE1kXCSMSW2SugV02sVbXslxDu4c9uZ53lUsGhmuJSUj1w="
)


def match_login_key_captcha(path: str) -> bool:
    return path.rstrip("/") == "/api/v4/key/captcha"


def match_login_email_code_send(path: str) -> bool:
    return path.rstrip("/") == "/api/v4/email/code/send"


def match_login_sms_code_send(path: str) -> bool:
    return path.rstrip("/") == "/api/v4/sms/code/send"


def match_login_code_validate(path: str) -> bool:
    return path.rstrip("/") in {
        "/api/v4/email/code/validate",
        "/api/v4/sms/code/validate",
    }


def match_login_code_submit(path: str) -> bool:
    clean = path.rstrip("/")
    return clean in {
        "/api/v4/auth/email/login/code",
        "/api/v4/auth/phone/login/code",
        "/api/v4/auth/mobile/login/code",
    }


def build_login_key_captcha(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok({"type": "RECAPTCHA", "content": _LOGIN_CAPTCHA_CONTENT})


def build_login_email_code_send(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok({"sent": True, "validForSec": 300})


def build_login_sms_code_send(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok({"sent": True, "validForSec": 300})


def build_login_code_validate(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok({"valid": True})


def build_login_code_submit(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    return build_login_data_response(ctx)
