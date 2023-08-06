import asyncio
import aiohttp

from auth import Auth
from api import AmeritradeAPI
from token_manager import TokenManager
from helpers import Ameritrade


async def main():
    async with aiohttp.ClientSession() as session:
        token_manager = TokenManager(consumer_key="ROTH_TRADER2@AMER.OAUTHAP")
        await token_manager.fetch_access_token()

        auth = Auth(session, "https://api.tdameritrade.com/v1", token_manager)

        api = AmeritradeAPI(auth)

        amtd = Ameritrade(api)

        try:
            print(await api.async_get_accounts("789090218"))
        except Exception as e:
            print(e)

try:
    asyncio.run(main())
except RuntimeError:
    print("done")
