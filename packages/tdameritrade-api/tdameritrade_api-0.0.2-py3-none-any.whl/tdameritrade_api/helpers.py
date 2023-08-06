from .api import AmeritradeAPI


class Ameritrade:
    def __init__(self, api: AmeritradeAPI):
        """Initialize the Ameritrade class and store the api."""
        self.api = api

    async def async_get_available_funds(self, account_id):
        res = await self.api.async_get_account(account_id)
        return res["securitiesAccount"]["currentBalances"]["availableFunds"]

    async def async_is_market_open(self):
        res = await self.api.async_get_market_hours("EQUITY")
        return res["equity"]["equity"]["isOpen"]
