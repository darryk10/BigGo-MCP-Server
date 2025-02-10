from logging import getLogger
import requests

from .utils import get_nindex_from_url, get_pid_from_url

from ..types.price_history_ret import PriceHistoryAPIRet

logger = getLogger(__name__)


def get_price_history(history_id: str, days: int) -> PriceHistoryAPIRet | None:
    url = "https://extension.biggo.com/api/product_price_history.php"
    body = {"item": [history_id], "days": days}

    logger.debug("call price history, body: %s", body)

    resp = requests.get(url, json=body)
    if resp.status_code >= 400:
        err_msg = f"price history api error: {resp.text}"
        logger.error(err_msg)
        raise ValueError(err_msg)

    if resp.json().get("result") == False:
        return None
    else:
        return PriceHistoryAPIRet.model_validate_json(resp.text)


def get_history_id(nindex: str, pid: str) -> str:
    return f"{nindex}-{pid}"


def get_price_history_with_url(days: int,
                               url: str) -> PriceHistoryAPIRet | None:
    if (nindex := get_nindex_from_url(url)) is None:
        logger.warning("nindex not found, url: %s", url)
        return

    if (pid := get_pid_from_url(nindex=nindex, url=url)) is None:
        logger.warning("product id not found, nindex: %s, url: %s", nindex, url)
        return

    history_id = get_history_id(nindex=nindex, pid=pid)
    resp = get_price_history(history_id=history_id, days=days)

    if resp is None and nindex in ["tw_mall_shopeemall", "tw_bid_shopee"]:
        nindex = "tw_mall_shopeemall" if nindex == "tw_bid_shopee" else "tw_mall_shopeemall"
        history_id = get_history_id(nindex=nindex, pid=pid)
        resp = get_price_history(
            history_id=history_id,
            days=days,
        )

    return resp
