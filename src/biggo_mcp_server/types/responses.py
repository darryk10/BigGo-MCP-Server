from pydantic import BaseModel

from .api_ret.price_history import PriceHistoryAPIRet

from .api_ret.product_search import ProductSearchAPIRet


class BaseToolResponse(BaseModel):

    def slim_dump(self) -> str:
        return self.model_dump_json(exclude_none=True)


class ProductSearchToolResponse(BaseToolResponse):
    product_search_result: ProductSearchAPIRet


class PriceHisotryGraphToolResponse(BaseToolResponse):
    price_history_graph: str


class PriceHisotryWithHistoryIDToolResponse(BaseToolResponse):
    price_hisotry_description: PriceHistoryAPIRet
    price_history_graph: str


class PriceHisotryWithURLToolResponse(PriceHisotryWithHistoryIDToolResponse):
    pass
