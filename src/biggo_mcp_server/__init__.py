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


async def start():
    args = argparse.ArgumentParser()
    args.add_argument("--region",
                      type=Regions,
                      choices=Regions,
                      default=Regions.US)
    args.add_argument("--client-id", type=str, default=None)
    args.add_argument("--client-secret", type=str, default=None)
    args.add_argument("--log-level",
                      type=LogLevel,
                      choices=LogLevel,
                      default=LogLevel.INFO)
    args = args.parse_args(namespace=Args)

    setting = BigGoMCPSetting(
        region=args.region,
        client_id=args.client_id,
        client_secret=args.client_secret,
        log_level=args.log_level,
    )

    logger.info("Starting BigGo MCP Server with setting: %s", setting)

    server = await create_server(setting)
    await server.run_stdio_async()


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
