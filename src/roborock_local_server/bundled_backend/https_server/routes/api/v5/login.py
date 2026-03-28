"""Route handlers for /api/v5 login/auth endpoints."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from ...auth.service import build_login_data_response, ok


def match_login_email_code_send(path: str) -> bool:
    return path.rstrip("/") == "/api/v5/email/code/send"


def match_login_sms_code_send(path: str) -> bool:
    return path.rstrip("/") == "/api/v5/sms/code/send"


def match_login_code_validate(path: str) -> bool:
    return path.rstrip("/") in {
        "/api/v5/email/code/validate",
        "/api/v5/sms/code/validate",
    }


def match_login_code_submit(path: str) -> bool:
    clean = path.rstrip("/")
    return clean in {
        "/api/v5/auth/email/login/code",
        "/api/v5/auth/phone/login/code",
        "/api/v5/auth/mobile/login/code",
    }


def match_login_password_submit(path: str) -> bool:
    clean = path.rstrip("/")
    return clean in {
        "/api/v5/auth/email/login/pwd",
        "/api/v5/auth/phone/login/pwd",
        "/api/v5/auth/mobile/login/pwd",
    }


def match_login_password_reset(path: str) -> bool:
    return path.rstrip("/") in {
        "/api/v5/user/password/mobile/reset",
        "/api/v5/user/password/email/reset",
    }


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


def build_login_password_submit(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = query_params, body_params, clean_path
    return build_login_data_response(ctx)


def build_login_password_reset(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok(None)
