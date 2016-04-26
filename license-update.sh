#!/bin/bash
export LC_ALL=C
curl -s 'https://docs.google.com/spreadsheets/d/14AdaJ6cmU0kvQ4ulq9pWpjdZL5tkR03exRSYJmPGdfs/export?format=tsv&id=14AdaJ6cmU0kvQ4ulq9pWpjdZL5tkR03exRSYJmPGdfs&gid=0' | grep -v "New format" \
  | sed -e 's,\s*$,,' > licenses_changes.ntxt

: > licenses_changes.ptxt
grep ^SUSE- licenses_changes.ntxt | cut -d'	' -f1 | while read -r l; do
  echo "$l+	$l+" >> licenses_changes.ptxt ; 
done

for i in $(w3m -dump -cols 1000 http://spdx.org/licenses/ | grep "License Text" | sed -e 's, *Y *License Text,,; s, *License Text,,; s,.* ,,;'); do 
	echo "$i	$i" >> licenses_changes.ntxt ; 
	echo "$i+	$i+" >> licenses_changes.ptxt ;
done
IFS=:
dups=$(tr '	' ':' < licenses_changes.ntxt | while read -r nl ol; do echo "$nl"; done | sed -e 's,^,B-,; s,B-SUSE-,A-,' | sort | uniq | sed -e 's,^.-,,' | sort | uniq -d)
if test -n "$dups"; then 
  echo "DUPS $dups"
  exit 1
fi
dups=$(tr '	' ':' < licenses_changes.ntxt | while read -r nl ol; do echo "$ol"; done | sort | uniq -d)
unset IFS
if test -n "$dups"; then 
  echo "DUPS $dups"
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
w3m -dump -cols 1000 http://spdx.org/licenses/ | grep "License Text" | sed -e 's, *Y *License Text,,; s, *License Text,,; s,\s* \([^ ]*\)$,:\1,' | while read -r text license; do
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
grep ^SUSE- licenses_changes.ntxt | cut -d'	' -f1 | sort -u | while read -r nl; do 
  echo "|$nl|"
done
unset IFS

rm licenses_changes.raw
) > README.md

for i in `w3m -dump -cols 1000 http://spdx.org/licenses/exceptions-index.html | grep "License Exception Text" | sed -e 's, *Y *License Exception Text,,; s, *License Exception Text,,; s,\s* \([^ ]*\)$,:\1,' | cut -d: -f2`; do
    echo "$i" >> license_exceptions.ntxt ;
done

cat license_exceptions.ntxt | sort -u -o data/licences_exceptions.txt
rm license_exceptions.ntxt

cat licenses_changes.ntxt licenses_changes.ptxt | sort -u -o licenses_changes.stxt
( echo "First line" ; cat licenses_changes.stxt ) > data/licenses_changes.txt
rm licenses_changes.ntxt licenses_changes.stxt licenses_changes.ptxt

