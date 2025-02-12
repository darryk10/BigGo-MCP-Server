from pydantic import RootModel


class SpecIndexesAPIRet(RootModel):
    root: list[str]


class SpecMappingAPIRet(RootModel):
    root: dict


class SpecSearchAPIRet(RootModel):
    root: list[dict]
