import argparse
import asyncio
from logging import getLogger
from .types.setting import BigGoMCPSetting, LogLevel, Regions
from .lib.server_setup import create_server
from dataclasses import dataclass

logger = getLogger(__name__)


@dataclass()
class Args:
    region: Regions
    client_id: str | None
    client_secret: str | None
    log_level: LogLevel
    es_proxy_url: str


async def start():
    args = argparse.ArgumentParser()
    args.add_argument("--region",
                      type=Regions,
                      choices=Regions,
                      default=Regions.TW)
    args.add_argument("--client-id", type=str, default=None)
    args.add_argument("--client-secret", type=str, default=None)
    args.add_argument("--log-level",
                      type=LogLevel,
                      choices=LogLevel,
                      default=LogLevel.INFO)
    args.add_argument("--es-proxy-url",
                      type=str,
                      default="http://es-proxy.d.cloud.biggo.com")
    args = args.parse_args(namespace=Args)

    setting = BigGoMCPSetting(
        region=args.region,
        client_id=args.client_id,
        client_secret=args.client_secret,
        log_level=args.log_level,
        es_proxy_url=args.es_proxy_url,
    )

    logger.info("Starting BigGo MCP Server with setting: %s", setting)

    server = await create_server(setting)
    await server.run_stdio_async()


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
