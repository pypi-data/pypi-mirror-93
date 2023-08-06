import logging
import sys

logger = logging.getLogger('MySDK')
formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)

console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)

logger.setLevel(logging.ERROR)

from mysdk import apihelper

"""
Module : mysdk
"""


class MySDK:
    """ This is the MySDK class.
    Methods: 
        get_jobs
        create_job
        update_job
        delete_job
    """

    def __init__(self, token) -> None:
        """
        :param token: MyShare given token
        :param test: what do you like
        """

        self.token = token



