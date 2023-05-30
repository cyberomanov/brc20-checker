import asyncio
import json

import httpx
from loguru import logger

from datatypes import MagicResponse, MagicItem


async def get_magic_tokens(address: str, client: httpx.AsyncClient) -> list[MagicItem]:
    total_tokens = []
    four_two_nine_sleep = 5

    limit = 1000
    offset = 0
    no_new_tokens = False

    while not no_new_tokens:
        payload = {
            "limit": limit,
            "offset": offset,
            "ownerAddress": address
        }

        while True:
            url = f"https://api-mainnet.magiceden.io/v2/ord/btc/wallets/tokens"
            response = await client.get(url=url, params=payload)

            if response.status_code == 200:
                magic_response = MagicResponse.parse_obj(json.loads(response.content))
                if magic_response.tokens:
                    total_tokens.extend(magic_response.tokens)

                    limit += 1000
                    offset += 1000
                else:
                    no_new_tokens = True
                break
            else:
                logger.error(f"{address} | 'get_magic_token' response error, "
                             f"code: {response.status_code}, "
                             f"reason: {response.reason_phrase}.")

                if response.status_code == 429:
                    await asyncio.sleep(four_two_nine_sleep)
                else:
                    break

    return total_tokens
