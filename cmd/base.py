from enum import Enum
from geo import time
from model import user
from cmd import coins
from telegram import (ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import ConversationHandler

DEFAULT_TIME_ZONE = "Europe/Moscow"


class CmdStates(Enum):
    START_SAVE_USER = 1


def start(bot, update):
    """
    /start command handler provides 2 scenarios:
    1. New User: show hello message, store user and ask location
    2. Existent User: show hello message and menu buttons

    :param bot:
    :param update:
    :return: next conversation state
    """
    stored_user = user.load_by_chat(update.message.chat_id)

    if not stored_user:
        chat_user = update.message.from_user

        user.create(
            chat_user.first_name + " " + chat_user.last_name,
            DEFAULT_TIME_ZONE,
            update.message.chat_id
        )

        return ask_location(bot, update)
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Hello, " + stored_user['name'] + "! Please choose the command from the list below.",
            reply_markup=coins.default_keyboard()
        )

        return ConversationHandler.END


def ask_location(bot, update):
    """
    Asks user location

    :param bot:
    :param update:
    :return: next conversation state
    """
    location_keyboard = [[KeyboardButton(text="Send Location", request_location=True), KeyboardButton(text="Skip")]]

    markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=False)

    msg = "Hello! I'm CryptoCoins bot. Please share your location with me " \
          "and I'll send you coins rates in the right time."

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        reply_markup=markup
    )

    return CmdStates.START_SAVE_USER


def update_user(bot, update):
    """
    Updates User:
    1. If location provided - find TZ by location, update user's TZ and show this TZ to user
    2. If location not provided: show default TZ to user

    :param bot:
    :param update:
    :return: end conversation state
    """
    user_location = update.message.location

    if user_location:
        timezone = time.get_timezone(user_location.longitude, user_location.latitude)
        user.update_time_zone(update.message.chat_id, timezone)
        msg = "I have added your Time Zone by location - " + timezone
    else:
        msg = "As you wasn't provided your location I have added default Time Zone " \
              "for notifications - " + DEFAULT_TIME_ZONE

    markup = ReplyKeyboardMarkup([[KeyboardButton(text="/add_coin")]], one_time_keyboard=False)

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        reply_markup=markup
    )

    return ConversationHandler.END


def help_msg(bot, update):
    """
    /help command handler

    :param bot:
    :param update:
    :return: None
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello! I'm CryptoCoins bot. You can subscribe to 3 times per day coins rates using /add_coin command. "
             "Just run this command and add your favourites coins. Also you can use /remove_coin command "
             "and remove uninteresting coins from the list. Use /my_coins command to check your selected coins list "
             "and /show_rates command to check selected coins rates.",
        reply_markup=coins.default_keyboard()
    )


def unknown(bot, update):
    """
    Unknown command handler

    :param bot:
    :param update:
    :return: None
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Sorry, I didn't understand that command. Please use a command from the list.",
        reply_markup=coins.default_keyboard()
    )


def cancel(bot, update):
    """
    /cancel command handler

    :param bot:
    :param update:
    :return: None
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Canceled ...",
        reply_markup=coins.default_keyboard()
    )
    return ConversationHandler.END
