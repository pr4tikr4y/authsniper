import time
from typing import List, Dict, Any
from rich.console import Console

from .config import TargetConfig
from .http_client import HttpClient

console = Console()


def _login_request(client: HttpClient, cfg: TargetConfig, username: str, password: str):
    url = cfg.login.url
    data = {
        cfg.login.username_field: username,
        cfg.login.password_field: password,
    }
    return client.post(url, data=data)


def check_rate_limiting(
    client: HttpClient, cfg: TargetConfig, attempts: int = 5, delay: float = 0.5
) -> Dict[str, Any]:
    """
    Sends several failed login attempts and checks if there is any obvious
    change in responses (status code / length). This is a heuristic.
    """
    console.rule("[bold yellow]Rate Limiting Check[/bold yellow]")

    username = cfg.login.test_username or "nonexistent_user"
    password = "WrongPassword!123"

    responses = []
    for i in range(attempts):
        resp = _login_request(client, cfg, username, password)
        responses.append(resp)
        console.print(
            f"[cyan]Attempt {i+1}[/cyan] -> {resp.status_code}, len={len(resp.text)}"
        )
        time.sleep(delay)

    first = responses[0]
    same = all(
        (r.status_code == first.status_code) and (len(r.text) == len(first.text))
        for r in responses[1:]
    )

    result = {
        "check": "rate_limiting",
        "attempts": attempts,
        "all_responses_identical": same,
    }

    if same:
        console.print(
            "[red]All responses looked identical.[/red] "
            "This might indicate missing incremental protections "
            "(no visible lockout / captcha / delay). Review manually."
        )
    else:
        console.print(
            "[green]Responses changed across attempts.[/green] "
            "There may be some form of protection in place (lockout / captcha / delay)."
        )

    return result


def check_weak_passwords(client: HttpClient, cfg: TargetConfig) -> Dict[str, Any]:
    """
    Tries a *small* set of passwords for a single known test account to quickly
    spot extremely weak password acceptance. Only for authorized testing.
    """
    console.rule("[bold yellow]Weak Password Policy Quick Check[/bold yellow]")

    username = cfg.login.test_username
    passwords: List[str] = cfg.login.test_passwords or []

    if not username or not passwords:
        console.print(
            "[yellow]No test_username or test_passwords configured. "
            "Skipping weak password check.[/yellow]"
        )
        return {
            "check": "weak_passwords",
            "skipped": True,
            "reason": "missing test_username or test_passwords",
        }

    success_indicator = cfg.login.success_indicator
    failure_indicator = cfg.login.failure_indicator

    accepted: List[str] = []

    for pwd in passwords:
        resp = _login_request(client, cfg, username, pwd)
        text = resp.text.lower()

        is_success = False
        if success_indicator and success_indicator.lower() in text:
            is_success = True
        elif failure_indicator and failure_indicator.lower() not in text:
            # fallback if failure text is absent
            is_success = True

        console.print(
            f"Testing password [bold]{pwd}[/bold] -> "
            f"status={resp.status_code}, success={is_success}"
        )

        if is_success:
            accepted.append(pwd)

    if accepted:
        console.print(
            "[red]Some very simple passwords were accepted for the test user![/red]"
        )
    else:
        console.print(
            "[green]Configured simple passwords were not accepted for the test user.[/green]"
        )

    return {
        "check": "weak_passwords",
        "accepted_passwords": accepted,
        "total_tested": len(passwords),
    }


def run_auth_checks(client: HttpClient, cfg: TargetConfig) -> Dict[str, Any]:
    console.rule(f"[bold blue]Auth Checks for {cfg.target_name}[/bold blue]")
    results = {}
    results["rate_limiting"] = check_rate_limiting(client, cfg)
    results["weak_passwords"] = check_weak_passwords(client, cfg)
    return results
