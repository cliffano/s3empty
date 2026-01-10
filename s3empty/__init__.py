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
    bucket_name: str = None,
    conf_file: str = None,
    batch_size: int = 0,
    allow_inexisting: bool = False,
    log_level: str = "info",
) -> None:
    """Process the bucket names to be emptied."""

    logger = init(log_level)
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
                _empty_s3_bucket(logger, s3, _bucket_name, batch_size)
            except ClientError as e:
                if (
                    allow_inexisting is True
                    and e.response["Error"]["Code"] == "NoSuchBucket"
                ):
                    logger.warning(f"Bucket {_bucket_name} does not exist")
                else:
                    raise


def _empty_s3_bucket(
    logger: object, s3: object, bucket_name: str, batch_size: int
) -> None:
    """Empty all objects within an S3 bucket."""

    s3_bucket = s3.Bucket(bucket_name)
    bucket_versioning = s3.BucketVersioning(bucket_name)

    if batch_size > 0:
        logger.info(
            f"Emptying objects and versions in bucket {bucket_name} "
            f"in batches of {batch_size}"
        )
        _delete_in_batches(logger, s3, bucket_name, batch_size)
    elif bucket_versioning.status == "Enabled":
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


def _delete_in_batches(
    logger: object, s3: object, bucket_name: str, batch_size: int
) -> None:
    """Delete objects in batches."""
    paginator = s3.meta.client.get_paginator("list_object_versions")
    page_iterator = paginator.paginate(
        Bucket=bucket_name, PaginationConfig={"PageSize": batch_size}
    )

    for page in page_iterator:
        batch = []
        versions = page.get("Versions", [])
        delete_markers = page.get("DeleteMarkers", [])

        for item in versions + delete_markers:
            batch.append({"Key": item["Key"], "VersionId": item["VersionId"]})
            logger.debug(
                f"Adding {item['Key']} {item['VersionId']} to batch for deletion..."
            )

        if not batch:
            logger.warn("No objects or delete markers found in this page")
            continue

        response = s3.meta.client.delete_objects(
            Bucket=bucket_name, Delete={"Objects": batch}
        )
        success_message = (
            f"Successfully deleted a batch of {len(batch)} objects/versions "
            f"in bucket {bucket_name}"
        )
        _handle_response(logger, response, success_message)


def _handle_response(logger, response: dict, success_message: str) -> None:
    # AWS delete_objects usually returns a dict (or list of dicts from paginator).
    # If the payload is not a dict/list of dicts with Deleted/Errors, treat it as unexpected.
    responses = response if isinstance(response, list) else [response]

    has_entries = False
    has_error = False

    for response_item in responses:
        if not isinstance(response_item, dict):
            has_entries = True
            has_error = True
            logger.error("Unexpected response:")
            logger.error(response_item)
            continue

        deleted = response_item.get("Deleted", [])
        errors = response_item.get("Errors", [])

        if deleted:
            has_entries = True
            _log_deleted_items(logger, deleted)

        if errors:
            has_entries = True
            has_error = True
            _log_error_items(logger, errors)

    if has_entries is False:
        logger.info("No objects to delete")
    elif has_error is False:
        logger.info(success_message)


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
    default=None,
    type=str,
    help="S3 bucket name to be emptied",
)
@click.option(
    "--conf-file",
    required=False,
    show_default=True,
    default=None,
    type=str,
    help="Configuration file containing S3 bucket names to be emptied",
)
@click.option(
    "--batch-size",
    required=False,
    show_default=True,
    default=0,
    type=int,
    help="Delete objects and versions in batches of this size",
)
@click.option(
    "--allow-inexisting",
    is_flag=True,
    required=False,
    show_default=True,
    default=False,
    type=bool,
    help="Allow inexisting buckets",
)
@click.option(
    "--log-level",
    required=False,
    show_default=True,
    default="info",
    type=str,
    help="Log level: debug, info, warning, error, critical",
)
@click.version_option(package_name="s3empty", prog_name="s3empty")
def cli(
    bucket_name: str,
    conf_file: str,
    batch_size: int,
    allow_inexisting: bool,
    log_level: str,
) -> None:
    """Python CLI for convenient emptying of S3 bucket"""
    empty_s3(bucket_name, conf_file, batch_size, allow_inexisting, log_level)
