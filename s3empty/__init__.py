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
        logger.info(f'Emptying all objects and versions in bucket {bucket_name}')
        s3_bucket.object_versions.delete()
    else:
        logger.info(f'Emptying all objects in bucket {bucket_name}')
        s3_bucket.objects.all().delete()

@click.command()
@click.option('--bucket-name', required=True, show_default=True, type=str,
              help='S3 bucket name to be emptied')
def cli(bucket_name: str) -> None:
    """Python CLI for convenient emptying of S3 bucket
    """
    empty_s3(bucket_name)
