import json
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
    async with service.session():
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
) -> Annotated[
        str,
        Field(description="Elasticsearch mappings plus an example document")]:
    """Elasticsearch Mapping For Product Specification"""
    logger.info("spec mapping, index: %s", index)
    setting = get_setting(ctx)
    service = SpecSearchService(setting)
    async with service.session():
        mapping = await service.spec_mapping(index)
    return SpecMappingToolResponse(
        mappings=mapping.mappings,
        example_document=mapping.example_document).slim_dump()


async def spec_search(
    ctx: Context,
    index: Annotated[str,
                     Field(description="""
                          Elasticsearch index

                          Steps to obtain this argument.
                          1. Use 'spec_indexes' tool to get the list of indexes
                          2. Choose the most relevant index
                          """)],
    elasticsearch_query: Annotated[
        str | dict,
        Field(description="""
                          Elasticsearch query

                          Steps to know what to query:
                          1. Use 'spec_indexes' tool to get the list of indexes
                          2. Choose the most relevant index
                          3. Use 'spec_mapping' tool to get the mapping of the index
                          4. Use this tool to query the index

                          Example:
                          ```json
                            {
                                "range": {
                                    "specs.physical_specifications.dimensions.height": {
                                        "gte": 1321,
                                        "lte": 2321
                                    }
                                }
                            }
                          ```
                          """,
              examples=[
                  {
                      "range": {
                          "specs.physical_specifications.dimensions.height": {
                              "gte": 1321,
                              "lte": 2321
                          }
                      }
                  },
              ])],
    size: Annotated[int,
                    Field(description="""
                         Search result size (1 ~ 10)
                         """,
                          ge=1,
                          le=10)] = 5,
) -> str:
    """Product Specification Search. 

    YOU MUST KNOW THE MAPPING OF THE INDEX BEFORE USING THIS TOOL.
    Use 'spec_mapping' tool to get the mapping of the index.
    """
    logger.info("spec search, index: %s, query: %s, size: %s", index,
                elasticsearch_query, size)
    setting = get_setting(ctx)
    service = SpecSearchService(setting)
    async with service.session():
        if isinstance(elasticsearch_query, str):
            query = json.loads(elasticsearch_query)
        else:
            query = elasticsearch_query
        hits = await service.search(index, query, size)
    return SpecSearchToolResponse(hits=hits).slim_dump()
