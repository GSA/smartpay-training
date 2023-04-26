#!/usr/bin/env bash

# Creates a cloud.gov deployer service account for a given space
# https://cloud.gov/docs/services/cloud-gov-service-account/

if [ -z "$1" ] ; then
  echo "Usage: $0 SPACE"
  exit 1
fi

org="gsa-smartpay"
space=$1

cf target -o ${org} -s ${space}
cf create-service cloud-gov-service-account space-deployer ${space}-deployer
cf create-service-key ${space}-deployer ${space}-deployer-key
cf service-key ${space}-deployer ${space}-deployer-key
