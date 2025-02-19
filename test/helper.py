import pytest
from os import environ
from biggo_mcp_server.types.setting import BigGoMCPSetting

ES_PROXY_URL = environ.get(
    "ES_PROXY_URL", "https://api.d.cloud.biggo.com/api/v1/mcp-es-proxy/")
AUTH_TOKEN_URL = environ.get(
    "AUTH_TOKEN_URL", "https://api-auth.dev.cloud.biggo.com/auth/v1/token")

CLIENT_ID = environ.get("CLIENT_ID", None)
CLIENT_SECRET = environ.get("CLIENT_SECRET", None)


@pytest.fixture
def setting():
    setting = BigGoMCPSetting(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              es_proxy_url=ES_PROXY_URL,
                              auth_token_url=AUTH_TOKEN_URL,
                              es_verify_certs=False,
                              auth_verify_certs=False)
    return setting
