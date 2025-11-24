from typing import Dict, Any
from rich.console import Console

from .config import TargetConfig
from .http_client import HttpClient
from .auth_checks import _login_request

console = Console()


def _ensure_logged_in(client: HttpClient, cfg: TargetConfig) -> bool:
    if not cfg.login.test_username or not cfg.login.test_passwords:
        console.print(
            "[yellow]No test credentials configured, cannot perform session checks.[/yellow]"
        )
        return False

    password = cfg.login.test_passwords[0]
    resp = _login_request(client, cfg, cfg.login.test_username, password)
    success_indicator = cfg.login.success_indicator
    if success_indicator and success_indicator.lower() in resp.text.lower():
        console.print("[green]Login seems successful with test credentials.[/green]")
        return True

    console.print(
        "[red]Login did not appear successful with the first test password. "
        "Session checks may be invalid.[/red]"
    )
    return False


def check_cookie_flags(client: HttpClient, cfg: TargetConfig) -> Dict[str, Any]:
    console.rule("[bold yellow]Session Cookie Flags[/bold yellow]")

    cookies = client.session.cookies
    results = []

    for cookie in cookies:
        name = cookie.name
        rest = getattr(cookie, "_rest", {})
        secure = cookie.secure
        httponly = bool(rest.get("HttpOnly", False))
        samesite = rest.get("SameSite", "None")

        issue_flags = []
        if not secure:
            issue_flags.append("missing Secure")
        if not httponly:
            issue_flags.append("missing HttpOnly")
        if samesite.lower() == "none":
            issue_flags.append("SameSite=None (review for CSRF risk)")

        console.print(
            f"Cookie [bold]{name}[/bold] -> "
            f"Secure={secure}, HttpOnly={httponly}, SameSite={samesite}"
        )

        results.append(
            {
                "name": name,
                "secure": secure,
                "httponly": httponly,
                "samesite": samesite,
                "issues": issue_flags,
            }
        )

    return {
        "check": "cookie_flags",
        "cookies": results,
    }


def check_session_protection(client: HttpClient, cfg: TargetConfig) -> Dict[str, Any]:
    console.rule("[bold yellow]Session Protection (Protected URL)[/bold yellow]")
    if not cfg.session.protected_url:
        console.print(
            "[yellow]No protected_url configured, skipping session protection check.[/yellow]"
        )
        return {
            "check": "session_protection",
            "skipped": True,
            "reason": "no protected_url",
        }

    resp = client.get(cfg.session.protected_url)
    status = resp.status_code
    console.print(
        f"GET {cfg.session.protected_url} -> status={status}, len={len(resp.text)}"
    )

    return {
        "check": "session_protection",
        "status_code": status,
    }


def run_session_checks(client: HttpClient, cfg: TargetConfig) -> Dict[str, Any]:
    console.rule(f"[bold blue]Session Checks for {cfg.target_name}[/bold blue]")

    if not _ensure_logged_in(client, cfg):
        return {
            "logged_in": False,
            "reason": "could not confirm login with provided test credentials",
        }

    cookie_result = check_cookie_flags(client, cfg)
    protection_result = check_session_protection(client, cfg)

    return {
        "logged_in": True,
        "cookie_flags": cookie_result,
        "session_protection": protection_result,
    }
