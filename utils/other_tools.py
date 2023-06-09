import base64
import json

from loguru import logger

from datatypes import UnisatAccount, MagicItem, UnisatItem, MagicDecodedItem


def read_addresses(path: str = 'data/btc.txt'):
    with open(path) as file:
        return file.read().splitlines()


def remove_duplicates(account: UnisatAccount):
    item_list = account.response.data.detail
    return [
        item_list[i] for i in range(len(item_list))
        if item_list[i] not in item_list[:i]
    ]


def decode_magic_base_64(item: MagicItem) -> MagicDecodedItem:
    try:
        decoded_magic_item_bytes = base64.b64decode(item.contentBody)
        decoded_magic_item_string = decoded_magic_item_bytes.decode('utf-8')
        decoded_magic_item = MagicDecodedItem.parse_obj(json.loads(decoded_magic_item_string))
        if 'name' in decoded_magic_item_string:
            decoded_magic_item.tick = decoded_magic_item.name.lower()
            decoded_magic_item.amt = 1
        elif 'tick' in decoded_magic_item_string:
            decoded_magic_item.tick = decoded_magic_item.tick.lower()
        return decoded_magic_item
    except Exception as e:
        logger.exception(e)


def get_magic_unisat(magic: list[MagicItem], unisat: list[UnisatItem]) -> dict:
    with_collection = {}
    wo_collection = {}

    for item in magic:
        if item.collectionSymbol:
            try:
                nft_name = item.meta.name if item.meta else f"#{item.inscriptionNumber}"
                collection_name = item.collection.name
                if 'BRC20' in collection_name:
                    collection_name = collection_name.replace('BRC20 ', '')

                if collection_name in with_collection:
                    with_collection[collection_name].append(nft_name)
                else:
                    with_collection[collection_name] = [nft_name]
            except Exception as e:
                logger.exception(e)
        else:
            decoded_magic_item = decode_magic_base_64(item=item)
            if decoded_magic_item.tick in wo_collection:
                wo_collection[decoded_magic_item.tick] += 1
            else:
                wo_collection[decoded_magic_item.tick] = 1

    for item in unisat:
        if item.ticker.lower() in wo_collection:
            if item.ticker.lower() in with_collection:
                wo_collection.pop(item.ticker.lower())
            else:
                if item.overallBalance:
                    wo_collection[item.ticker.lower()] = {
                        "transferable": item.transferableBalance,
                        "available": item.availableBalance,
                        "total": item.overallBalance
                    }
                else:
                    wo_collection.pop(item.ticker.lower())

    return {**with_collection, **wo_collection}
