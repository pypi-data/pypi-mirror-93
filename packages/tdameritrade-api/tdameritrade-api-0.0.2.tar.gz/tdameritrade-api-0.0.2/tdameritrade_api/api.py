from .auth import Auth


class AmeritradeAPI:
    """Class to communicate with the Ameritrade API."""

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_account(self, account_id):
        """Return the account details"""
        resp = await self.auth.request("get", f"/accounts/{account_id}")
        resp.raise_for_status()
        return await resp.json()

    async def async_get_quote(self, ticker):
        """Return a quote for a specified ticker"""
        resp = await self.auth.request("get", f"/marketdata/{ticker}/quotes")
        resp.raise_for_status()
        return await resp.json()

    async def async_get_market_hours(self, market):
        """Return the status of specified market"""
        resp = await self.auth.request("get", f"/marketdata/{market}/hours")
        resp.raise_for_status()
        return await resp.json()

    async def async_get_orders(self, account_id):
        """Return current orders for the specified account"""
        resp = await self.auth.request("get", f"/accounts/{account_id}/orders")
        resp.raise_for_status()
        return await resp.json()

    async def async_place_order(
        self,
        price,
        instruction,
        quantity,
        symbol,
        account_id,
        order_type="LIMIT",
        session="NORMAL",
        duration="DAY",
        orderStrategyType="SINGLE",
        assetType="EQUITY",
    ):
        """Place an order"""
        data = {
            "orderType": order_type,
            "price": price,
            "session": session,
            "duration": duration,
            "orderStrategyType": orderStrategyType,
            "orderLegCollection": [
                {
                    "instruction": instruction,
                    "quantity": quantity,
                    "instrument": {"symbol": symbol, "assetType": assetType},
                }
            ],
        }
        resp = await self.auth.request(
            "post", f"/accounts/{account_id}/orders", json=data
        )
        resp.raise_for_status()

        return True
