#! /bin/sh

# this script is maintained here: https://github.com/openSUSE/obs-service-format_spec_file
# SPDX-License-Identifier: GPL-2.0-or-later

set -e

export LC_ALL=C
curl -s -L 'https://docs.google.com/spreadsheets/d/14AdaJ6cmU0kvQ4ulq9pWpjdZL5tkR03exRSYJmPGdfs/export?format=tsv&id=14AdaJ6cmU0kvQ4ulq9pWpjdZL5tkR03exRSYJmPGdfs&gid=0' | grep -v "New format" \
  | sed -e 's,\s*$,,' > licenses_changes.ntxt

: > licenses_changes.ptxt
grep ^SUSE- licenses_changes.ntxt | cut -d'	' -f1 | while read -r l; do
  echo "$l	$l" >> licenses_changes.ptxt ;
  # add + only to non or-later ones, otheriwse add the +
  if [[ ${l/-or-later/} == ${l} ]]; then
    echo "$l+	$l+" >> licenses_changes.ptxt ;
  else
    echo "$l	${l/-or-later/}+" >> licenses_changes.ptxt ;
  fi
done

for i in $(curl -s https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json | jq -r '.licenses | .[] | select(.isDeprecatedLicenseId|not) | .licenseId'); do
  echo "$i	$i" >> licenses_changes.ntxt ;
  echo "$i+	$i+" >> licenses_changes.ntxt ;
  # For these that can be "or later" generate also replacement of + SPDX-2.0
  if [[ ${i/-or-later/} != ${i} ]]; then
    echo "$i	${i/-or-later/}+" >> licenses_changes.ntxt ;
  fi
  # replace old -only without the name
  if [[ ${i/-only/} != ${i} ]]; then
    echo "$i	${i/-only/}" >> licenses_changes.ntxt ;
  fi
done
IFS=:
dups=$(tr '	' ':' < licenses_changes.ntxt | while read -r nl ol; do echo "$nl"; done | sed -e 's,^,B-,; s,B-SUSE-,A-,' | sort | uniq | sed -e 's,^.-,,' | sort | uniq -d)
if test -n "$dups"; then 
  echo "SUSE DUPS $dups"
  exit 1
fi

: > licenses_changes.raw
(
cat README.md.in
echo ""
echo "# [SPDX Licenses](http://spdx.org/licenses)"
echo ""
echo "License Tag | Description"
echo "----------- | -----------"
IFS=:
curl -s https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json | jq -r '.licenses | .[] | select(.isDeprecatedLicenseId|not) | [.licenseId, ":", .name] | add' | sort | while read license text; do
  echo "$license | $text"
  echo "$license" >> licenses_changes.raw
done
unset IFS

echo ""
echo "# SUSE Additions"
echo ""
echo "|License Tag|"
echo "|-----------|"

IFS=:
grep -E "^(LicenseRef-SUSE-|SUSE-)" licenses_changes.ntxt | cut -d'	' -f1 | sort -u | while read nl; do
  echo "|$nl|"
done
unset IFS

rm licenses_changes.raw
) > README.md

cat licenses_changes.ntxt licenses_changes.ptxt | sort -u -o spec_cleaner/data/licenses_changes.txt
rm licenses_changes.ntxt licenses_changes.ptxt

