#!/usr/bin/env bash
set -o nounset

printf "\n\n========================================\n"
echo "Show help guide: s3empty --help"
s3empty --help

printf "\n\n========================================\n"
echo "Run command with default config file: s3empty"
s3empty

printf "\n\n========================================\n"
echo "Run command without permission:"
echo "s3empty --bucket-name some-bucket"
AWS_PROFILE=studio-tester s3empty --bucket-name some-bucket

export AWS_DEFAULT_REGION=ap-southeast-2
ACCOUNT_ID=$(AWS_PROFILE=studio-tester aws sts get-caller-identity --query Account --output text)
export $(python -m aws_assume_role_lib arn:aws:iam::${ACCOUNT_ID}:role/studio-s3empty --profile studio-tester --env)

printf "\n\n========================================\n"
echo "Run command with bucket having versioning enabled:"
echo "s3empty --bucket-name studio-s3empty-with-versioning"
s3empty --bucket-name studio-s3empty-with-versioning

printf "\n\n========================================\n"
echo "Second run command with bucket having versioning enabled when bucket is already emptied:"
echo "s3empty --bucket-name studio-s3empty-with-versioning"
s3empty --bucket-name studio-s3empty-with-versioning

printf "\n\n========================================\n"
echo "Run command with bucket not having versioning enabled:"
echo "s3empty --bucket-name studio-s3empty-without-versioning"
s3empty --bucket-name studio-s3empty-without-versioning

printf "\n\n========================================\n"
echo "Second run command with bucket not having versioning enabled when bucket is already emptied:"
echo "s3empty --bucket-name studio-s3empty-without-versioning"
s3empty --bucket-name studio-s3empty-without-versioning
