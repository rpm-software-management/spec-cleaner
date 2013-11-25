#!/usr/bin/env bash

verify_fetch() {
    if [[ -z ${1} ]]; then
        echo "Specify the URL to verify"
        exit 1
    fi
    local curl=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' "${1}")
    if [[ ! ( ${curl} == 302 || ${curl} == 200 ) ]]; then
        echo "Unable to download the repodata from \"${1}\""
        exit 1
    fi
}

if [[ -z $1 ]]; then
    echo "Specify the distribution version: \"13.1\""
    exit 1
fi

TEMPDIR="$(mktemp -d)"
TMP="$(mktemp)"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
URL="http://download.opensuse.org/distribution/${1}/repo/oss/suse/"

#echo "Working in \"${TEMPDIR}\""
pushd "${TEMPDIR}" &> /dev/null
    #echo
    #echo "Downloading repomd.xml file..."
    verify_fetch "${URL}repodata/repomd.xml"
    wget "${URL}repodata/repomd.xml" -O repomd.xml > /dev/null

    PRIMARY="${URL}$(grep primary.xml.gz repomd.xml |awk -F'"' '{print $2}')"
    rm repomd.xml

    #echo
    #echo "Downloading primary.xml..."
    verify_fetch "${PRIMARY}"
    wget "${PRIMARY}" -O primary.xml.gz > /dev/null

    #echo
    #echo "Generating pkgconfig_conversions.txt..."
    zcat primary.xml.gz > "$TMP"
    sed -nf "${DIR}"/pkgconfig-update.sed "$TMP" | sort | uniq
popd &> /dev/null

rm -rf ${TEMPDIR}
