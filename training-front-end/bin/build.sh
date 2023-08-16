#/bin/bash

set -e

echo $BRANCH

case "$BRANCH" in
main)
    MODE="production" ;;
staging)
    MODE="staging" ;;
dev)
    MODE="dev" ;;
*)
    MODE="dev" ;;
esac

echo "building for:"
echo $MODE

astro build  --mode $MODE