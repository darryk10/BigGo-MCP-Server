from pydantic import BaseModel
import base64
import requests


class _AuthTokenResp(BaseModel):
    access_token: str


def get_access_token(
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

    resp = requests.post(
        url=endpoint,
        headers=headers,
        params=params,
    )
    if resp.status_code >= 400:
        msg = f"get access token error, {resp.text}"
        raise ValueError(msg)

    data = resp.json()
    parsed_data = _AuthTokenResp.model_validate(data)

    return parsed_data.access_token
