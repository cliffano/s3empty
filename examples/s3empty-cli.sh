#!/usr/bin/env bash
set -o nounset

printf "\n\n========================================\n"
printf "Show help guide:\n"
s3empty --help

printf "\n\n========================================\n"
printf "Run command with default config file:\n"
s3empty

printf "\n\n========================================\n"
printf "Run command without permission:\n"
AWS_PROFILE=studio-tester s3empty --bucket-name some-bucket

printf "\n\n****************************************\n"
printf "Assume studio-s3empty role:\n"
export AWS_DEFAULT_REGION=ap-southeast-2
ACCOUNT_ID=$(AWS_PROFILE=studio-tester aws sts get-caller-identity --query Account --output text)
export $(python -m aws_assume_role_lib arn:aws:iam::${ACCOUNT_ID}:role/studio-s3empty --profile studio-tester --env)

printf "\n\n========================================\n"
printf "Run command with bucket having versioning enabled:\n"
s3empty --bucket-name studio-s3empty-with-versioning

printf "\n\n========================================\n"
printf "Second run command with bucket having versioning enabled when bucket is already emptied:\n"
s3empty --bucket-name studio-s3empty-with-versioning

printf "\n\n========================================\n"
printf "Run command with bucket not having versioning enabled:\n"
s3empty --bucket-name studio-s3empty-without-versioning

printf "\n\n========================================\n"
printf "Second run command with bucket not having versioning enabled when bucket is already emptied:\n"
s3empty --bucket-name studio-s3empty-without-versioning

printf "\n\n========================================\n"
printf "Run command with inexisting bucket:\n"
s3empty --bucket-name studio-s3empty-inexisting

printf "\n\n========================================\n"
printf "Run command with inexisting bucket being allowed:\n"
s3empty --bucket-name studio-s3empty-inexisting --allow-inexisting

printf "\n\n========================================\n"
printf "Run command with configuration file containing inexisting buckets:\n"
s3empty --conf-file s3empty-conf-inexisting.yaml --allow-inexisting

printf "\n\n========================================\n"
printf "Run command with configuration file:\n"
s3empty --conf-file s3empty-conf.yaml

printf "\n\n========================================\n"
printf "Run command with configuration template file:\n"
STUDIO_ID=studio s3empty --conf-file s3empty-conf.yaml.j2

printf "\n\n========================================\n"
printf "Run command with combination of bucket and configuration file:\n"
s3empty --bucket-name studio-s3empty-with-versioning --conf-file s3empty-conf.yaml

printf "\n\n========================================\n"
printf "Run command with debug log level:\n"
s3empty --conf-file s3empty-conf.yaml --log-level debug
