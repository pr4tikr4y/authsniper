import argparse
import json

from rich.console import Console

from .config import load_config
from .http_client import HttpClient
from .auth_checks import run_auth_checks
from .session_checks import run_session_checks
from .jwt_checks import analyze_jwt
from . import __version__

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="authsniper",
        description=(
            "AuthSniper – Authentication & Session Security Toolkit "
            "(for authorized testing only)"
        ),
    )
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="Path to YAML config for the target",
    )
    parser.add_argument(
        "--checks",
        choices=["auth", "session", "jwt", "all"],
        default="all",
        help="Which checks to run",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (in addition to console output)",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"authsniper {__version__}"
    )

    args = parser.parse_args()

    cfg = load_config(args.config)
    client = HttpClient(cfg.base_url)

    results = {}

    if args.checks in ("auth", "all"):
        auth_result = run_auth_checks(client, cfg)
        results["auth"] = auth_result

    if args.checks in ("session", "all"):
        session_result = run_session_checks(client, cfg)
        results["session"] = session_result

    if args.checks in ("jwt", "all"):
        jwt_result = analyze_jwt(cfg)
        results["jwt"] = jwt_result

    if args.json:
        console.rule("[bold magenta]JSON Output[/bold magenta]")
        console.print_json(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
