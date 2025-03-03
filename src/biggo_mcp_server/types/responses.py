from typing_extensions import Self
from pydantic import BaseModel, model_validator
from .api_ret.price_history import PriceHistoryAPIRet
from .api_ret.product_search import ProductSearchAPIRet


class BaseToolResponse(BaseModel):

    def slim_dump(self) -> str:
        return self.model_dump_json(exclude_none=True)


class ProductSearchToolResponse(BaseToolResponse):
    product_search_result: ProductSearchAPIRet
    reason: str | None = None
    display_rules: str | None = None

    @model_validator(mode='after')
    def post_init(self) -> Self:
        if len(self.product_search_result.list) == 0:
            self.reason = """
No results found. Possible reasons:
1. This search is much more complex than a simple product search.
2. The user is asking things related to product specifications.

If the problems might be related to the points listed above,
please use the 'spec_search' tool and try again.
            """
            return self

        # add display rules if result is not empty
        else:
            self.display_rules = """
As a product researcher, you need to find the most relavent product and present them in utmost detail.
Without following the rules listed bellow, the output will become useless, you must follow the rules before responding to the user.
All rules must be followed strictly.

Here are a list of rules you must follow:
Rule 1: Images must be included, plain text is not enough.
Rule 2: Product urls must be included so that the user can by the product with a simple click if possible.
Rule 3: Display more then one relavent product if possible, having multiple choices is a good thing.
            """

        return self


class PriceHisotryGraphToolResponse(BaseToolResponse):
    price_history_graph: str
    display_rules: str = """
This is a markdown image link, it must be included in the final output. 
    """


class PriceHistoryToolResponse(BaseToolResponse):
    price_history_description: PriceHistoryAPIRet
    price_history_graph: str
    display_rules: str = """
Field explanation:
'price_history_description': includes detailed price history info.
'price_history_graph': includes a markdown image link used for visualizing price history.

Here are a list of rules you must follow:
Rule 1: Both 'price_history_description' and the link provided at 'price_history_graph' field must be included in the output.
    """


class SpecIndexesToolResponse(BaseToolResponse):
    indexes: list[str]


class SpecMappingToolResponse(BaseToolResponse):
    mappings: dict
    example_document: dict
    note: str = """
Specifications are under the 'specs' field
Example fields paths:
- specs.physical_specs.weight
- specs.technical_specs.water_resistance.depth
- specs.sensors.gyroscope
"""


class SpecSearchToolResponse(BaseToolResponse):
    hits: list[dict]
    reason: str | None = None
    display_rules: str | None = None

    @model_validator(mode='after')
    def post_init(self) -> Self:
        if len(self.hits) == 0:
            self.reason = """
No results found. Possible reasons:
1. You have no clue about the mapping.
2. You have not used the 'spec_mapping' tool to get the mapping of the index.

Do you really know what you are doing?
You MUST think about this before you tell the user that no results are found.
You MUST be ABSOLUTELY sure that you understand the mapping of the index, and that the
search criteria is correct, and that there is TRULY no result.

If you have any doubt, please use the 'spec_mapping' tool to get the mapping of the index,
and try again.
The 'spec_mapping' tool will give you the mapping of the index, and an example document.
'spec_mapping' is the only way to understand the mapping of the index.
It is the best tool to use before you search the index.
            """

        else:
            self.display_rules = """
Rules that must be followed when presenting this data.
Without following the rules listed bellow, the output will become useless, you must follow the rules before responding to the user.
All rules must be followed strictly.

Here are a list of rules you must follow:
Rule 1: Product image must be included.
Rule 2: Display more then one relavent product if possible.
            """

        return self
