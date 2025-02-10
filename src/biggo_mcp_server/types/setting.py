from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_LEVEL_CHOICES = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BigGoMCPSetting(BaseSettings):
    """
    BigGo MCP Server settings

    All settings can be configured via environment variables with the prefix BIGGO_MCP_.
    For example, BIGGO_MCP_LOG_LEVEL=DEBUG will set log_level to DEBUG.
    """
    model_config = SettingsConfigDict(env_prefix="BIGGO_MCP_")

    client_id: str | None = None
    client_secret: str | None = None

    log_level: LOG_LEVEL_CHOICES = "INFO"
