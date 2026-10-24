#!/bin/bash
# Regenerate one conversion table (cmake, perl, pkgconfig, tex) from the
# distribution repodata and print it to stdout.
#
# The primary.xml archive is downloaded into a staging directory and
# verified against the checksum and size published in repomd.xml before
# anything is generated from it. A download that is truncated or corrupted
# therefore aborts the run -- including one that would still decompress
# cleanly, e.g. an archive cut at a zstd frame boundary or a complete but
# stale file served by a mirror. Without the check such a download turns
# into a silently shortened table, which is how the published tables were
# once damaged (the tex table shipped with 251 of its 4162 lines and was
# only caught by a manual re-download verified against repomd.xml).
# The table is printed only once it has been generated completely, so a
# failed run emits nothing at all and the Makefile keeps the old file.

set -e -o pipefail

if [ -z "$1" ]; then
    echo "You need to specify the name of the resource to grab, e.g. \"cmake\""
    exit 1
fi

if [ -z "$2" ]; then
    echo "Specify the distribution version, e.g. \"leap/42.1\""
    exit 1
fi

BASEURL="https://download.opensuse.org/distribution/$2/repo/oss/"

# Staging directory for the downloads, created in the working directory.
# The archive is only ever decompressed as a stream -- the decompressed
# primary.xml is far too large to stage on disk, and /tmp is a small
# tmpfs on some systems.
WORKDIR="$(mktemp -d "$(pwd)/.conversions-update.XXXXXX")"
trap 'rm -rf "$WORKDIR"' EXIT

curl -#fL -o "$WORKDIR/repomd.xml" "${BASEURL}repodata/repomd.xml"

# repomd.xml publishes the location, checksum and size of the primary
# metadata; extract all three so the download can be verified against them.
read -r ARCHIVE CHECKSUM SIZE < <(perl -0777 -ne '
    if (/<data type="primary">(.*?)<\/data>/s) {
        my $block = $1;
        my ($href) = $block =~ /<location href="([^"]*primary\.xml\.(?:gz|zst))"/;
        my ($type, $sum) = $block =~ /<checksum type="(sha256|sha512)">([0-9a-f]+)<\/checksum>/;
        my ($size) = $block =~ /<size>(\d+)<\/size>/;
        print "$href $type:$sum $size\n" if $href;
    }' "$WORKDIR/repomd.xml") || true

if [ -z "$ARCHIVE" ]; then
    echo >&2 "Unable to find primary.xml in the repodata of \"$BASEURL\""
    exit 1
fi
CHECKSUM_TYPE="${CHECKSUM%%:*}"
CHECKSUM_VALUE="${CHECKSUM##*:}"
if [ -z "$CHECKSUM_VALUE" ]; then
    echo >&2 "repomd.xml of \"$BASEURL\" publishes no sha256/sha512 checksum for primary.xml"
    exit 1
fi

curl -#fL -o "$WORKDIR/primary.xml.archive" "${BASEURL}${ARCHIVE}"

if [ -n "$SIZE" ]; then
    DOWNLOADED_SIZE="$(wc -c < "$WORKDIR/primary.xml.archive" | tr -d ' ')"
    if [ "$DOWNLOADED_SIZE" != "$SIZE" ]; then
        echo >&2 "Size mismatch for $ARCHIVE: repomd.xml announces $SIZE bytes, got $DOWNLOADED_SIZE"
        exit 1
    fi
fi

case "$CHECKSUM_TYPE" in
    sha512) SUMTOOL="sha512sum" ;;
    sha256) SUMTOOL="sha256sum" ;;
    *)
        echo >&2 "Unsupported checksum type \"$CHECKSUM_TYPE\" in repomd.xml of \"$BASEURL\""
        exit 1
        ;;
esac
DOWNLOADED_SUM="$("$SUMTOOL" "$WORKDIR/primary.xml.archive" | cut -d' ' -f1)"
if [ "$DOWNLOADED_SUM" != "$CHECKSUM_VALUE" ]; then
    echo >&2 "Checksum mismatch for $ARCHIVE: repomd.xml announces $CHECKSUM_VALUE, got $DOWNLOADED_SUM"
    exit 1
fi
echo >&2 "Verified $ARCHIVE against the $CHECKSUM_TYPE checksum in repomd.xml"

# Newer distributions (Leap 16 and later) compress repodata with zstd
# instead of gzip, so decompress accordingly.
case "$ARCHIVE" in
    *.zst) DECOMPRESS="zstd -dc" ;;
    *)     DECOMPRESS="zcat" ;;
esac

$DECOMPRESS "$WORKDIR/primary.xml.archive" \
    | perl "$(cd "$(dirname "$0")" && pwd)/conversions-update.pl" "$1" \
    > "$WORKDIR/conversions.txt"

if [ ! -s "$WORKDIR/conversions.txt" ]; then
    echo >&2 "Generating the $1 conversions from $ARCHIVE produced no output"
    exit 1
fi
cat "$WORKDIR/conversions.txt"
