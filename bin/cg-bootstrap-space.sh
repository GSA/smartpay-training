#!/usr/bin/env bash

# Bootstraps a given space in cloud.gov

set -e

if [ -z "$1" ] ; then
  echo "Usage: $0 SPACE"
  exit 1
fi

org="gsa-smartpay"
app_name="smartpay-training"
space=$1

if [[ "$space" == "prod" || "$space" == "staging" ]]; then
  rds_plan="large-gp-psql-redundant"
  redis_plan="redis-3node"
else
  rds_plan="small-psql"
  redis_plan="redis-dev"
fi

echo "Bootstrapping space: $space"
echo "Using RDS plan: $rds_plan"
echo "Using Redis plan: $redis_plan"
echo

cf target -o ${org} -s ${space}

# Egress security groups
# The `trusted_local_networks_egress` security group allows the app to connect
# to cloud.gov marketplace services such as Redis and RDS. The
# `public_networks_egress` security group allows the app to connect to external
# SMTP servers.
cf bind-security-group trusted_local_networks_egress $org --space $space
cf bind-security-group public_networks_egress $org --space $space

# Services
cf create-service aws-elasticache-redis $redis_plan smartpay-training-redis
cf create-service aws-rds $rds_plan smartpay-training-db

# Secrets
cf create-user-provided-service smartpay-training-secrets
