"""A module that provides app configuration"""
import json
import os

__author__ = 'ivanenkoa@gmail.com'

if not os.path.isfile("config.json"):
    exit("config.json file not found")

with open("config.json") as config_file:
    CONFIG = json.load(config_file)

if len(CONFIG["bot_token"]) == 0:
    exit("Empty Bot Token")

if len(CONFIG["coins"]) == 0:
    exit("There are not any coins in the list in config.json")
