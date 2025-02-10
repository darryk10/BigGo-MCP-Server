"""
Mostly just make sure the tools are working.
"""

from biggo_mcp_server.server import price_history_graph, price_history_with_history_id, price_history_with_url, product_search


def test_get_history():
    history = price_history_with_history_id(
        history_id="tw_pmall_rakuten-nwdsl_6MONJRBOO",
        days="90",
    )
    assert isinstance(history, str)


def test_get_history_with_url():
    history = price_history_with_url(
        url="https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=13660781",
        days="90",
    )
    assert isinstance(history, str)


def test_product_search():
    search = product_search(query="iphone")
    assert isinstance(search, str)


def test_price_history_graph():
    search = price_history_graph(
        history_id="tw_pmall_rakuten-nwdsl_6MONJRBOO",
        language="tw",
    )
    assert isinstance(search, str)
