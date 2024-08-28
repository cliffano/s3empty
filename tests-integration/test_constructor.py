# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import botocore
from s3empty import empty_s3

class TestConstructor(unittest.TestCase):

    def test_constructor_without_credential(self):
        with self.assertRaises(botocore.exceptions.NoCredentialsError):
            empty_s3('some-bucket')
