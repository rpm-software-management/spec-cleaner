#!/bin/bash
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

for i in $(curl -s https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json | jq -r '.licenses | .[] | select(.isDeprecatedLicenseId|not) | .licenseId'); do
    echo "$i" >> license_exceptions.ntxt ;
done

sort -u -o data/licenses_exceptions.txt license_exceptions.ntxt
rm license_exceptions.ntxt

(
cat README.md.in 
echo ""
echo "# [SPDX Licenses](http://spdx.org/licenses)"
echo ""
echo "License Tag | Description"
echo "----------- | -----------"
IFS=:
w3m -dump -cols 1000 http://spdx.org/licenses/ | grep "License Text" | sed -e 's, *License Text.*, LT,; s,Y\s*LT$,LT,; s,Y\s*LT$,LT,;  s,\s*LT$,,;; s,\s* \([^ ]*\)$,:\1,' | while read text license; do
  echo "$license | $text"
  echo "$license" >> licenses_changes.raw
done
unset IFS

echo ""
echo "# SPDX Exceptions"
echo ""
echo "|Exception name|"
echo "|--------------|"
cat data/licenses_exceptions.txt

echo ""
echo "# SUSE Additions"
echo ""
echo "|License Tag|"
echo "|-----------|"

IFS=:
grep ^SUSE- licenses_changes.ntxt | cut -d'	' -f1 | sort -u | while read -r nl; do 
  echo "|$nl|"
done
unset IFS

rm licenses_changes.raw
) > README.md

cat licenses_changes.ntxt licenses_changes.ptxt | sort -u -o data/licenses_changes.txt
rm licenses_changes.ntxt licenses_changes.ptxt

