<img align="right" src="https://raw.github.com/cliffano/s3empty/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/s3empty/workflows/CI/badge.svg)](https://github.com/cliffano/s3empty/actions?query=workflow%3ACI)
[![Security Status](https://snyk.io/test/github/cliffano/s3empty/badge.svg)](https://snyk.io/test/github/cliffano/s3empty)
[![Dependencies Status](https://img.shields.io/librariesio/release/pypi/s3empty)](https://libraries.io/github/cliffano/s3empty)
[![Published Version](https://img.shields.io/pypi/v/s3empty.svg)](https://pypi.python.org/pypi/s3empty)
<br/>

S3Empty
--------

S3Empty is a Python CLI for conveniently emptying an AWS S3 bucket.

This tool is useful when you want to delete all objects in a bucket before deleting the bucket itself. It handles versioned and non-versioned S3 buckets.

    BucketNotEmpty: The bucket you tried to delete is not empty. You must delete all versions in the bucket.

![S3Empty console screenshot](https://raw.github.com/cliffano/s3empty/master/screenshots/console.jpg "S3Empty console screenshot")

Installation
------------

    pip3 install s3empty

Usage
-----

Run S3Empty with specified bucket name:

    s3empty --bucket-name some-bucket

Run S3Empty with a configuration file containing the bucket names:

    s3empty --conf-file path/to/some-conf-file.yaml

By default, S3Empty will raise an error if the bucket does not exist. However, there will be scenarios where the S3 bucket you want to empty does not exist or no longer exists. You can use the `--allow-inexisting` flag to allow inexisting buckets and S3Empty will display a warning message and exits without raising any error:

    s3empty --bucket-name some-bucket --allow-inexisting

Show help guide:

    s3empty --help

Configuration
-------------

You can specify multiple bucket names in S3Empty configuration file and give it a name with `.yaml` extension, e.g. `some-conf-file.yaml` :

    ---
    bucket_names:
      - some-bucket-1
      - some-bucket-2

And then call S3Empty:

    s3empty --conf-file path/to/some-conf-file.yaml

The configuration file also supports Jinja template where environment variables are available for use. You can give this configuration template a name with `.yaml.j2` extension, e.g. `some-conf-file.yaml.j2` .

For example, if there is an environment variable `ACCOUNT_ID=1234567` , you can specify it in the configuration file:

    ---
    bucket_names:
      - some-{{ env.ACCOUNT_ID }}-bucket-1
      - some-{{ env.ACCOUNT_ID }}-bucket-2

And then call S3Empty:

    s3empty --conf-file path/to/some-conf-file.yaml.j2

Permission
----------

Here's an IAM policy with minimum permissions required by S3Empty:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3EmptyPolicy",
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketVersioning",
                "s3:ListBucket",
                "s3:ListBucketVersions",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
            ],
            "Resource": [
                "arn:aws:s3:::some-bucket",
                "arn:aws:s3:::some-bucket/*"
            ]
        }
    ]
}
```

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/s3empty/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/s3empty/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/s3empty/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/s3empty/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/s3empty/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/s3empty/doc/sphinx/index.html)
