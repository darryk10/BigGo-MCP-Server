from biggo_mcp_server.types.api_ret.product_search import ListItem, ProductSearchAPIRet
from biggo_mcp_server.types.setting import Domains


def test_construct_r_link():
    data = ProductSearchAPIRet(list=[
        ListItem(
            oid="123",
            title="test",
            price=100,
            affurl="/r/some-path",
        )
    ])

    data.construct_r_link(Domains.TW)
    assert data.list[0].affurl is None
    assert data.list[0].url is not None
    assert data.list[0].url == f"https://biggo.com.tw/r/some-path"
