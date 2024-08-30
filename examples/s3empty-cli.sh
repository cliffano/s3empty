#!/usr/bin/env bash
set -o nounset

echo "\n\n========================================"
echo "Show help guide: s3empty --help"
s3empty --help

echo "\n\n========================================"
echo "Run command with default config file: s3empty"
s3empty

echo "\n\n========================================"
echo "Run command with specified bucket name:"
echo "s3empty --bucket-name some-bucket"
s3empty --bucket-name some-bucket
