"""Logger for S3 Empty."""
from conflog import Conflog

def init():
    """Initialize logger.
    """

    cfl = Conflog(
        conf_dict={
            'level': 'info',
            'format': '[s3empty] %(levelname)s %(message)s'
        }
    )

    return cfl.get_logger(__name__)
