from typing import Dict, Any, Optional
import requests


class HttpClient:
    """
    Simple wrapper around requests.Session so that
    proxies, headers, logging etc. can be added easily later.
    """

    def __init__(self, base_url: str, verify: bool = True):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.verify = verify

    def post(
        self,
        url: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        return self.session.post(url, data=data, headers=headers or {})

    def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        return self.session.get(url, headers=headers or {})
