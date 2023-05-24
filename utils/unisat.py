import json

import requests
from loguru import logger

from config import *
from datatypes import *
from utils import read_addresses, remove_duplicates


def get_response(address: str) -> UnisatAccount:
    unisat_account = UnisatAccount()

    start = 0
    limit = 100

    while True:
        url = f"https://unisat.io/brc20-api-v2/address/{address}/brc20/summary?start={start}&limit={limit}"
        response = requests.get(url=url)

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
            logger.error(f"response error, code: {response.status_code}, reason: {response.reason}.")
            break

    return unisat_account


def main_checker():
    total_token = 0
    total_accounts_with_token = 0

    addresses = read_addresses()
    for index, address in enumerate(addresses):
        unisat_account = get_response(address=address)

        if unisat_account.response.data.detail:
            unisat_account.response.data.detail = remove_duplicates(account=unisat_account)

            for item in unisat_account.response.data.detail:
                if ticker_to_check == item.ticker:
                    total_token += item.overallBalance
                    total_accounts_with_token += 1

                if ticker_to_check == item.ticker or item.ticker not in tickers_to_ignore:
                    logger.info(f"#{index + 1} | {unisat_account.address} | "
                                f"{item.ticker}: transferable: {item.transferableBalance}, "
                                f"available: {item.availableBalance}, "
                                f"total: {item.overallBalance}.")
        else:
            logger.warning(f"#{index + 1} | {unisat_account.address} | empty.")

    if ticker_to_check:
        logger.info(f"{ticker_to_check} {total_token} in total | {total_accounts_with_token}/{len(addresses)}.")
