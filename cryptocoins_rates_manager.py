import pytz
import logging

from telegram.ext import (Updater)
from datetime import datetime
from model import user
from log import bot_logger
from cmd import coins
from app_config import app

# Init Bot
try:
    updater = Updater(token=app.get_config().get('bot_token'))
except ValueError as e:
    updater = None
    bot_logger.log(logging.FATAL, str(e))
    exit("Can not init Bot Updater object")

users = user.get_all()
utc_now = pytz.utc.localize(datetime.utcnow())
notification_times = app.get_config().get('notification_times')

for user in users:
    user_time = utc_now.astimezone(pytz.timezone(user['time_zone'])).strftime("%H:%M")

    if user_time in notification_times:
        coins.send_rates(updater.bot, user)
