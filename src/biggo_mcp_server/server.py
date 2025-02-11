from logging import getLogger
from typing import Annotated, Literal
from aiohttp import ClientSession
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .types.responses import PriceHisotryGraphToolResponse, PriceHisotryWithHistoryIDToolResponse, ProductSearchToolResponse
from .lib.log import setup_logging
from .types.setting import BigGoMCPSetting
from .lib.price_history import gen_price_history_graph_url, get_price_history, get_price_history_with_url
from .types.api_ret.product_search import ProductSearchAPIRet

logger = getLogger(__name__)

server = FastMCP("BigGo MCP Server")
setting = BigGoMCPSetting()
setup_logging(setting.log_level)


@server.tool()
async def product_search(
    query: Annotated[
        str, Field(description="Search query", examples=["iphone", "護唇膏"])]
) -> str:
    """Product Search"""

    logger.info("product search, query: %s", query)

    url = f"https://biggo.com.tw/api/v1/spa/search/{query}/product"
    logger.debug("product search, url: %s", url)

    async with ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status >= 400:
                err_msg = f"product search api error: {await resp.text()}"
                logger.error(err_msg)
                raise ValueError(err_msg)

            # clean data
            cleaned_data = ProductSearchAPIRet.model_validate(await resp.json())

    return ProductSearchToolResponse(
        product_search_result=cleaned_data).slim_dump()


@server.tool()
def price_history_graph(
    history_id: Annotated[
        str,
        Field(description="""
              Product History ID
              Here are a few steps to obtain this argument.
              1. Use 'product_search' tool to retrive a list of products
              2. Find the most relevant product.
              3. The product should have a field called 'history_id', use it as the value for this argument
              """,
              examples=[
                  "tw_pmall_rakuten-nwdsl_6MONJRBOO", "tw_pec_senao-1363332"
              ])],
    language: Annotated[Literal["tw", "en"],
                        Field(description="Timeline label language")],
) -> str:
    """Link That Visualizes Product Price History"""

    logger.info("price history graph, history_id: %s, language: %s", history_id,
                language)
    url = gen_price_history_graph_url(history_id, language)

    return PriceHisotryGraphToolResponse(
        price_history_graph=f"![Price History Graph]({url})").slim_dump()


@server.tool()
async def price_history_with_history_id(
    history_id: Annotated[
        str,
        Field(description="""
              Product History ID
              Here are a few steps to obtain this argument.
              1. Use 'product_search' tool to retrive a list of products
              2. Find the most relevant product.
              3. The product should have a field called 'history_id', use it as the value for this argument
              """,
              examples=[
                  "tw_pmall_rakuten-nwdsl_6MONJRBOO", "tw_pec_senao-1363332"
              ])],
    days: Annotated[Literal["90", "80", "365", "730"],
                    Field(description="History range")],
    language: Annotated[Literal["tw", "en"],
                        Field(description="Timeline label language")],
) -> str:
    """Product Price History With History ID"""

    logger.info("price history with history id, history_id: %s, days: %s",
                history_id, days)
    resp = await get_price_history(history_id=history_id, days=int(days))
    if resp is None:
        return "No price history found"

    url = gen_price_history_graph_url(history_id, language)

    return PriceHisotryWithHistoryIDToolResponse(
        price_hisotry_description=resp,
        price_history_graph=f"![Price History Graph]({url})").slim_dump()


@server.tool()
async def price_history_with_url(
    days: Annotated[Literal["90", "80", "365", "730"],
                    Field(description="History range")],
    url: Annotated[str, Field(description="Product URL")],
    language: Annotated[Literal["tw", "en"],
                        Field(description="Timeline label language")],
) -> str:
    """Product Price History With URL"""

    logger.info("price history with url, url: %s, days: %s", url, days)
    resp = await get_price_history_with_url(days=int(days), url=url)
    if resp is None:
        return "No price history found"

    url = gen_price_history_graph_url(resp.history_id, language)

    return PriceHisotryWithHistoryIDToolResponse(
        price_hisotry_description=resp.data,
        price_history_graph=f"![Price History Graph]({url})").slim_dump()


@server.tool()
async def spec_indexes(
) -> Annotated[str, Field(description="List of Elasticsearch indexes")]:
    """Elasticsearch Indexes for Product Specification"""
    return "Not implemented"


@server.tool()
async def spec_mapping(
    index: Annotated[str,
                     Field(description="""
                          Elasticsearch index
                          Here are a few steps to obtain this argument.
                          1. Use 'spec_indexes' tool to get the list of indexes
                          2. Choose the most relevant index
                          """)]
) -> Annotated[str, Field(description="Elasticsearch Mappings")]:
    """Elasticsearch Mapping For Product Specification """
    return "Not implemented"


@server.tool()
async def spec_search(
    index: Annotated[str,
                     Field(description="""
                          Elasticsearch index
                          Here are a few steps to obtain this argument.
                          1. Use 'spec_indexes' tool to get the list of indexes
                          2. Choose the most relevant index
                          """)],
    # TODO: add examples
    query: Annotated[str,
                     Field(description="""
                          Elasticsearch query, no need to include the `query` field.
                          Steps to know what to query:
                          1. Use 'spec_indexes' tool to get the list of indexes
                          2. Choose the most relevant index
                          3. Use 'spec_mapping' tool to get the mapping of the index
                          4. Use this tool to query the index
                          """)],
) -> str:
    """Product Specification Search"""
    return "Not implemented"
