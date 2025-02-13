import pytest
from os import environ
from biggo_mcp_server.types.setting import BigGoMCPSetting

ES_PROXY_URL = environ.get("ES_PROXY_URL", "http://localhost:8888")


@pytest.fixture
def setting():
    setting = BigGoMCPSetting()
    setting.es_proxy_url = ES_PROXY_URL
    return setting
