"""
Just check if the tools can be called without errors.
"""

from biggo_mcp_server.server import price_history_graph, price_history_with_history_id, price_history_with_url, product_search
import pytest


@pytest.mark.asyncio
async def test_get_history():
    history = await price_history_with_history_id(
        history_id="tw_pmall_rakuten-nwdsl_6MONJRBOO",
        days="90",
        language="tw",
    )
    assert isinstance(history, str)


@pytest.mark.asyncio
async def test_get_history_with_url():
    history = await price_history_with_url(
        url="https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=13660781",
        days="90",
        language="tw",
    )
    assert isinstance(history, str)


@pytest.mark.asyncio
async def test_product_search():
    search = await product_search(query="iphone")
    assert isinstance(search, str)


def test_price_history_graph():
    search = price_history_graph(
        history_id="tw_pmall_rakuten-nwdsl_6MONJRBOO",
        language="tw",
    )
    assert isinstance(search, str)
