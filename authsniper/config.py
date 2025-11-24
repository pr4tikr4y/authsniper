from dataclasses import dataclass
from typing import List, Optional, Dict
import yaml


@dataclass
class LoginConfig:
    url: str
    method: str
    username_field: str
    password_field: str
    test_username: Optional[str] = None
    test_passwords: Optional[List[str]] = None
    success_indicator: Optional[str] = None
    failure_indicator: Optional[str] = None


@dataclass
class SessionConfig:
    protected_url: Optional[str] = None


@dataclass
class JwtConfig:
    sample_token: Optional[str] = None
    expected_alg: Optional[str] = None
    max_lifetime_seconds: Optional[int] = None


@dataclass
class TargetConfig:
    target_name: str
    base_url: str
    login: LoginConfig
    session: SessionConfig
    jwt: Optional[JwtConfig] = None


def load_config(path: str) -> TargetConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    login_data = data.get("login", {})
    session_data = data.get("session", {})
    jwt_data: Dict = data.get("jwt", {}) or {}

    login = LoginConfig(
        url=login_data["url"],
        method=login_data.get("method", "POST").upper(),
        username_field=login_data["username_field"],
        password_field=login_data["password_field"],
        test_username=login_data.get("test_username"),
        test_passwords=login_data.get("test_passwords", []),
        success_indicator=login_data.get("success_indicator"),
        failure_indicator=login_data.get("failure_indicator"),
    )

    session = SessionConfig(
        protected_url=session_data.get("protected_url"),
    )

    jwt_cfg = None
    if jwt_data:
        jwt_cfg = JwtConfig(
            sample_token=jwt_data.get("sample_token"),
            expected_alg=jwt_data.get("expected_alg"),
            max_lifetime_seconds=jwt_data.get("max_lifetime_seconds"),
        )

    return TargetConfig(
        target_name=data["target_name"],
        base_url=data["base_url"],
        login=login,
        session=session,
        jwt=jwt_cfg,
    )
