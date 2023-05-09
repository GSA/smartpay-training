#!/usr/bin/env bash

# Sets secrets in cloud.gov

set -e

if [ -z "$3" ] ; then
  echo "Usage: $0 SPACE SECRET_NAME SECRET_VALUE"
  exit 1
fi

org="gsa-smartpay"
app_name="smartpay-training"
ups_name="${app_name}-secrets"
space="$1"
secret_name="$2"
secret_value="$3"

cf target -o ${org} -s ${space}

app_guid=$(cf app --guid $app_name)
env=$(cf curl "/v2/apps/$app_guid/env")
credentials=$(echo $env | jq --arg ups_name $ups_name '.system_env_json.VCAP_SERVICES."user-provided"[] | select(.name == $ups_name) | .credentials')
new_credentials=$(echo $credentials | jq -r --arg secret_name "$secret_name" --arg secret_value "$secret_value" 'if ."$secret_name" then "$secret_name" = "$secret_value" else . + { ($secret_name): ($secret_value) } end')

tmpfile=$(mktemp)
echo $new_credentials > $tmpfile
cf uups smartpay-training-secrets -p $tmpfile
rm $tmpfile
