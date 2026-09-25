#!/bin/bash
set -o pipefail

fetch() {
    local status
    status="$(curl -o /dev/null -LsIw '%{http_code}' "$1" 2>&1)"
    if [ "$status" != 200 ]; then
        echo >&2 "Unable to download the repodata from \"$1\": $status"
        exit 1
    fi
    curl -#fL "$1"
}

if [ -z "$1" ]; then
    echo "You need to specify the name of the resource to grab, e.g. \"cmake\""
    exit 1
fi

if [ -z "$2" ]; then
    echo "Specify the distribution version, e.g. \"leap/42.1\""
    exit 1
fi

BASEURL="http://download.opensuse.org/distribution/$2/repo/oss/"
# Newer distributions (Leap 16 and later) compress repodata with zstd
# instead of gzip, so match either and decompress accordingly.
ARCHIVE="$(fetch "${BASEURL}repodata/repomd.xml" \
    | perl -ne 'print $1 if /"(.*?primary\.xml\.(gz|zst))"/')"
if [ -z "$ARCHIVE" ]; then
    echo >&2 "Unable to find primary.xml in the repodata of \"$BASEURL\""
    exit 1
fi
case "$ARCHIVE" in
    *.zst) DECOMPRESS="zstd -dc" ;;
    *)     DECOMPRESS="zcat" ;;
esac
fetch "${BASEURL}${ARCHIVE}" \
    | $DECOMPRESS | perl "$(cd "$(dirname $0)" && pwd)/conversions-update.pl" $1
