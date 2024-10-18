#!/usr/bin/env bash
set -o nounset

echo "\n\n========================================"
echo "Show help guide: s3empty --help"
s3empty --help

echo "\n\n========================================"
echo "Run command with default config file: s3empty"
s3empty

export AWS_DEFAULT_REGION=ap-southeast-2
ACCOUNT_ID=$(AWS_PROFILE=studio-tester aws sts get-caller-identity --query Account --output text)
export $(python -m aws_assume_role_lib arn:aws:iam::${ACCOUNT_ID}:role/studio-s3empty --profile studio-tester --env)

echo "\n\n========================================"
echo "Run command with bucket having versioning enabled:"
echo "s3empty --bucket-name studio-s3empty-with-versioning"
s3empty --bucket-name studio-s3empty-with-versioning

echo "\n\n========================================"
echo "Run command with bucket not having versioning enabled:"
echo "s3empty --bucket-name studio-s3empty-without-versioning"
s3empty --bucket-name studio-s3empty-without-versioning
