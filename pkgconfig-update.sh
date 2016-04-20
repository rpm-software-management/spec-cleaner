#!/bin/bash
fetch() {
    local status
    status="$(curl -o /dev/null -LsIw '%{http_code}' "$1" 2>&1)"
    if [ "$status" != 200 ]; then
        echo >&2 "Unable to download the repodata from \"$1\": $status"
        exit 1
    fi
    curl -#L "$1"
}

if [ -z "$1" ]; then
    echo "Specify the distribution version, e.g. \"13.1\""
    exit 1
fi

BASEURL="http://download.opensuse.org/distribution/$1/repo/oss/suse/"
fetch "${BASEURL}$(fetch "${BASEURL}repodata/repomd.xml" \
    | perl -ne 'print $1 if /"(.*?primary.xml.gz)"/')" \
    | zcat | perl "$(cd "$(dirname $0)" && pwd)/pkgconfig-update.pl"
