#!/usr/bin/env bash

# Rotates the credentials for a cloud.gov deployer service account
# https://cloud.gov/docs/services/cloud-gov-service-account/#rotating-credentials

if [ -z "$1" ] ; then
  echo "Usage: $0 SPACE"
  exit 1
fi

org="gsa-smartpay"
space=$1

cf target -o ${org} -s ${space}
cf delete-service-key ${space}-deployer ${space}-deployer-key
cf create-service-key ${space}-deployer ${space}-deployer-key
cf service-key ${space}-deployer ${space}-deployer-key
