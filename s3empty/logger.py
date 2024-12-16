"""Logger for S3 Empty."""

from conflog import Conflog


def init(log_level: str) -> object:
    """Initialize logger."""

    cfl = Conflog(
        conf_dict={"level": log_level, "format": "[s3empty] %(levelname)s %(message)s"}
    )

    return cfl.get_logger(__name__)
