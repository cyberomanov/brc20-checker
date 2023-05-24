from datatypes import UnisatAccount


def read_addresses(path: str = 'data/btc.txt'):
    with open(path) as file:
        return file.read().splitlines()


def remove_duplicates(account: UnisatAccount):
    item_list = account.response.data.detail
    return [
        item_list[i] for i in range(len(item_list))
        if item_list[i] not in item_list[:i]
    ]
