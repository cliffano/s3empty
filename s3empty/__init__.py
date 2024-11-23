# pylint: disable=too-many-locals
"""
s3empty
=======
Empty an AWS S3 bucket, versioned, not versioned, anything.
"""
import boto3
from botocore.exceptions import ClientError
import click
from cfgrw import CFGRW
from .logger import init


def empty_s3(
    bucket_name: str = None, conf_file: str = None, allow_inexisting: bool = False
) -> None:
    """Process the bucket names to be emptied."""

    logger = init()
    s3 = boto3.resource("s3")

    bucket_names = []

    if bucket_name is not None:
        bucket_names.append(bucket_name)

    if conf_file is not None:
        logger.info(f"Reading configuration file {conf_file}")
        cfgrw = CFGRW(conf_file=conf_file)
        conf_values = cfgrw.read(["bucket_names"])
        bucket_names.extend(conf_values["bucket_names"])

    if not bucket_names:
        logger.warning("No buckets specified to be emptied")
    else:
        logger.info(f'Buckets to be emptied: {", ".join(bucket_names)}')
        for _bucket_name in bucket_names:
            try:
                _empty_s3_bucket(logger, s3, _bucket_name)
            except ClientError as e:
                if (
                    allow_inexisting is True
                    and e.response["Error"]["Code"] == "NoSuchBucket"
                ):
                    logger.warning(f"Bucket {_bucket_name} does not exist")
                else:
                    raise


def _empty_s3_bucket(logger: object, s3: object, bucket_name: str) -> None:
    """Empty all objects within an S3 bucket."""

    s3_bucket = s3.Bucket(bucket_name)
    bucket_versioning = s3.BucketVersioning(bucket_name)

    if bucket_versioning.status == "Enabled":
        logger.info(f"Emptying all objects and versions in bucket {bucket_name}...")
        response = s3_bucket.object_versions.delete()
        success_message = (
            f"Successfully emptied all objects and versions in bucket {bucket_name}"
        )
        _handle_response(logger, response, success_message)
    else:
        logger.info(f"Emptying all objects in bucket {bucket_name}...")
        response = s3_bucket.objects.all().delete()
        success_message = f"Successfully emptied all objects in bucket {bucket_name}"
        _handle_response(logger, response, success_message)


def _handle_response(logger, response: dict, success_message: str) -> None:
    if isinstance(response, list) and len(response) >= 1:
        has_error = False
        for response_item in response:
            if "Deleted" in response_item and len(response_item["Deleted"]) >= 1:
                _log_deleted_items(logger, response_item["Deleted"])
            if "Errors" in response_item and len(response_item["Errors"]) >= 1:
                has_error = True
                _log_error_items(logger, response_item["Errors"])
        if has_error is False:
            logger.info(success_message)
    elif isinstance(response, list) and len(response) == 0:
        logger.info("No objects to delete")
    else:
        logger.error("Unexpected response:")
        logger.error(response)


def _log_deleted_items(logger, deleted_items: list) -> None:
    for deleted in deleted_items:
        if "VersionId" in deleted:
            logger.info(f'Deleted {deleted["Key"]} {deleted["VersionId"]}')
        else:
            logger.info(f'Deleted {deleted["Key"]}')


def _log_error_items(logger, error_items: list) -> None:
    for error in error_items:
        if "VersionId" in error:
            logger.error(
                (
                    f'Error {error["Code"]} - Unable to delete '
                    f'key {error["Key"]} {error["VersionId"]}: {error["Message"]}'
                )
            )
        else:
            logger.error(
                (
                    f'Error {error["Code"]} - Unable to delete '
                    f'key {error["Key"]}: {error["Message"]}'
                )
            )


@click.command()
@click.option(
    "--bucket-name",
    required=False,
    show_default=True,
    type=str,
    help="S3 bucket name to be emptied",
)
@click.option(
    "--conf-file",
    required=False,
    show_default=True,
    type=str,
    help="Configuration file containing S3 bucket names to be emptied",
)
@click.option(
    "--allow-inexisting",
    is_flag=True,
    required=False,
    show_default=True,
    type=bool,
    help="Allow inexisting buckets",
)
def cli(bucket_name: str, conf_file: str, allow_inexisting: bool) -> None:
    """Python CLI for convenient emptying of S3 bucket"""
    empty_s3(bucket_name, conf_file, allow_inexisting)
