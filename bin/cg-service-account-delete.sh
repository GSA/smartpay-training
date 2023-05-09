#!/usr/bin/env bash

# Deletes the cloud.gov deployer service account from a given space
# https://cloud.gov/docs/services/cloud-gov-service-account/

set -e

if [ -z "$1" ] ; then
  echo "Usage: $0 SPACE"
  exit 1
fi

org="gsa-smartpay"
space=$1

cf target -o ${org} -s ${space}
cf delete-service-key ${space}-deployer ${space}-deployer-key
cf delete-service ${space}-deployer
