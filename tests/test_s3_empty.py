# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, call
import unittest.mock
import unittest
from click.testing import CliRunner
from s3empty import empty_s3
from s3empty import cli

class TestS3Empty(unittest.TestCase):

    @patch('boto3.resource')
    @patch('s3empty.init')
    def test_empty_s3_with_bucket_versioning_enabled_and_successful_deletion( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_resource):

        mock_logger = unittest.mock.Mock()
        mock_bucket_versioning = unittest.mock.Mock()
        mock_bucket = unittest.mock.Mock()
        mock_bucket_object_versions = unittest.mock.Mock()
        mock_response = [
            {
                'ResponseMetadata': {},
                'Deleted': [
                    {
                        'Key': 'some-key1',
                        'VersionId': 'some-version1'
                    }
                ]
            }
        ]

        func_init.return_value = mock_logger

        func_init.return_value = mock_logger
        func_resource.return_value.Bucket.return_value = mock_bucket
        func_resource.return_value.BucketVersioning.return_value = mock_bucket_versioning
        mock_bucket_versioning.status = 'Enabled'
        mock_bucket.object_versions = mock_bucket_object_versions
        mock_bucket_object_versions.delete.return_value = mock_response

        empty_s3(bucket_name='some-bucket', conf_file=None)

        self.assertEqual(mock_logger.info.call_count, 4)
        mock_logger.info.assert_has_calls([
            call('Buckets to be emptied: some-bucket')
        ])
        mock_logger.info.assert_has_calls([
            call('Emptying all objects and versions in bucket some-bucket...')
        ])
        mock_logger.info.assert_has_calls([
            call('Deleted some-key1 some-version1')
        ])
        mock_logger.info.assert_has_calls([
            call('Successfully emptied all objects and versions in bucket some-bucket')
        ])

        self.assertEqual(mock_bucket_object_versions.delete.call_count, 1)
        mock_bucket_object_versions.delete.assert_has_calls([
            call()
        ])

    @patch('boto3.resource')
    @patch('s3empty.init')
    def test_empty_s3_with_bucket_versioning_enabled_and_erronous_deletion( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_resource):

        mock_logger = unittest.mock.Mock()
        mock_bucket_versioning = unittest.mock.Mock()
        mock_bucket = unittest.mock.Mock()
        mock_bucket_object_versions = unittest.mock.Mock()
        mock_response = [
            {
                'ResponseMetadata': {},
                'Errors': [
                    {
                        'Code': 'some-code1',
                        'Key': 'some-key1',
                        'VersionId': 'some-version1',
                        'Message': 'some-message1'
                    }
                ]
            }
        ]

        func_init.return_value = mock_logger

        func_init.return_value = mock_logger
        func_resource.return_value.Bucket.return_value = mock_bucket
        func_resource.return_value.BucketVersioning.return_value = mock_bucket_versioning
        mock_bucket_versioning.status = 'Enabled'
        mock_bucket.object_versions = mock_bucket_object_versions
        mock_bucket_object_versions.delete.return_value = mock_response

        empty_s3(bucket_name='some-bucket', conf_file=None)

        self.assertEqual(mock_logger.error.call_count, 1)
        mock_logger.error.assert_has_calls([
            call((
                'Error some-code1 - Unable to delete '
                'key some-key1 some-version1: some-message1'
            ))
        ])

        self.assertEqual(mock_logger.info.call_count, 2)
        mock_logger.info.assert_has_calls([
            call('Buckets to be emptied: some-bucket')
        ])
        mock_logger.info.assert_has_calls([
            call('Emptying all objects and versions in bucket some-bucket...')
        ])

        self.assertEqual(mock_bucket_object_versions.delete.call_count, 1)
        mock_bucket_object_versions.delete.assert_has_calls([
            call()
        ])

    @patch('boto3.resource')
    @patch('s3empty.init')
    def test_empty_s3_with_bucket_versioning_disabled_and_successful_deletion( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_resource):

        mock_logger = unittest.mock.Mock()
        mock_bucket_versioning = unittest.mock.Mock()
        mock_bucket = unittest.mock.Mock()
        mock_bucket_objects_all = unittest.mock.Mock()
        mock_response = [
            {
                'ResponseMetadata': {},
                'Deleted': [
                    {
                        'Key': 'some-key1'
                    }
                ]
            }
        ]

        func_init.return_value = mock_logger
        func_resource.return_value.Bucket.return_value = mock_bucket
        func_resource.return_value.BucketVersioning.return_value = mock_bucket_versioning
        mock_bucket_versioning.status = 'Disabled'
        mock_bucket.objects.all.return_value = mock_bucket_objects_all
        mock_bucket_objects_all.delete.return_value = mock_response

        empty_s3(bucket_name='some-bucket', conf_file=None)

        self.assertEqual(mock_logger.info.call_count, 4)
        mock_logger.info.assert_has_calls([
            call('Buckets to be emptied: some-bucket')
        ])
        mock_logger.info.assert_has_calls([
            call('Emptying all objects in bucket some-bucket...')
        ])
        mock_logger.info.assert_has_calls([
            call('Deleted some-key1')
        ])
        mock_logger.info.assert_has_calls([
            call('Successfully emptied all objects in bucket some-bucket')
        ])

        self.assertEqual(mock_bucket_objects_all.delete.call_count, 1)
        mock_bucket_objects_all.delete.assert_has_calls([
            call()
        ])

    @patch('boto3.resource')
    @patch('s3empty.init')
    def test_empty_s3_with_bucket_versioning_disabled_and_erronous_deletion( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_resource):

        mock_logger = unittest.mock.Mock()
        mock_bucket_versioning = unittest.mock.Mock()
        mock_bucket = unittest.mock.Mock()
        mock_bucket_objects_all = unittest.mock.Mock()
        mock_response = [
            {
                'ResponseMetadata': {},
                'Errors': [
                    {
                        'Code': 'some-code1',
                        'Key': 'some-key1',
                        'Message': 'some-message1'
                    }
                ]
            }
        ]

        func_init.return_value = mock_logger
        func_resource.return_value.Bucket.return_value = mock_bucket
        func_resource.return_value.BucketVersioning.return_value = mock_bucket_versioning
        mock_bucket_versioning.status = 'Disabled'
        mock_bucket.objects.all.return_value = mock_bucket_objects_all
        mock_bucket_objects_all.delete.return_value = mock_response

        empty_s3(bucket_name='some-bucket', conf_file=None)

        self.assertEqual(mock_logger.error.call_count, 1)
        mock_logger.error.assert_has_calls([
            call('Error some-code1 - Unable to delete key some-key1: some-message1')
        ])

        self.assertEqual(mock_logger.info.call_count, 2)
        mock_logger.info.assert_has_calls([
            call('Buckets to be emptied: some-bucket')
        ])
        mock_logger.info.assert_has_calls([
            call('Emptying all objects in bucket some-bucket...')
        ])

        self.assertEqual(mock_bucket_objects_all.delete.call_count, 1)
        mock_bucket_objects_all.delete.assert_has_calls([
            call()
        ])

    @patch('boto3.resource')
    @patch('s3empty.init')
    def test_empty_s3_with_no_objects( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_resource):

        mock_logger = unittest.mock.Mock()
        mock_bucket_versioning = unittest.mock.Mock()
        mock_bucket = unittest.mock.Mock()
        mock_bucket_object_versions = unittest.mock.Mock()
        mock_response = []

        func_init.return_value = mock_logger

        func_init.return_value = mock_logger
        func_resource.return_value.Bucket.return_value = mock_bucket
        func_resource.return_value.BucketVersioning.return_value = mock_bucket_versioning
        mock_bucket_versioning.status = 'Enabled'
        mock_bucket.object_versions = mock_bucket_object_versions
        mock_bucket_object_versions.delete.return_value = mock_response

        empty_s3(bucket_name='some-bucket', conf_file=None)

        self.assertEqual(mock_logger.info.call_count, 3)
        mock_logger.info.assert_has_calls([
            call('Buckets to be emptied: some-bucket')
        ])
        mock_logger.info.assert_has_calls([
            call('Emptying all objects and versions in bucket some-bucket...')
        ])
        mock_logger.info.assert_has_calls([
            call('No objects to delete')
        ])

        self.assertEqual(mock_bucket_object_versions.delete.call_count, 1)
        mock_bucket_object_versions.delete.assert_has_calls([
            call()
        ])

    @patch('boto3.resource')
    @patch('s3empty.init')
    def test_empty_s3_with_unexpected_response( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_resource):

        mock_logger = unittest.mock.Mock()
        mock_bucket_versioning = unittest.mock.Mock()
        mock_bucket = unittest.mock.Mock()
        mock_bucket_object_versions = unittest.mock.Mock()
        mock_response = 'some-unexpected-message'

        func_init.return_value = mock_logger

        func_init.return_value = mock_logger
        func_resource.return_value.Bucket.return_value = mock_bucket
        func_resource.return_value.BucketVersioning.return_value = mock_bucket_versioning
        mock_bucket_versioning.status = 'Enabled'
        mock_bucket.object_versions = mock_bucket_object_versions
        mock_bucket_object_versions.delete.return_value = mock_response

        empty_s3(bucket_name='some-bucket', conf_file=None)

        self.assertEqual(mock_logger.error.call_count, 2)
        mock_logger.error.assert_has_calls([
            call('Unexpected response:'),
            call('some-unexpected-message')
        ])

        self.assertEqual(mock_logger.info.call_count, 2)
        mock_logger.info.assert_has_calls([
            call('Buckets to be emptied: some-bucket')
        ])
        mock_logger.info.assert_has_calls([
            call('Emptying all objects and versions in bucket some-bucket...')
        ])

        self.assertEqual(mock_bucket_object_versions.delete.call_count, 1)
        mock_bucket_object_versions.delete.assert_has_calls([
            call()
        ])

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
        func_empty_s3.assert_called_once_with('some-bucket', None)
