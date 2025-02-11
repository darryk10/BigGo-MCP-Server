from logging import getLogger
from .tools import (
    price_history_graph,
    price_history_with_history_id,
    price_history_with_url,
    product_search,
    spec_indexes,
    spec_mapping,
    spec_search,
)
from .log import setup_logging
from ..types.setting import BigGoMCPSetting
from .server import BigGoMCPServer

logger = getLogger(__name__)


async def create_server(setting: BigGoMCPSetting) -> BigGoMCPServer:
    server = BigGoMCPServer(setting)
    setup_logging(setting.log_level)

    # Product Search
    server.add_tool(product_search)

    # Price History
    server.add_tool(price_history_graph)
    server.add_tool(price_history_with_history_id)
    server.add_tool(price_history_with_url)

    # Spec Search
    server.add_tool(spec_indexes)
    server.add_tool(spec_mapping)
    server.add_tool(spec_search)

    return server
