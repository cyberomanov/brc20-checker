import asyncio
import json

import httpx
from loguru import logger

from config import *
from datatypes import *
from utils import read_addresses, remove_duplicates, get_btc_balance


async def get_unisat_response(address: str, client: httpx.AsyncClient) -> UnisatAccount:
    unisat_account = UnisatAccount()

    start = 0
    limit = 100

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
                logger.error(f"unisat response error, code: {unisat_response.code}, msg: {unisat_response.msg}.")
                break
        else:
            logger.error(f"response error, code: {response.status_code}, reason: {response.reason_phrase}.")
            break

    return unisat_account


async def main_checker():
    btc_denom = 100000000
    btc_round = 5
    btc_total = 0.0

    total_token = 0
    total_accounts_with_token = 0

    addresses = read_addresses()
    for index, address in enumerate(addresses):
        timeout = httpx.Timeout(60)
        async with httpx.AsyncClient(timeout=timeout) as client:
            tasks = [
                get_unisat_response(address=address, client=client),
                get_btc_balance(address=address, client=client)
            ]
            results = await asyncio.gather(*tasks)
            unisat_account, btc_balance = results[0], results[1]

            btc_total += btc_balance.confirmed
            message = f"#{index + 1} | {unisat_account.address} | " \
                      f"{round(btc_balance.confirmed / btc_denom, btc_round)} $BTC"
            if unisat_account.response.data.detail:
                unisat_account.response.data.detail = remove_duplicates(account=unisat_account)

                for item in unisat_account.response.data.detail:
                    message_append = f" | [{item.ticker}] transferable: {item.transferableBalance}, " \
                                     f"available: {item.availableBalance}, " \
                                     f"total: {item.overallBalance}."

                    if ticker_to_check == item.ticker:
                        total_token += item.overallBalance
                        total_accounts_with_token += 1

                    if ticker_to_check:
                        if ticker_to_check == item.ticker:
                            logger.info(message + message_append)
                    elif item.ticker not in tickers_to_ignore:
                        logger.info(message + message_append)
            else:
                logger.warning(f"{message} | empty.")

    if ticker_to_check:
        logger.success(f"{ticker_to_check} {total_token} in total | {total_accounts_with_token}/{len(addresses)}.")
    logger.success(f"{round(btc_total / btc_denom, btc_round)} $BTC in total.")
