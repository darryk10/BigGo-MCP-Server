from logging import getLogger
from typing import Annotated
from mcp.server.fastmcp import Context
from pydantic import Field
from ..types.responses import SpecIndexesToolResponse, SpecMappingToolResponse, SpecSearchToolResponse
from ..lib.utils import get_setting
from ..services.spec_search import SpecSearchService

logger = getLogger(__name__)


async def spec_indexes(
    ctx: Context,
) -> Annotated[str, Field(description="List of Elasticsearch indexes")]:
    """Elasticsearch Indexes for Product Specification"""
    logger.info("spec indexes")
    setting = get_setting(ctx)
    service = SpecSearchService(setting)
    indexes = await service.spec_indexes()
    return SpecIndexesToolResponse(indexes=indexes).slim_dump()


async def spec_mapping(
    ctx: Context,
    index: Annotated[str,
                     Field(description="""
                          Elasticsearch index
                          Steps to obtain this argument.
                          1. Use 'spec_indexes' tool to get the list of indexes
                          2. Choose the most relevant index
                          """)],
) -> Annotated[str, Field(description="Elasticsearch Mappings")]:
    """Elasticsearch Mapping For Product Specification """
    logger.info("spec mapping, index: %s", index)
    setting = get_setting(ctx)
    service = SpecSearchService(setting)
    mapping = await service.spec_mapping(index)
    return SpecMappingToolResponse(mapping=mapping).slim_dump()


async def spec_search(
    ctx: Context,
    index: Annotated[str,
                     Field(description="""
                          Elasticsearch index
                          Steps to obtain this argument.
                          1. Use 'spec_indexes' tool to get the list of indexes
                          2. Choose the most relevant index
                          """)],
    query: Annotated[str,
                     Field(description="""
                          Elasticsearch query, no need to include the `query` field.
                          Steps to know what to query:
                          1. Use 'spec_indexes' tool to get the list of indexes
                          2. Choose the most relevant index
                          3. Use 'spec_mapping' tool to get the mapping of the index
                          4. Use this tool to query the index
                          5. If the mapping has 'region' related fields, 
                             use 'get_current_region' tool to get the current region
                             and apply it in the query. Regions are in lowercase.
                          """)],
    size: Annotated[int,
                    Field(description="""
                         Search result size (1 ~ 1000)
                         """,
                          ge=1,
                          le=1000)],
) -> str:
    """Product Specification Search"""
    logger.info("spec search, index: %s, query: %s, size: %s", index, query,
                size)
    setting = get_setting(ctx)
    service = SpecSearchService(setting)
    documents = await service.search(index, query, size)
    return SpecSearchToolResponse(documents=documents).slim_dump()
