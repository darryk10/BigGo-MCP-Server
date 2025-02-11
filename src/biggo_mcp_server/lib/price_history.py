from dataclasses import dataclass
from logging import getLogger
from aiohttp import ClientSession
from .utils import get_nindex_from_url, get_nindex_oid, get_pid_from_url
from ..types.api_ret.price_history import PriceHistoryAPIRet

logger = getLogger(__name__)


def gen_price_history_graph_url(history_id: str, language: str) -> str:
    item_info = get_nindex_oid(history_id)
    url = f"https://imbot-dev.biggo.dev/chart?nindex={item_info.nindex}&oid={item_info.oid}&lang={language}"
    return url


async def get_price_history(history_id: str,
                            days: int) -> PriceHistoryAPIRet | None:
    url = "https://extension.biggo.com/api/product_price_history.php"
    body = {"item": [history_id], "days": days}

    logger.debug("call price history, body: %s", body)

    async with ClientSession() as session:
        async with session.post(url=url, json=body) as resp:
            if resp.status >= 400:
                err_msg = f"price history api error: {await resp.text()}"
                logger.error(err_msg)
                raise ValueError(err_msg)

            if (data := await resp.json()).get("result") == False:
                return None
            else:
                return PriceHistoryAPIRet.model_validate(data)


def get_history_id(nindex: str, pid: str) -> str:
    return f"{nindex}-{pid}"


@dataclass(slots=True)
class PriceHistoryWithUrlRet:
    nindex: str
    pid: str
    data: PriceHistoryAPIRet

    @property
    def history_id(self) -> str:
        return get_history_id(nindex=self.nindex, pid=self.pid)


async def get_price_history_with_url(days: int,
                                     url: str) -> PriceHistoryWithUrlRet | None:
    if (nindex := await get_nindex_from_url(url)) is None:
        logger.warning("nindex not found, url: %s", url)
        return

    if (pid := await get_pid_from_url(nindex=nindex, url=url)) is None:
        logger.warning("product id not found, nindex: %s, url: %s", nindex, url)
        return

    history_id = get_history_id(nindex=nindex, pid=pid)
    resp = await get_price_history(history_id=history_id, days=days)

    if resp is None and nindex in ["tw_mall_shopeemall", "tw_bid_shopee"]:
        nindex = "tw_mall_shopeemall" if nindex == "tw_bid_shopee" else "tw_mall_shopeemall"
        history_id = get_history_id(nindex=nindex, pid=pid)
        resp = await get_price_history(
            history_id=history_id,
            days=days,
        )

    if resp is not None:
        return PriceHistoryWithUrlRet(nindex=nindex, pid=pid, data=resp)
