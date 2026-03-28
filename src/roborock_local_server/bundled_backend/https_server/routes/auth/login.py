"""Route handlers for v1 login/auth endpoints."""

from __future__ import annotations

from typing import Any

from shared.context import ServerContext

from .service import build_login_data_response, ok


def match_login_ml_c(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/ml/c"


def match_login_email_code_send(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/sendEmailCode"


def match_login_sms_code_send(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/sendSmsCode"


def match_login_code_validate(path: str) -> bool:
    return path.rstrip("/") in {
        "/api/v1/validateEmailCode",
        "/api/v1/validateSmsCode",
    }


def match_login_code_submit(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/loginWithCode"


def match_login_password_submit(path: str) -> bool:
    return path.rstrip("/") == "/api/v1/login"


def build_login_ml_c(
    ctx: ServerContext,
    query_params: dict[str, list[str]],
    body_params: dict[str, list[str]],
    clean_path: str,
) -> dict[str, Any]:
    _ = ctx, query_params, body_params, clean_path
    return ok({"r": False})


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
