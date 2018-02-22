import re
from app_config import app
from coinmarketcap import Market


def get_coin_rate(coin_id):
    """
    Get Crypto Coin USD rate from CoinMarketCap by coin ID
    :param string coin_id: CoinMarketCap coin ID like 'bitcoin' for BTC
    :return: crypto coin USD rate
    """
    market = Market()
    data = market.ticker(coin_id)

    if len(data) > 0:
        data = data[0]

    result = "Unavailable"

    if 'price_usd' in data:
        result = data['price_usd']

    return result


def clear_currency_code(original_code):
    """
    Removes brackets [] from currency code value

    :param string original_code: currency code with brackets like [BTC]
    :return: cleared currency code like BTC
    """
    cleared_code = original_code.replace("[", "")
    cleared_code = cleared_code.replace("]", "")

    return cleared_code


def get_coins_pattern():
    """
    Returns coins regexp pattern object

    :return: pattern object
    """
    return comp("^(" + regex_coins_or() + ")$")


def comp(pattern):
    """
    Returns a pre compiled Regex pattern to ignore case

    :param string pattern: regexp pattern
    :return: pattern object
    """
    return re.compile(pattern, re.IGNORECASE)


def regex_coins_or():
    """
    Returns regex representation of OR for all coins in config 'coins'
    :return: regex coins or str
    """
    coins_regex_or = str()
    all_coins = app.get_config().get('coins')

    for coin in all_coins:
        coins_regex_or += "\[" + coin + "\]|"

    return coins_regex_or[:-1]