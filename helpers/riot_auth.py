import re
import ssl
from collections import OrderedDict
from typing import Callable

import requests
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager


class RiotAuth:
    def __init__(self, username: str, password: str, twofa_callback: Callable[..., None] = lambda x: None) -> None:
        self.username = username
        self.password = password
        self.twofa_callback = twofa_callback

    def authenticate(self) -> tuple[str, OrderedDict[str, str]]:
        class SSLAdapter(HTTPAdapter):
            def init_poolmanager(self, connections: int, maxsize: int, block: bool = False):
                self.poolmanager = PoolManager(
                    num_pools=connections,
                    maxsize=maxsize,
                    block=block,
                    ssl_version=ssl.PROTOCOL_TLSv1_2,
                )

        auth_endpoint = "https://auth.riotgames.com/api/v1/authorization"

        # Set cookies

        data = {
            "client_id": "play-valorant-web-prod",
            "nonce": "1",
            "redirect_uri": "https://playvalorant.com/opt_in",
            "response_type": "token id_token",
        }

        headers = OrderedDict(
            {
                "Accept-Encoding": "gzip, deflate, br",
                "Host": "auth.riotgames.com",
                "User-Agent": "RiotClient/43.0.1.4195386.4190634 rso-auth (Windows; 10;;Professional, x64)",
            }
        )

        session = requests.session()
        session.mount(auth_endpoint, SSLAdapter())
        session.headers = headers  # type: ignore
        res = session.post(auth_endpoint, json=data, headers=headers)

        # Get token

        data = {
            "type": "auth",
            "username": self.username,
            "password": self.password,
        }

        res = session.put(auth_endpoint, json=data, headers=headers)
        res_json = res.json()

        if res_json["error"] == "auth_error":
            raise ValueError("Your username or password may be incorrect!")
        elif res_json["type"] == "multifactor":
            twofa_code = input("Input 2FA Code: ")
            data = {
                "type": "multifactor",
                "code": twofa_code,
                "rememberDevice": False,
            }
            res = session.put(auth_endpoint, json=data, headers=headers)

            if res.json()["error"] == "multifactor_attempt_failed":
                raise ValueError("Please enter correct 2fa code.")

        pattern = re.compile(
            r"access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)"
        )
        data = pattern.findall(res.json()["response"]["parameters"]["uri"])[0]
        access_token = data[0]

        # Get entitlement

        headers = OrderedDict(
            {
                "Accept-Encoding": "gzip, deflate, br",
                "Host": "entitlements.auth.riotgames.com",
                "User-Agent": "RiotClient/43.0.1.4195386.4190634 rso-auth (Windows; 10;;Professional, x64)",
                "Authorization": f"Bearer {access_token}",
            }
        )

        res = session.post("https://entitlements.auth.riotgames.com/api/token/v1", json={}, headers=headers)
        entitlements_token = res.json()["entitlements_token"]

        # Get PUUID

        headers = OrderedDict(
            {
                "Accept-Encoding": "gzip, deflate, br",
                "Host": "auth.riotgames.com",
                "User-Agent": "RiotClient/43.0.1.4195386.4190634 rso-auth (Windows; 10;;Professional, x64)",
                "Authorization": f"Bearer {access_token}",
            }
        )

        res = session.post("https://auth.riotgames.com/userinfo", json={}, headers=headers)
        user_id: str = res.json()["sub"]

        session.close()

        # Update headers

        headers["X-Riot-Entitlements-JWT"] = entitlements_token
        del headers["Host"]

        return user_id, headers

    def __repr__(self) -> str:
        return f"RiotAuth(username: {self.username})"


# if __name__ == "__main__":
#     try:
#         auth = RiotAuth().authenticate()
#         print(auth[0])
#     except ValueError as e:
#         print(e)
