from model import get_db


def load_by_chat(chat_id):
    """
    Load users collection byt chat ID

    :param int chat_id: Telegram Chat ID
    :return: users dictionary
    """
    return get_db().users.find_one({"chat_id": chat_id})


def create(name, time_zone, chat_id):
    """
    Create users collection

    :param string name: Telegram users's name
    :param string time_zone:
    :param int chat_id: Telegram Chat ID
    :return: inserted collection ID
    """
    user = {
        "chat_id": chat_id,
        "name": name,
        "time_zone": time_zone,
        "coins": []
    }

    return get_db().users.insert_one(user).inserted_id


def update_time_zone(chat_id, time_zone):
    """
    Update user's TimeZone

    :param int chat_id: Telegram Chat ID
    :param string time_zone: time zone like 'Europe/Moscow'
    :return: none
    """
    user = load_by_chat(chat_id)

    if isinstance(user, dict) and 'time_zone' in user:
        get_db().users.update_one({'_id': user['_id']}, {"$set": {"time_zone": time_zone}}, upsert=False)


def get_coins_list(chat_id):
    """
    Get User by Chat ID and return his coins list

    :param int chat_id: Telegram Chat ID
    :return: the list of user's coins
    """
    user = load_by_chat(chat_id)

    if isinstance(user, dict) and 'coins' in user:
        return user['coins']
    else:
        return []


def add_coin(chat_id, coin):
    """
    Add new coin to the user's coins list

    :param int chat_id: Telegram Chat ID
    :param string coin: currency code ISO 4217 like BTC, ETH
    :return: updated list of the user's coins
    """
    user = load_by_chat(chat_id)
    result = []

    if isinstance(user, dict) and 'coins' in user:
        coins = user['coins']

        if coin not in coins:
            coins.append(coin)
            get_db().users.update_one({'_id': user['_id']}, {"$set": {"coins": coins}}, upsert=False)

        result = coins

    return result


def remove_coin(chat_id, coin):
    """
    Remove coin from the user's coins list

    :param int chat_id: Telegram Chat ID
    :param coin: currency code ISO 4217 like BTC, ETH
    :return: updated list of the user's coins
    """
    user = load_by_chat(chat_id)
    result = []

    if isinstance(user, dict) and 'coins' in user:
        coins = user['coins']

        if coin in coins:
            coins.remove(coin)
            get_db().users.update_one({'_id': user['_id']}, {"$set": {"coins": coins}}, upsert=False)

        result = coins

    return result
