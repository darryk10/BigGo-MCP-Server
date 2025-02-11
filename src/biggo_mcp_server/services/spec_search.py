from ..types.setting import BigGoMCPSetting


class SpecSearchService:

    def __init__(self, setting: BigGoMCPSetting):
        self._setting = setting

    async def spec_indexes(self) -> list[str]:
        ...

    async def spec_mapping(self, index: str) -> dict:
        ...

    async def search(self, index: str, query: str):
        ...
