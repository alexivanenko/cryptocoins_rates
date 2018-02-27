"""A module that provides app configuration"""
import json
import os

__author__ = 'ivanenkoa@gmail.com'

script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = script_dir.replace("app_config", "")
conf_path = os.path.join(script_dir, 'config.json')

if not os.path.isfile(conf_path):
    exit("config.json file not found")

with open(conf_path) as config_file:
    CONFIG = json.load(config_file)

if len(CONFIG["bot_token"]) == 0:
    exit("Empty Bot Token")

if len(CONFIG["coins"]) == 0:
    exit("There are not any coins in the list in config.json")
