class SpecSearch:

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    async def prepare(self):
        # get access token
        # connect to elasticsearch
        pass

    async def get_index_list(self):
        pass

    async def get_mapping(self, index: str):
        pass

    async def search(self, index: str, query: str):
        pass
