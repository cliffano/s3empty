# pylint: disable=too-many-locals
"""
s3empty
"""
import boto3
import click
from .logger import init

def empty_s3(bucket_name: str) -> None:
    """Display text from configuration file."""

    logger = init()

    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(bucket_name)
    bucket_versioning = s3.BucketVersioning(bucket_name)

    if bucket_versioning.status == 'Enabled':
        logger.info(f'Emptying all objects and versions in bucket {bucket_name}...')
        response = s3_bucket.object_versions.delete()
        success_message = f'Successfully emptied all objects and versions in bucket {bucket_name}'
        _handle_response(logger, response, success_message)
    else:
        logger.info(f'Emptying all objects in bucket {bucket_name}...')
        response = s3_bucket.objects.all().delete()
        success_message = f'Successfully emptied all objects in bucket {bucket_name}'
        _handle_response(logger, response, success_message)

def _handle_response(logger, response, success_message):
    if isinstance(response, list) and len(response) >= 1:
        has_error = False
        for response_item in response:
            if 'Deleted' in response_item and len(response_item['Deleted']) >= 1:
                _log_deleted_items(logger, response_item['Deleted'])
            if 'Errors' in response_item and len(response_item['Errors']) >= 1:
                has_error = True
                _log_error_items(logger, response_item['Errors'])
        if has_error is False:
            logger.info(success_message)
    elif isinstance(response, list) and len(response) == 0:
        logger.info('No objects to delete')
    else:
        logger.error('Unexpected response:')
        logger.error(response)

def _log_deleted_items(logger, deleted_items):
    for deleted in deleted_items:
        if 'Version' in deleted:
            logger.info(f'Deleted {deleted["Key"]} version {deleted["Version"]}')
        else:
            logger.info(f'Deleted {deleted["Key"]}')

def _log_error_items(logger, error_items):
    for error in error_items:
        if 'Version' in error:
            logger.error((
                f'Error {error["Code"]} - Unable to delete '
                f'key {error["Key"]} version {error["Version"]}: {error["Message"]}'
            ))
        else:
            logger.error((
                f'Error {error["Code"]} - Unable to delete '
                f'key {error["Key"]}: {error["Message"]}'
            ))

@click.command()
@click.option('--bucket-name', required=True, show_default=True, type=str,
              help='S3 bucket name to be emptied')
def cli(bucket_name: str) -> None:
    """Python CLI for convenient emptying of S3 bucket
    """
    empty_s3(bucket_name)
