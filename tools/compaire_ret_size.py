"""
== product_search_api_ret ==
Original length: 65571, Cleaned length: 23112.
        Current Percentage = (35.24728919796861)%
        Original / Cleaned = 2.837097611630322

== ec_list_api_ret ==
Original length: 222499, Cleaned length: 22023.
        Current Percentage = (9.898022013582084)%
        Original / Cleaned = 10.10302865186396

== Total length comparison ==
Removed tools: 
    - ec_list
Original length: 288070, Cleaned length: 23112.
        Current Percentage = (8.023049953136391)%
        Original / Cleaned = 12.464087919695396
"""
from dataclasses import dataclass
from biggo_mcp_server.types.ec_list_ret import ECListAPIRet
from biggo_mcp_server.types.product_search_ret import ProductSearchAPIRet


@dataclass(slots=True)
class Statistics:
    original: int
    cleaned: int


def print_length_comparison(original: int, cleaned: int):
    print(f"""Original length: {original}, Cleaned length: {cleaned}. 
        Current Percentage = ({(cleaned/original) * 100})%
        Original / Cleaned = {original/cleaned}
        """)


def product_search_api_ret() -> Statistics:
    print("== product_search_api_ret ==")
    # original response
    with open("./data/original_prod_search_ret.json", "r") as f:
        original = f.read()

    # cleaned
    clean_data = ProductSearchAPIRet.model_validate_json(original)
    clean_data = clean_data.model_dump_json(exclude_none=True)

    # compaire
    print_length_comparison(original=len(original), cleaned=len(clean_data))

    return Statistics(original=len(original), cleaned=len(clean_data))


def ec_list_api_ret() -> Statistics:
    print("== ec_list_api_ret ==")
    # original response
    with open("./data/ec_list_ret.json", "r") as f:
        original = f.read()

    # cleaned
    clean_data = ECListAPIRet.model_validate_json(original)
    clean_data = clean_data.model_dump_json(exclude_none=True)

    # compaire
    print_length_comparison(original=len(original), cleaned=len(clean_data))

    return Statistics(original=len(original), cleaned=len(clean_data))


def main():
    product_search_statistic = product_search_api_ret()
    ec_list_statistic = ec_list_api_ret()

    print("== Total length comparison ==")
    original = product_search_statistic.original + ec_list_statistic.original
    cleaned = product_search_statistic.cleaned  # + ec_list_statistic.cleaned (tool removed)
    print_length_comparison(original=original, cleaned=cleaned)


if __name__ == "__main__":
    main()
