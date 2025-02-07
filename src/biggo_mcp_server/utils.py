import base64
from dataclasses import dataclass
from aiohttp import ClientSession
from pydantic import BaseModel


@dataclass(slots=True)
class NindexOID:
    nindex: str
    oid: str


def get_nindex_oid(inpt: str) -> NindexOID:
    """
    Arguments:
    - inpt: structure <nindex>-<oid>
    """
    temp = inpt.split("-", maxsplit=1)
    return NindexOID(nindex=temp[0], oid=temp[1])


class _AuthTokenResp(BaseModel):
    access_token: str


async def get_access_token(
        client_id: str,
        client_secret: str,
        endpoint: str = "https://api.biggo.com/auth/v1/token") -> str:
    """Get access token with client credentials"""

    params = {
        "grant_type": "client_credentials",
    }
    credentials = f"{client_id}:{client_secret}".encode()
    authorization = base64.b64encode(credentials).decode()
    headers = {
        "Authorization": f"Basic {authorization}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with ClientSession() as session:
        async with session.post(
                url=endpoint,
                headers=headers,
                params=params,
        ) as resp:
            if resp.status >= 400:
                msg = f"get access token error, {await resp.text()}"
                raise ValueError(msg)

            data = await resp.json()
            parsed_data = _AuthTokenResp.model_validate(data)

    return parsed_data.access_token
