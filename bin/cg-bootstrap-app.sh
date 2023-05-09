#!/usr/bin/env bash

# Bootstraps the app in a given space in cloud.gov

set -e

if [ -z "$1" ] ; then
  echo "Usage: $0 SPACE"
  exit 1
fi

org="gsa-smartpay"
space=$1

cf target -o ${org} -s ${space}

# Create the app but don't start it yet
cf push --no-start --vars-file manifest-vars.${space}.yml
