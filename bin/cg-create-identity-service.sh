#!/usr/bin/env bash

# Creates an OAuth provider service in cloud.gov

set -e

if [ -z "$2" ] ; then
  echo "Usage: $0 SPACE FRONT_END_BASE_URL"
  echo
  echo "Example: $0 prod https://training.smartpay.gsa.gov"
  exit 1
fi

org="gsa-smartpay"
app_name="smartpay-training"
space=$1
redirect_url=${2%/}/auth_callback
post_logout_url=${2%/}
service_instance_name="smartpay-training-oauth-client"
service_key_name="smartpay-training-oauth-key"

echo "Creating identity provider service in space: $space"
echo "Service instance name: ${service_instance_name}"
echo "Service key name: ${service_key_name}"
echo "Redirect URL: ${redirect_url}"
echo "Post-logout URL: ${post_logout_url}"
echo

cf target -o ${org} -s ${space}

# Create identity provider
cf create-service cloud-gov-identity-provider oauth-client ${service_instance_name}

# Create service key
cf create-service-key smartpay-training-oauth-client ${service_key_name} \
    -c "{\"redirect_uri\": [\"${redirect_url}\", \"${post_logout_url}\"]}"

echo If needed, you can retrieve the client_id and client_secret with:
echo cf service-key smartpay-training-oauth-client ${service_key_name}
