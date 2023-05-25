import json

import httpx
from loguru import logger

from datatypes import ExplorerResponse


async def get_btc_balance(address: str, client: httpx.AsyncClient) -> ExplorerResponse:
    url = f"https://api.blockchain.info/haskoin-store/btc/address/{address}/balance"
    response = await client.get(url=url)

    if response.status_code == 200:
        return ExplorerResponse.parse_obj(json.loads(response.content))
    else:
        logger.error(f"response error, code: {response.status_code}, reason: {response.reason_phrase}.")
        return ExplorerResponse(
            address=address,
            confirmed=0,
            unconfirmed=0,
            utxo=0,
            txs=0,
            received=0
        )
