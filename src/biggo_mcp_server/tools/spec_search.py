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
    try:
        async with service.session():
            mapping = await service.spec_mapping(index)
    except Exception as e:
        raise Exception(
            f"You must know the available indexes before using this tool. Error: {e}"
        )
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
        dict,
        Field(description="""
              Elasticsearch query

              Size must be less than or equal to 10.
              """,
              examples=[{
                  "query": {
                      "range": {
                          "specs.physical_specifications.dimensions.height": {
                              "gte": 1321,
                              "lte": 2321
                          }
                      }
                  },
                  "size":
                      5,
                  "sort": [{
                      "specs.physical_specifications.dimensions.height": "asc"
                  }]
              }])],
) -> str:
    """Product Specification Search. 

    Use 'spec_mapping' tool to get the mapping of the index.
    """
    logger.info("spec search, index: %s, query: %s", index, elasticsearch_query)

    setting = get_setting(ctx)
    service = SpecSearchService(setting)
    try:
        async with service.session():
            hits = await service.search(index, elasticsearch_query)
    except Exception as e:
        raise Exception(
            f"You must know the mapping of the index before using this tool. Error: {e}"
        )
    return SpecSearchToolResponse(hits=hits).slim_dump()
