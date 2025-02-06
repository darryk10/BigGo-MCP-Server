from logging import getLogger
from typing import Annotated, Literal
from mcp.server.fastmcp import FastMCP
from pydantic import Field
import requests

server = FastMCP("BigGo MCP Server")

logger = getLogger(__name__)


@server.tool()
def product_search(
    query: Annotated[
        str, Field(description="Search query", examples=["iphone", "護唇膏"])]
) -> str:
    """Product Search"""

    logger.info("product search, query: %s", query)

    url = f"https://biggo.com.tw/api/v1/spa/search/{query}/product?group=gp"
    logger.debug("product search, url: %s", url)

    resp = requests.get(url)
    if resp.status_code >= 400:
        err_msg = f"product search api error: {resp.text}"
        logger.error(err_msg)
        raise ValueError(err_msg)

    result = resp.json()
    logger.debug("product search result: %s", result)
    return result


@server.tool()
async def ec_list() -> str:
    """Get EC List
    This includes 'provide' that can be used in combination with 'oid'
    to create the currect 'item' structure for price history search
    """

    logger.info("get ec list")

    url = "https://biggo.com.tw/app/provide2sitetype.php"

    resp = requests.get(url)
    if resp.status_code >= 400:
        err_msg = f"ec list api error: {resp.text}"
        logger.error(err_msg)
        raise ValueError(err_msg)

    result = resp.json()
    logger.debug("ec list result: %s", result)
    return result


@server.tool()
async def price_history(
    item: Annotated[
        str,
        Field(description=
              """Product to search for. The structure is <provide>-<oid>""",
              examples=["tw_pmall_rakuten-nwdsl_6MONJRBOO"])],
    days: Annotated[Literal["days90", "days180", "days365", "days730"],
                    Field(description="History range")],
) -> str:
    """Product Price History"""

    logger.info("price history, item: %s, days: %s", item, days)

    days_number = int(days.lstrip("days"))
    url = "https://extension.biggo.com/api/product_price_history.php"
    body = {"item": [item], "days": days_number}

    logger.info("call price history, body: %s", body)

    resp = requests.get(url, json=body)
    if resp.status_code >= 400:
        err_msg = f"price history api error: {resp.text}"
        logger.error(err_msg)
        raise ValueError(err_msg)

    result = resp.json()
    logger.debug("price history result: %s", result)
    return result
