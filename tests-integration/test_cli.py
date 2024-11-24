# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from unittest.mock import patch
from click.testing import CliRunner
from moto import mock_aws
import botocore
import boto3
from s3empty import cli


class TestCli(unittest.TestCase):

    def test_cli_with_invalid_arg(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--some-invalid-arg"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("No such option: --some-invalid-arg", result.output)

    @mock_aws
    def test_cli_without_credential(self):
        with patch("boto3.Session") as mock_boto3_session:
            mock_boto3_session.side_effect = botocore.exceptions.NoCredentialsError

            runner = CliRunner()
            result = runner.invoke(cli, ["--bucket-name", "some-bucket"])

            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("Unable to locate credentials", result.exception.args[0])
            self.assertIn("NoCredentialsError", result.exc_info[0].__name__)

    @mock_aws
    def test_cli_having_successful_deletion(self):
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket="some-bucket")

        s3.Bucket("some-bucket").put_object(Key="some-key1", Body="some-message1")
        s3.Bucket("some-bucket").put_object(Key="some-key2", Body="some-message2")

        runner = CliRunner()
        result = runner.invoke(cli, ["--bucket-name", "some-bucket"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] INFO Buckets to be emptied: some-bucket", result.output
        )
        self.assertIn(
            "[s3empty] INFO Emptying all objects in bucket some-bucket...",
            result.output,
        )
        self.assertIn("[s3empty] INFO Deleted some-key1", result.output)
        self.assertIn("[s3empty] INFO Deleted some-key2", result.output)
        self.assertIn(
            "[s3empty] INFO Successfully emptied all objects in bucket some-bucket",
            result.output,
        )

        bucket = s3.Bucket("some-bucket")
        objects = list(bucket.objects.all())
        self.assertEqual(len(objects), 0)

    @mock_aws
    @patch("s3empty.CFGRW.read", return_value={"bucket_names": ["some-bucket"]})
    def test_cli_having_successful_deletion_with_conf_file(
        self, mock_read
    ):  # pylint: disable=unused-argument
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket="some-bucket")

        s3.Bucket("some-bucket").put_object(Key="some-key1", Body="some-message1")
        s3.Bucket("some-bucket").put_object(Key="some-key2", Body="some-message2")

        runner = CliRunner()
        result = runner.invoke(cli, ["--conf-file", "some-s3empty.yaml"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] INFO Reading configuration file some-s3empty.yaml", result.output
        )
        self.assertIn(
            "[s3empty] INFO Buckets to be emptied: some-bucket", result.output
        )
        self.assertIn(
            "[s3empty] INFO Emptying all objects in bucket some-bucket...",
            result.output,
        )
        self.assertIn("[s3empty] INFO Deleted some-key1", result.output)
        self.assertIn("[s3empty] INFO Deleted some-key2", result.output)
        self.assertIn(
            "[s3empty] INFO Successfully emptied all objects in bucket some-bucket",
            result.output,
        )

        bucket = s3.Bucket("some-bucket")
        objects = list(bucket.objects.all())
        self.assertEqual(len(objects), 0)

    @mock_aws
    def test_cli_having_successful_deletion_with_inexisting_bucket(self):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["--bucket-name", "some-inexisting-bucket", "--allow-inexisting"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] WARNING Bucket some-inexisting-bucket does not exist",
            result.output,
        )
