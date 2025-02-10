from logging import getLogger
from ..types.setting import LOG_LEVEL_CHOICES

logger = getLogger(__name__)


def setup_logging(log_level: LOG_LEVEL_CHOICES = "INFO"):
    logger = getLogger("biggo_mcp_server")
    logger.setLevel(log_level)
    msg = "BigGo MCP Server logging setup, log_level: %s"
    match log_level:
        case "DEBUG":
            logger.debug(msg, log_level)
        case "INFO":
            logger.info(msg, log_level)
        case "WARNING":
            logger.warning(msg, log_level)
        case "ERROR":
            logger.error(msg, log_level)
        case "CRITICAL":
            logger.critical(msg, log_level)
