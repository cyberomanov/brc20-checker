import asyncio
import json

import httpx
from loguru import logger

from datatypes import ExplorerResponse


async def get_btc_balance(address: str, client: httpx.AsyncClient) -> ExplorerResponse:
    four_two_nine_sleep = 5
    while True:
        url = f"https://api.blockchain.info/haskoin-store/btc/address/{address}/balance"
        response = await client.get(url=url)

        if response.status_code == 200:
            return ExplorerResponse.parse_obj(json.loads(response.content))
        else:
            logger.error(f"{address} | 'get_btc_balance' response error, "
                         f"code: {response.status_code}, "
                         f"reason: {response.reason_phrase}.")

            if response.status_code == 429:
                await asyncio.sleep(four_two_nine_sleep)
            else:
                return ExplorerResponse(
                    address=address,
                    confirmed=0,
                    unconfirmed=0,
                    utxo=0,
                    txs=0,
                    received=0
                )
