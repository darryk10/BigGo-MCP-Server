import pytest
from biggo_mcp_server.services.product_search import ProductSearchService
from biggo_mcp_server.services.spec_search import SpecMappingRet, SpecSearchService
from biggo_mcp_server.types.setting import BigGoMCPSetting
from .helper import *


@pytest.mark.asyncio
async def test_spec_search_service_indexes(setting: BigGoMCPSetting):
    service = SpecSearchService(setting)
    async with service.session():
        indexes = await service.spec_indexes()
        assert isinstance(indexes, list)


@pytest.mark.asyncio
async def test_spec_search_service_mapping(setting: BigGoMCPSetting):
    service = SpecSearchService(setting)
    async with service.session():
        indexes = await service.spec_indexes()
        mapping = await service.spec_mapping(indexes[0])
        assert isinstance(mapping, SpecMappingRet)


@pytest.mark.asyncio
async def test_spec_search_service_search(setting: BigGoMCPSetting):
    service = SpecSearchService(setting)
    async with service.session():
        indexes = await service.spec_indexes()
        hits = await service.search(indexes[0], {"query": {"match_all": {}}})
        assert isinstance(hits, list)

        with pytest.raises(ValueError):
            await service.search(indexes[0], {
                "query": {
                    "match_all": {}
                },
                "size": 11
            })


@pytest.mark.asyncio
async def test_product_search_service(setting: BigGoMCPSetting):
    """Make sure that 'r' link is constructed"""
    service = ProductSearchService(setting)
    ret = await service.search("iphone")
    for product in ret.list:
        assert product.url is not None
        assert product.url.startswith(f"https://{setting.domain.value}")
