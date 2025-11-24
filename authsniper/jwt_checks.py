import time
from typing import Dict, Any

from rich.console import Console
import jwt  # PyJWT

from .config import TargetConfig

console = Console()


def analyze_jwt(cfg: TargetConfig) -> Dict[str, Any]:
    console.rule("[bold yellow]JWT Security Checks[/bold yellow]")

    if not cfg.jwt or not cfg.jwt.sample_token:
        console.print(
            "[yellow]No JWT sample_token configured, skipping JWT checks.[/yellow]"
        )
        return {
            "check": "jwt",
            "skipped": True,
            "reason": "no sample_token",
        }

    token = cfg.jwt.sample_token

    try:
        # Inspect header and payload WITHOUT verifying signature
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={"verify_signature": False})
    except Exception as e:
        console.print(f"[red]Failed to decode JWT:[/red] {e}")
        return {
            "check": "jwt",
            "error": str(e),
        }

    alg = header.get("alg", "none")
    issues = []

    console.print(f"Header: [bold]{header}[/bold]")
    console.print(f"Payload: [bold]{payload}[/bold]")

    # 1) alg = none
    if alg.lower() == "none":
        issues.append("JWT uses alg=none (critical)")

    # 2) Expected alg mismatch
    expected_alg = cfg.jwt.expected_alg
    if expected_alg and alg != expected_alg:
        issues.append(f"JWT alg '{alg}' differs from expected '{expected_alg}'")

    # 3) Exp and lifetime
    exp = payload.get("exp")
    now = int(time.time())
    lifetime = None
    if exp is None:
        issues.append("No 'exp' claim present (token may never expire)")
    else:
        iat = payload.get("iat", now)
        lifetime = exp - iat
        max_life = cfg.jwt.max_lifetime_seconds
        if max_life and lifetime > max_life:
            issues.append(
                f"Token lifetime {lifetime}s exceeds max allowed {max_life}s"
            )

    result = {
        "check": "jwt",
        "alg": alg,
        "header": header,
        "payload": payload,
        "issues": issues,
        "lifetime_seconds": lifetime,
    }

    if issues:
        console.print("[red]JWT issues detected:[/red]")
        for i in issues:
            console.print(f" - {i}")
    else:
        console.print("[green]No obvious JWT misconfigurations detected.[/green]")

    return result
