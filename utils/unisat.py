import asyncio
import json

import httpx
from loguru import logger

from datatypes import *


async def get_unisat_account(address: str, client: httpx.AsyncClient) -> UnisatAccount:
    unisat_account = UnisatAccount()

    start = 0
    limit = 100
    four_two_nine_sleep = 5

    while True:
        url = f"https://unisat.io/brc20-api-v2/address/{address}/brc20/summary?start={start}&limit={limit}"
        response = await client.get(url=url)

        if response.status_code == 200:
            unisat_response = UnisatResponse.parse_obj(json.loads(response.content))

            if unisat_response.code == 0:
                if start == 0:
                    unisat_account = UnisatAccount(address=address, response=unisat_response)
                elif unisat_response.data.detail:
                    unisat_account.response.data.detail += unisat_response.data.detail
                else:
                    break
                start += 1
                limit += 100
            else:
                logger.error(f"{address} | 'internal_unisat' response error, "
                             f"code: {unisat_response.code}, "
                             f"msg: {unisat_response.msg}.")
                break
        else:
            logger.error(f"{address} | 'get_unisat_account' response error, "
                         f"code: {response.status_code}, "
                         f"reason: {response.reason_phrase}.")

            if response.status_code == 429:
                await asyncio.sleep(four_two_nine_sleep)
            else:
                break

    return unisat_account
