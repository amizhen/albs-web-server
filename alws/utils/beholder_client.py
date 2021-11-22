import urllib.parse

import aiohttp


class BeholderClient:
    def __init__(self, host: str, token: str = None):
        self._host = host
        self._headers = {}
        if token is not None:
            self._headers.update({
                'Authorization': f'Bearer {token}',
            })

    def _get_url(self, endpoint: str) -> str:
        return urllib.parse.urljoin(self._host, endpoint)

    async def get(self, endpoint: str,
                  headers: dict = None, params: dict = None):
        req_headers = self._headers.copy()
        if headers:
            req_headers.update(**headers)
        full_url = self._get_url(endpoint)
        async with aiohttp.ClientSession(headers=req_headers) as session:
            async with session.get(full_url, params=params) as response:
                json = await response.json()
                response.raise_for_status()
                return json