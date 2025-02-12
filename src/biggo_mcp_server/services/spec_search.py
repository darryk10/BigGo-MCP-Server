from logging import getLogger
from aiohttp import ClientSession
from ..types.api_ret.spec import SpecIndexesAPIRet, SpecMappingAPIRet, SpecSearchAPIRet
from ..lib.access_token import get_access_token
from ..types.setting import BigGoMCPSetting

logger = getLogger(__name__)


class SpecSearchService:

    def __init__(self, setting: BigGoMCPSetting):
        self._setting = setting

    async def _get_access_token(self) -> str:
        if self._setting.client_id is None or self._setting.client_secret is None:
            err_msg = "Client ID or Client Secret is not set"
            logger.error(err_msg)
            raise ValueError(err_msg)

        return await get_access_token(
            self._setting.client_id,
            self._setting.client_secret,
        )

    async def spec_indexes(self) -> list[str]:
        access_token = await self._get_access_token()

        url = f"{self._setting.es_proxy_url}/_cat/indices/spec*"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status >= 400:
                    err_msg = f"spec indexes api error: {await response.text()}"
                    logger.error(err_msg)
                    raise ValueError(err_msg)

                data = SpecIndexesAPIRet.model_validate(await response.json())

        return data.root

    async def spec_mapping(self, index: str) -> dict:
        access_token = await self._get_access_token()

        url = f"{self._setting.es_proxy_url}/{index}/_mapping"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status >= 400:
                    err_msg = f"spec mapping api error: {await response.text()}"
                    logger.error(err_msg)
                    raise ValueError(err_msg)

                data = SpecMappingAPIRet.model_validate(await response.json())

        return data.root

    async def search(self, index: str, query: str, size: int) -> list[dict]:
        access_token = await self._get_access_token()

        url = f"{self._setting.es_proxy_url}/{index}/_search"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        body = {
            "size": size,
            "query": query,
        }

        async with ClientSession() as session:
            async with session.post(url, headers=headers,
                                    json=body) as response:
                if response.status >= 400:
                    err_msg = f"spec search api error: {await response.text()}"
                    logger.error(err_msg)
                    raise ValueError(err_msg)

                data = SpecSearchAPIRet.model_validate(await response.json())

        return data.root
