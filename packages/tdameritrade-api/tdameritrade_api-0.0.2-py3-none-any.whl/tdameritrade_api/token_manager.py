import yaml
import os
import json

from datetime import datetime, timedelta

from aiohttp import ClientSession, ClientResponse


class TokenManager:
    def __init__(self, consumer_key=None):
        """Initialize the Token Manager."""
        self.access_token = None
        self.access_expires = None
        self.refresh_token = None
        self.refresh_expires = None
        self.access_aquired = None
        self.refresh_aquired = None
        self.consumer_key = consumer_key
        self.cache_location = os.path.join(os.getcwd(), "ameritrade.yaml")

    async def fetch_access_token(self):
        try:
            with open(self.cache_location) as file:
                token_info = yaml.full_load(file)

            self.access_token = token_info["access_token"]
            self.access_expires = token_info["access_expires"]
            self.refresh_token = token_info["refresh_token"]
            self.refresh_expires = token_info["refresh_expires"]
            self.access_aquired = token_info["access_aquired"]
            self.refresh_aquired = token_info["refresh_aquired"]

            if not await self.is_token_valid():
                await self.refresh_access_token()
        except FileNotFoundError:
            await self.refresh_access_token()
            return

    async def save_access_token(self):
        with open(self.cache_location, "w") as file:
            yaml.dump(
                {
                    "access_token": self.access_token,
                    "access_expires": self.access_expires,
                    "refresh_token": self.refresh_token,
                    "refresh_expires": self.refresh_expires,
                    "access_aquired": self.access_aquired,
                    "refresh_aquired": self.refresh_aquired,
                },
                file,
            )

    async def is_token_valid(self):
        if await self.is_token_expired():
            return False
        return True

    async def is_token_expired(self):
        if not self.access_expires or not self.access_aquired:
            return True

        if datetime.now() > (
            self.access_aquired + timedelta(seconds=int(self.access_expires))
        ):
            return True
        return False

    async def is_refresh_token_valid(self):
        if datetime.now() < (
            self.refresh_aquired + timedelta(seconds=int(self.refresh_expires))
        ):
            return True
        return False

    async def refresh_access_token(self):
        """Get a token."""
        websession = ClientSession()
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "grant_type": "refresh_token",
            "client_id": self.consumer_key,
            "refresh_token": self.refresh_token,
            "redirect_uri": "http://localhost",
        }

        resp = await websession.request(
            "post",
            "https://api.tdameritrade.com/v1/oauth2/token",
            data=data,
            headers=headers,
        )
        txt_res = await (resp.text())

        json_res = json.loads(txt_res)

        self.access_aquired = datetime.now()
        self.access_token = json_res["access_token"]
        self.access_expires = json_res["expires_in"]

        await self.save_access_token()
