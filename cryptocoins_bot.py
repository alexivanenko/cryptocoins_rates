import logging

from telegram.ext import (Updater, CommandHandler, ConversationHandler, MessageHandler, RegexHandler, Filters)
from log import bot_logger
from cmd import base
from cmd import coins
from app_config import app

# Init Bot
try:
    updater = Updater(token=app.get_config().get('bot_token'))
except ValueError as e:
    updater = None
    bot_logger.log(logging.FATAL, str(e))
    exit("Can not init Bot Updater object")


updater.dispatcher.add_handler(CommandHandler("help", base.help_msg))
updater.dispatcher.add_handler(CommandHandler("my_coins", coins.my_coins))
updater.dispatcher.add_handler(CommandHandler("show_rates", coins.my_coins))

hello_handler = ConversationHandler(
    entry_points=[CommandHandler('start', base.start)],
    states={
        base.CmdStates.START_SAVE_USER:
            [
                MessageHandler(Filters.location, base.update_user),
                RegexHandler('^Skip$', base.update_user)
            ],
    },
    fallbacks=[CommandHandler('cancel', base.cancel)]
)

updater.dispatcher.add_handler(hello_handler)

add_coin_handler = ConversationHandler(
    entry_points=[CommandHandler('add_coin', coins.add_coin_start)],
    states={
        coins.AddCoinStates.ADD:
            [
                RegexHandler(coins.helper.get_coins_pattern(), coins.add_coin),
                CommandHandler('cancel', base.cancel)
            ],
        coins.AddCoinStates.COMPLETE_ADD:
            [
                CommandHandler('add_coin', coins.add_coin_start),
                CommandHandler('cancel', base.cancel)
            ],
    },
    fallbacks=[CommandHandler('cancel', base.cancel)]
)

updater.dispatcher.add_handler(add_coin_handler)

remove_coin_handler = ConversationHandler(
    entry_points=[CommandHandler('remove_coin', coins.remove_coin_start)],
    states={
        coins.AddCoinStates.REMOVE:
            [
                RegexHandler(coins.helper.get_coins_pattern(), coins.remove_coin),
                CommandHandler('cancel', base.cancel)
            ],
        coins.AddCoinStates.COMPLETE_REMOVE:
            [
                CommandHandler('remove_coin', coins.remove_coin_start),
                CommandHandler('cancel', base.cancel)
            ],
    },
    fallbacks=[CommandHandler('cancel', base.cancel)]
)

updater.dispatcher.add_handler(remove_coin_handler)

updater.dispatcher.add_handler(MessageHandler(Filters.command, base.unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, base.unknown))

updater.start_polling()
updater.idle()
