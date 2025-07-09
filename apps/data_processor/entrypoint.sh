#!/usr/bin/env bash
set -e

# dump all env vars except no_proxy, and prefix with "export "
printenv \
  | grep -v '^no_proxy=' \
  | sed 's/^/export /' \
  > /container_env.sh

chmod 0644 /container_env.sh
cron -f
