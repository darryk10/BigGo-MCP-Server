from enum import StrEnum
from pydantic import BaseModel


class GraphLanguage(StrEnum):
    TW = "tw"
    EN = "en"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Regions(StrEnum):
    ID = "ID"
    VN = "VN"
    TH = "TH"
    PH = "PH"
    MY = "MY"
    IN = "IN"
    US = "US"
    TW = "TW"
    HK = "HK"
    JP = "JP"
    SG = "SG"


class Domains(StrEnum):
    ID = "biggo.id"
    VN = "vn.biggo.com"
    TH = "biggo.co.th"
    PH = "ph.biggo.com"
    MY = "my.biggo.com"
    IN = "biggo.co.in"
    US = "biggo.com"
    TW = "biggo.com.tw"
    HK = "biggo.hk"
    JP = "biggo.jp"
    SG = "biggo.sg"


REGION_DOMAIN_MAP: dict[Regions, Domains] = {
    Regions.ID: Domains.ID,
    Regions.VN: Domains.VN,
    Regions.TH: Domains.TH,
    Regions.PH: Domains.PH,
    Regions.MY: Domains.MY,
    Regions.IN: Domains.IN,
    Regions.US: Domains.US,
    Regions.TW: Domains.TW,
    Regions.HK: Domains.HK,
    Regions.JP: Domains.JP,
    Regions.SG: Domains.SG,
}


class BigGoMCPSetting(BaseModel):
    """
    BigGo MCP Server settings
    """

    client_id: str | None = None
    client_secret: str | None = None

    region: Regions = Regions.TW

    log_level: LogLevel = LogLevel.INFO

    es_proxy_url: str = "https://mcp-es-proxy.d.cloud.biggo.com"
    es_verify_certs: bool = True

    auth_token_url: str = "https://api.biggo.com/auth/v1/token"

    @property
    def domain(self) -> Domains:
        return REGION_DOMAIN_MAP[self.region]

    @property
    def graph_language(self) -> GraphLanguage:
        if self.region == Regions.TW:
            return GraphLanguage.TW
        else:
            return GraphLanguage.EN
