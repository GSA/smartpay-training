#!/usr/bin/env bash

echo "Generating SSL certificate..."

set -euo pipefail

openssl req \
  -new -x509 -days 3650 -nodes \
  -subj /CN=localhost \
  -out /var/lib/postgresql/server.crt \
  -keyout /var/lib/postgresql/server.key

chown postgres:postgres /var/lib/postgresql/server.{crt,key}
chmod 600 /var/lib/postgresql/server.{crt,key}
