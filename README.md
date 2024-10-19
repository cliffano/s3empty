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

![S3Empty console screenshot](screenshots/console.jpg "S3Empty console screenshot")

Installation
------------

    pip3 install s3empty

Usage
-----

Run S3Empty with specified bucket name:

    s3empty --bucket-name some-bucket

Show help guide:

    s3empty --help

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
