#!/usr/bin/env bash

verify_fetch() {
    if [[ -z ${1} ]]; then
        echo "Specify the URL to verify"
        exit 1
    fi
    local curl=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' "${1}")
    if [[ ! ( ${curl} == 302 || ${curl} == 200 ) ]]; then
        echo "Unable to download the data from \"${1}\""
        exit 1
    fi
}

DOCS="https://docs.google.com/spreadsheet/pub?hl=en_US&hl=en_US&key=0AqPp4y2wyQsbdGQ1V3pRRDg5NEpGVWpubzdRZ0tjUWc&single=true&gid=0&output=txt"
SPDX="http://spdx.org/licenses/"
TEMPDIR="$(mktemp -d)"

#echo "Working in \"${TEMPDIR}\""
pushd "${TEMPDIR}" &> /dev/null
    verify_fetch "${DOCS}"
    curl -s "${DOCS}" | grep -v "New format" > licenses_changes.txt
    grep ^SUSE- licenses_changes.txt | awk -F' ' '{print $1}' | while read l; do
        echo -e "${l}+\t${l}+\n" >> licenses_changes.txt
    done

    verify_fetch "${SPDX}"
    for i in `w3m -dump -cols 1000 "${SPDX}" | grep "License Text" | sed -e 's, *Y *License Text,,; s, *License Text,,; s,.* ,,;'`; do
        echo -e "${i}\t${i}\n" >> licenses_changes.txt
        if [[ ${i:-1} != '+' ]] ; then
            echo -e "${i}+\t${i}+\n" >> licenses_changes.txt
        fi
    done
    (
        LC_ALL=C
        sort -o licenses_changes.txt -u licenses_changes.txt
    )
    cat licenses_changes.txt
popd &> /dev/null

rm -rf ${TEMPDIR}
