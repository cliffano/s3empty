# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from unittest.mock import patch
from click.testing import CliRunner
from moto import mock_aws
import botocore
import boto3
from s3empty import cli


class TestCli(unittest.TestCase):

    def test_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage: cli [OPTIONS]", result.output)
        self.assertIn("Show this message and exit.", result.output)

    def test_cli_with_no_arg(self):
        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] WARNING No buckets specified to be emptied", result.output
        )

    def test_cli_with_invalid_arg(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--some-invalid-arg"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error: No such option: --some-invalid-arg", result.output)

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
    def test_cli_having_versioning_enabled(self):
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket="some-bucket")

        s3.Bucket("some-bucket").put_object(Key="some-key1", Body="some-message1")
        s3.Bucket("some-bucket").put_object(Key="some-key2", Body="some-message2")

        s3.BucketVersioning("some-bucket").enable()

        runner = CliRunner()
        result = runner.invoke(cli, ["--bucket-name", "some-bucket"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] INFO Buckets to be emptied: some-bucket", result.output
        )
        self.assertIn(
            "[s3empty] INFO Emptying all objects and versions in bucket some-bucket...",
            result.output,
        )
        self.assertIn("[s3empty] INFO Deleted some-key1", result.output)
        self.assertIn("[s3empty] INFO Deleted some-key2", result.output)
        self.assertIn(
            "[s3empty] INFO Successfully emptied all objects and versions in bucket some-bucket",
            result.output,
        )

        bucket = s3.Bucket("some-bucket")
        objects = list(bucket.objects.all())
        self.assertEqual(len(objects), 0)

    @mock_aws
    def test_cli_having_versioning_enabled_when_bucket_is_already_emptied(
        self,
    ):
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket="some-bucket")

        s3.BucketVersioning("some-bucket").enable()

        runner = CliRunner()
        result = runner.invoke(cli, ["--bucket-name", "some-bucket"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] INFO Buckets to be emptied: some-bucket", result.output
        )
        self.assertIn(
            "[s3empty] INFO Emptying all objects and versions in bucket some-bucket...",
            result.output,
        )
        self.assertIn("[s3empty] INFO No objects to delete", result.output)
        self.assertNotIn(
            "[s3empty] INFO Successfully emptied all objects and versions in bucket some-bucket",
            result.output,
        )

    @mock_aws
    def test_cli_not_having_versioning_enabled(self):
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
    def test_cli_not_having_versioning_enabled_when_bucket_is_already_emptied(
        self,
    ):
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket="some-bucket")

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
        self.assertIn("[s3empty] INFO No objects to delete", result.output)
        self.assertNotIn(
            "[s3empty] INFO Successfully emptied all objects in bucket some-bucket",
            result.output,
        )

    @mock_aws
    def test_cli_with_inexisting_bucket(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--bucket-name", "some-inexisting-bucket"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] INFO Buckets to be emptied: some-inexisting-bucket",
            result.output,
        )

    @mock_aws
    def test_cli_with_inexisting_bucket_being_allowed(self):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["--bucket-name", "some-inexisting-bucket", "--allow-inexisting"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] WARNING Bucket some-inexisting-bucket does not exist",
            result.output,
        )

    @mock_aws
    @patch("s3empty.CFGRW.read", return_value={"bucket_names": ["some-bucket"]})
    def test_cli_with_conf_file(self, mock_read):  # pylint: disable=unused-argument
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
    @patch("s3empty.CFGRW.read", return_value={"bucket_names": ["some-bucket"]})
    def test_cli_with_conf_template_file(
        self, mock_read
    ):  # pylint: disable=unused-argument
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket="some-bucket")

        s3.Bucket("some-bucket").put_object(Key="some-key1", Body="some-message1")
        s3.Bucket("some-bucket").put_object(Key="some-key2", Body="some-message2")

        runner = CliRunner()
        result = runner.invoke(cli, ["--conf-file", "some-s3empty.yaml.j2"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] INFO Reading configuration file some-s3empty.yaml.j2",
            result.output,
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
    @patch("s3empty.CFGRW.read", return_value={"bucket_names": ["some-bucket2"]})
    def test_cli_with_bucket_and_conf_file(
        self, mock_read
    ):  # pylint: disable=unused-argument
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket="some-bucket1")
        s3.create_bucket(Bucket="some-bucket2")

        s3.Bucket("some-bucket1").put_object(Key="some-key1", Body="some-message1")
        s3.Bucket("some-bucket1").put_object(Key="some-key2", Body="some-message2")
        s3.Bucket("some-bucket2").put_object(Key="some-key3", Body="some-message3")
        s3.Bucket("some-bucket2").put_object(Key="some-key4", Body="some-message4")

        runner = CliRunner()
        result = runner.invoke(
            cli, ["--bucket-name", "some-bucket1", "--conf-file", "s3empty-conf.yaml"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[s3empty] INFO Reading configuration file s3empty-conf.yaml", result.output
        )
        self.assertIn(
            "[s3empty] INFO Buckets to be emptied: some-bucket1, some-bucket2",
            result.output,
        )
        self.assertIn(
            "[s3empty] INFO Emptying all objects in bucket some-bucket1...",
            result.output,
        )
        self.assertIn("[s3empty] INFO Deleted some-key1", result.output)
        self.assertIn("[s3empty] INFO Deleted some-key2", result.output)
        self.assertIn(
            "[s3empty] INFO Successfully emptied all objects in bucket some-bucket1",
            result.output,
        )
        self.assertIn(
            "[s3empty] INFO Emptying all objects in bucket some-bucket2...",
            result.output,
        )
        self.assertIn("[s3empty] INFO Deleted some-key3", result.output)
        self.assertIn("[s3empty] INFO Deleted some-key4", result.output)
        self.assertIn(
            "[s3empty] INFO Successfully emptied all objects in bucket some-bucket2",
            result.output,
        )

        bucket1 = s3.Bucket("some-bucket1")
        objects1 = list(bucket1.objects.all())
        self.assertEqual(len(objects1), 0)

        bucket2 = s3.Bucket("some-bucket2")
        objects2 = list(bucket2.objects.all())
        self.assertEqual(len(objects2), 0)

    @mock_aws
    @patch("s3empty.CFGRW.read", return_value={"bucket_names": ["some-bucket"]})
    def test_cli_with_warning_log_level(
        self, mock_read
    ):  # pylint: disable=unused-argument
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket="some-bucket")

        s3.Bucket("some-bucket").put_object(Key="some-key1", Body="some-message1")
        s3.Bucket("some-bucket").put_object(Key="some-key2", Body="some-message2")

        runner = CliRunner()
        result = runner.invoke(
            cli, ["--conf-file", "some-s3empty.yaml", "--log-level", "warning"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertNotIn(
            "[s3empty] INFO Reading configuration file some-s3empty.yaml", result.output
        )
        self.assertNotIn(
            "[s3empty] INFO Buckets to be emptied: some-bucket", result.output
        )
        self.assertNotIn(
            "[s3empty] INFO Emptying all objects in bucket some-bucket...",
            result.output,
        )
        self.assertNotIn("[s3empty] INFO Deleted some-key1", result.output)
        self.assertNotIn("[s3empty] INFO Deleted some-key2", result.output)
        self.assertNotIn(
            "[s3empty] INFO Successfully emptied all objects in bucket some-bucket",
            result.output,
        )

        bucket = s3.Bucket("some-bucket")
        objects = list(bucket.objects.all())
        self.assertEqual(len(objects), 0)
