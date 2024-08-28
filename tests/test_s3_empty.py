# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, call
import unittest.mock
import unittest
from click.testing import CliRunner
from s3empty import empty_s3
from s3empty import cli

class TestS3Empty(unittest.TestCase):

    # @patch('boto3.resource')
    # @patch('s3empty.init')
    # def test_empty_s3_with_bucket_versioning_enabled( # pylint: disable=too-many-arguments
    #         self,
    #         func_init,
    #         func_resource):

    #     mock_logger = unittest.mock.Mock()
    #     mock_resource = unittest.mock.Mock()
    #     mock_bucket_versioning = unittest.mock.Mock()
    #     mock_bucket = unittest.mock.Mock()
    #     mock_bucket_object_versions = unittest.mock.Mock()

    #     func_init.return_value = mock_logger
    #     func_resource.return_value = mock_resource

    #     mock_resource.Bucket.return_value = mock_bucket
    #     mock_resource.BucketVersioning.return_value = mock_bucket_versioning
    #     mock_bucket_versioning.status = unittest.mock.PropertyMock(return_value='Enabled')
    #     mock_bucket.object_versions.return_value = mock_bucket_object_versions

    #     empty_s3(bucket_name='some-bucket')

    #     self.assertEqual(mock_logger.info.call_count, 1)
    #     mock_logger.info.assert_has_calls([
    #         call('Emptying all objects and versions in bucket some-bucket')
    #     ])

    #     self.assertEqual(mock_bucket_object_versions.delete.call_count, 1)
    #     mock_bucket_object_versions.delete.assert_has_calls([
    #         call()
    #     ])

    @patch('boto3.resource')
    @patch('s3empty.init')
    def test_empty_s3_with_bucket_versioning_disabled( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_resource):

        mock_logger = unittest.mock.Mock()
        mock_resource = unittest.mock.Mock()
        mock_bucket_versioning = unittest.mock.Mock()
        mock_bucket = unittest.mock.Mock()
        mock_bucket_objects = unittest.mock.Mock()
        mock_bucket_objects_all = unittest.mock.Mock()

        func_init.return_value = mock_logger
        func_resource.return_value = mock_resource

        mock_resource.Bucket.return_value = mock_bucket
        mock_resource.BucketVersioning.return_value = mock_bucket_versioning
        mock_bucket_versioning.status = unittest.mock.PropertyMock(return_value='Disabled')
        mock_bucket.objects = unittest.mock.PropertyMock(return_value=mock_bucket_objects)
        mock_bucket_objects.all.return_value = mock_bucket_objects_all

        empty_s3(bucket_name='some-bucket')

        self.assertEqual(mock_logger.info.call_count, 1)
        mock_logger.info.assert_has_calls([
            call('Emptying all objects in bucket some-bucket')
        ])

        # self.assertEqual(mock_bucket_objects_all.delete.call_count, 1)
        # mock_bucket_objects_all.delete.assert_has_calls([
        #     call()
        # ])

    @patch('s3empty.empty_s3')
    def test_cli( # pylint: disable=too-many-arguments
            self,
            func_empty_s3):

        func_empty_s3.return_value = None

        runner = CliRunner()
        result = runner.invoke(cli, [
            '--bucket-name',
            'some-bucket'
        ])
        assert not result.exception
        assert result.exit_code == 0
        assert result.output == ''

        # should delegate call to apply
        func_empty_s3.assert_called_once_with('some-bucket')
