#!/usr/bin/env bash

# Sets environment variables in cloud.gov

if [ -z "$1" ] ; then
  echo "Usage: $0 SPACE [VAR_NAME=value ...]"
  exit 1
fi

org="gsa-smartpay"
app_name="smartpay-training"
space=$1

cf target -o ${org} -s ${space}

for arg in "${@:2}" ; do
  env_name="$(echo $arg | cut -f1 -d'=')"
  env_value="$(echo $arg | cut -f2- -d'=')"
  cf set-env $app_name $env_name "$env_value"
done
