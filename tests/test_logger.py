# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import logging
import unittest
from s3empty.logger import init


class TesLogger(unittest.TestCase):

    def test_init(self):

        logger = init("info")
        assert isinstance(logger, logging.LoggerAdapter) is True
