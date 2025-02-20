import pytest
from os import environ, path
from pathlib import Path
from dotenv import load_dotenv
from biggo_mcp_server.types.setting import BigGoMCPSetting

def load_env_files():
    # 嘗試載入測試環境變數
    test_env_paths = [
        Path(__file__).parent / '.env.test',  # test/.env.test
        Path(__file__).parent.parent / '.env.test',  # .env.test
    ]

    for env_path in test_env_paths:
        if env_path.exists():
            load_dotenv(str(env_path))  # Python 3.10 需要轉換為字串
            return True
    return False

# 確保環境變數被載入
load_env_files()

ES_PROXY_URL = environ.get("ES_PROXY_URL",
                           "https://api.biggo.com/api/v1/mcp-es-proxy/")
AUTH_TOKEN_URL = environ.get("AUTH_TOKEN_URL",
                             "https://api.biggo.com/auth/v1/token")

CLIENT_ID = environ.get("CLIENT_ID", None)
CLIENT_SECRET = environ.get("CLIENT_SECRET", None)


@pytest.fixture
def setting():
    client_id = environ.get("BIGGO_MCP_SERVER_CLIENT_ID")
    client_secret = environ.get("BIGGO_MCP_SERVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError(
            "Environment variables BIGGO_MCP_SERVER_CLIENT_ID and BIGGO_MCP_SERVER_CLIENT_SECRET must be set. "
            "Please check if .env.test exists and contains the correct values."
        )
    
    setting = BigGoMCPSetting(
        client_id=client_id,
        client_secret=client_secret,
    )
    return setting
