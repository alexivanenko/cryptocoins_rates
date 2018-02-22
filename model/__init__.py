"""A module that provides interaction with MongoDB"""
import logging
import urllib.parse

from pymongo import MongoClient
from pymongo.errors import (ConnectionFailure, OperationFailure)
from log import bot_logger
from app_config import app

__author__ = 'ivanenkoa@gmail.com'


def model_exit(log_msg):
    bot_logger.log(logging.FATAL, log_msg)
    exit("Can not connect to MongoDB")

DB_CONNECTION = None

db_config = app.get_config().get('db')

try:
    client = MongoClient('mongodb://%s:%s@%s' % (urllib.parse.quote_plus(db_config.get('user')),
                                                 urllib.parse.quote_plus(db_config.get('pass')),
                                                 urllib.parse.quote_plus(db_config.get('server'))))
    try:
        client.server_info()
        DB_CONNECTION = client
    except OperationFailure as e:
        model_exit(str(e))

except ConnectionFailure as e:
    model_exit(str(e))


def get_db():
    if DB_CONNECTION:
        return DB_CONNECTION.get_database(db_config.get('name'))
    else:
        model_exit("Can not connect to Database")
