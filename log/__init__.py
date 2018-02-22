"""A module that provides Log functions"""
import logging

__author__ = 'ivanenkoa@gmail.com'

formatter_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.ERROR, format=formatter_str)
logger = logging.getLogger()

handler = logging.FileHandler("error.log", encoding="utf-8")
handler.setLevel(logging.ERROR)

formatter = logging.Formatter(formatter_str)
handler.setFormatter(formatter)

logger.addHandler(handler)
