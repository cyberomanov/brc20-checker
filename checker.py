from config import *
from utils import *


async def main_checker():
    btc_denom = 100000000
    btc_round = 6
    btc_total = 0.0

    total_token = 0
    total_accounts_with_token = 0

    addresses = read_addresses()
    for index, address in enumerate(addresses):
        timeout = httpx.Timeout(60)
        async with httpx.AsyncClient(timeout=timeout) as client:
            tasks = [
                get_unisat_account(address=address, client=client),
                get_btc_balance(address=address, client=client),
                get_magic_tokens(address=address),
            ]
            results = await asyncio.gather(*tasks)
            unisat_account, btc_balance, magic_tokens = results[0], results[1], results[2]

            magic_unisat = get_magic_unisat(unisat=remove_duplicates(account=unisat_account), magic=magic_tokens)

            btc_total += btc_balance.confirmed
            logger.success(f"#{index + 1} | {unisat_account.address} | "
                           f"{btc_balance.confirmed / btc_denom:.{btc_round}f} $BTC.")

            collections_message = ''
            tokens_message = ''

            if magic_unisat:
                for item in magic_unisat:
                    if type(magic_unisat[item]) == dict:
                        if item.upper() not in tickers_to_ignore and item.lower() not in tickers_to_ignore:
                            # if magic_unisat[item]['total']:
                            tokens_message += f"{item.upper()} [transferable: {magic_unisat[item]['transferable']}, " \
                                              f"available: {magic_unisat[item]['available']}, " \
                                              f"total: {magic_unisat[item]['total']}], "
                    else:
                        if item.upper() not in tickers_to_ignore and item.lower() not in tickers_to_ignore:
                            collections_message += f"{item.upper()} {magic_unisat[item]}, "

                    if ticker_to_check.lower() == item.lower():
                        if 'total' in magic_unisat[item]:
                            total_token += magic_unisat[item]['total']
                        else:
                            total_token += len(magic_unisat[item])
                        total_accounts_with_token += 1

                at_least_anything = False
                if collections_message:

                    at_least_anything = True
                    if ticker_to_check:
                        if ticker_to_check.lower() in collections_message or \
                                ticker_to_check.upper() in collections_message:

                            logger.debug('collections: ' + collections_message[:-2] + '.')
                        else:
                            logger.info('collections: ' + collections_message[:-2] + '.')
                    else:
                        logger.info('collections: ' + collections_message[:-2] + '.')
                if tokens_message:

                    at_least_anything = True
                    if ticker_to_check:
                        if ticker_to_check.lower() in tokens_message or \
                                ticker_to_check.upper() in tokens_message:

                            logger.debug('tokens: ' + tokens_message[:-2] + '.')
                        else:
                            logger.info('tokens: ' + tokens_message[:-2] + '.')
                    else:
                        logger.info('tokens: ' + tokens_message[:-2] + '.')
                if not at_least_anything:
                    logger.warning(f"empty: no any collection or token.")
            else:
                logger.warning(f"empty: no any collection or token.")

        logger.info(int(len(addresses[0]) * 1.4) * '-')

    if ticker_to_check:
        logger.info(f"[{ticker_to_check}] {total_token} in total | {total_accounts_with_token}/{len(addresses)}.")
    logger.info(f"{btc_total / btc_denom:.{btc_round}f} $BTC in total.")


if __name__ == '__main__':
    add_logger(version='v1.4')
    try:
        asyncio.run(main_checker())
    except Exception as e:
        logger.exception(e)
