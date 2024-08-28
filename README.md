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

Installation
------------

    pip3 install s3empty

Usage
-----

Run s3empty with specified bucket name:

    s3empty --bucket-name some-bucket

Show help guide:

    s3empty --help

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
