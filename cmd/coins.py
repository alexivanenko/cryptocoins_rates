from enum import Enum
from app_config import app
from model import user
from cmd import helper
from telegram import (ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import ConversationHandler


class AddCoinStates(Enum):
    ADD = 1
    COMPLETE_ADD = 2
    REMOVE = 3
    COMPLETE_REMOVE = 4


def build_menu(buttons, cols_num=1):
    menu = [buttons[i:i + cols_num] for i in range(0, len(buttons), cols_num)]

    return menu


def get_markup(buttons, cols_num):
    return ReplyKeyboardMarkup(build_menu(buttons, cols_num))


def default_keyboard():
    """
    Returns bot default keyboard with base coins commands
    :return: keyboard markup
    """
    command_buttons = [
        KeyboardButton("/my_coins"),
        KeyboardButton("/add_coin"),
        KeyboardButton("/remove_coin"),
        KeyboardButton("/show_rates"),
    ]

    return get_markup(command_buttons, 2)


def my_coins(bot, update):
    """
    Show user's crypto coins list with USD rates
    :param bot:
    :param update:
    :return: None
    """
    user_coins = user.get_coins_list(update.message.chat_id)

    if not user_coins:
        msg = "Please add some coins using /add_coin command."
    else:
        msg = "Your favourite Crypto Coins:\n"
        all_coins = app.get_config().get('coins')

        for coin in user_coins:
            rate = ""
            coin_id = ""

            if coin in all_coins:
                coin_id = all_coins[coin]
                rate = helper.get_coin_rate(coin_id)
                rate = "$" + rate

            msg += "<b>["+coin+"] "+coin_id.title()+": "+rate+"</b>\n"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        parse_mode="HTML",
        reply_markup=default_keyboard()
    )


def add_coin_start(bot, update):
    """
    Shows add coin message and available for adding coins
    :param bot:
    :param update:
    :return: next conversation state
    """
    all_coins = app.get_config().get('coins')
    user_coins = user.get_coins_list(update.message.chat_id)

    if len(all_coins) == len(user_coins):

        markup = default_keyboard()
        msg = "All available coins were added to your list. You can add more coins in the config.json file."
        result = ConversationHandler.END

    else:

        buttons = []
        counter = 1

        for coin in all_coins:
            # don't show more than 10 coins
            if counter >= 10:
                break

            if coin not in user_coins:
                buttons.append(KeyboardButton("["+coin+"]"))
                counter += 1

        buttons.append(KeyboardButton("/cancel"))
        markup = get_markup(buttons, cols_num=2)
        msg = "Please select Crypto Coin from the list bellow for adding."

        result = AddCoinStates.ADD

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        reply_markup=markup
    )

    return result


def add_coin(bot, update):
    """
    Update user's coins list: add selected coin
    :param bot:
    :param update:
    :return: nex conversation state
    """
    coin = helper.clear_currency_code(update.message.text)
    if coin:
        user.add_coin(update.message.chat_id, coin)

    buttons = [
        KeyboardButton("/add_coin"),
        KeyboardButton("/cancel")
    ]

    bot.send_message(
        chat_id=update.message.chat_id,
        text=coin + " was successfully added to your coins list. Do you want to add more coins or cancel operation?",
        reply_markup=get_markup(buttons, cols_num=2)
    )

    return AddCoinStates.COMPLETE_ADD


def remove_coin_start(bot, update):
    """
    Shows remove coin message and available for removing coins

    :param bot:
    :param update:
    :return: next conversation state
    """
    user_coins = user.get_coins_list(update.message.chat_id)

    if not user_coins:

        markup = default_keyboard()
        msg = "Please add some coins to your list."
        result = ConversationHandler.END

    else:

        buttons = []
        counter = 1

        for coin in user_coins:
            # don't show more than 10 coins
            if counter >= 10:
                break

            buttons.append(KeyboardButton("["+coin+"]"))
            counter += 1

        buttons.append(KeyboardButton("/cancel"))
        markup = get_markup(buttons, cols_num=2)
        msg = "Please select Crypto Coin from the list bellow for removing."

        result = AddCoinStates.REMOVE

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        reply_markup=markup
    )

    return result


def remove_coin(bot, update):
    """
    Update user's coins list: remove selected coin
    :param bot:
    :param update:
    :return: nex conversation state
    """
    coin = helper.clear_currency_code(update.message.text)
    if coin:
        user.remove_coin(update.message.chat_id, coin)

    buttons = [
        KeyboardButton("/remove_coin"),
        KeyboardButton("/cancel")
    ]

    bot.send_message(
        chat_id=update.message.chat_id,
        text=coin + " was successfully removed from your coins list. "
                    "Do you want to remove more coins or cancel operation?",
        reply_markup=get_markup(buttons, cols_num=2)
    )

    return AddCoinStates.COMPLETE_REMOVE
