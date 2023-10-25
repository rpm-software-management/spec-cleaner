
# spec-cleaner

![Build Status](https://github.com/rpm-software-management/spec-cleaner/workflows/Python%20package/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/rpm-software-management/spec-cleaner/badge.svg?branch=master)](https://coveralls.io/github/rpm-software-management/spec-cleaner?branch=master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/rpm-software-management/spec-cleaner.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/rpm-software-management/spec-cleaner/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/rpm-software-management/spec-cleaner.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/rpm-software-management/spec-cleaner/context:python)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


spec-cleaner is a tool that cleans the given RPM spec file according to the style guide and returns the result.

It's used for [openSUSE](https://www.opensuse.org), where it's planned to be a replacement for `osc service localrun format_spec_file` and it is intended to provide the same or better features in order to be able to unify all the spec files in [OBS](https://build.opensuse.org/).

# Table of contents
* [Installation and usage](#installation-and-usage)
* [Tests](#tests)
* [Contributing](#contributing)
* [Versioning and releasing](#versioning-and-releasing)
* [Authors](#authors)

## Installation and usage

### Installation
The latest version is available on [PyPI](https://pypi.org/project/spec_cleaner/). It can be installed by running `pip install spec_cleaner`.

spec-cleaner is also provided as an RPM package for openSUSE Leap ([15.0](https://build.opensuse.org/package/show/openSUSE:Leap:15.0:Update/spec-cleaner) and [15.1](https://build.opensuse.org/package/show/openSUSE:Leap:15.1:Update/spec-cleaner)) and [openSUSE Tumbleweed](https://build.opensuse.org/package/show/openSUSE:Factory/spec-cleaner). When the new version of spec-cleaner is released then the version updates are performed for all maintained openSUSE codestreams. That means that there is always the latest version available in openSUSE:Leap.

### Usage
Simply run `spec-cleaner -i <specfile>` to clean your specfile up.


## Tests

### Running the tests
spec-cleaner provides quite an extensive testsuite. You can run these tests locally either directly via `pytest`.

#### pytest
Just install `python3-pytest`, `python3-pytest-cov`, `python3-pytest-isort` and `python3-pytest-sugar` (for a nice progress bar) and then run all tests via:

    pytest

## Contributing
You are more than welcome to contribute to this project. If you are not sure about your changes, feel free to create an issue where you can discuss it before the implementation.

### Contribution Guidelines

When changing anything in the code, make sure that you don't forget to:

  * Follow [pep8](https://www.python.org/dev/peps/pep-0008/).
  * Install [pre-commit](https://pre-commit.com/) framework and run `pre-commit install` to install `pre-commit` into your git hooks.
  * Add proper comments and docstrings (follow [pep257](https://www.python.org/dev/peps/pep-0257/) and [Google Python Style Guide for docstrings and comments](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings))
  * Add [tests](TESTSUITE.md) (mainly if you implement a new feature).
  * Add `mypy` support for the new code.
  * Run and pass all tests, `flake8` and `mypy` checks.

See below for more details.

### pre-commit

spec-cleaner project adopted `pre-commit` framework for managing and maintaining pre-commit hooks. After you clone the spec-cleaner repository, please install [pre-commit](https://pre-commit.com/) framework (`pip install pre-commit`) and run `pre-commit install` to install `pre-commit` into your git hooks. Then `pre-commit` will run automatically on `git commit` and it will check your contribution with `isort`, `black`, `flake8`, `flake8-docstrings` and `mypy`.

Please note that similar checks run in CI when you submit a PR and it won't pass code review without passing these checks.

### mypy

Optional static type checker support was implemented for the most important parts of the code. If you want to run it on your own, just install `python3-mypy` and run

     mypy spec_cleaner

### Black

The code of spec-cleaner is formated with [Black](https://github.com/psf/black). We use `--skip-string-normalization` and `--line-length 100` options. Black runs automatically in the `pre-commit` hook.

### Adding new tests
When a new feature is added to spec-cleaner then a test for this piece of code must be added. See [how to write tests for spec-cleaner](TESTSUITE.md).


## Versioning and releasing
For the versions available, see the [tags on this repository](https://github.com/openSUSE/spec-cleaner/releases).

If you have proper permissions you can find handy [how to do a new release](RELEASE.md).

## Authors

* See the list of [contributors](AUTHORS) who participated in this project


# [SPDX Licenses](http://spdx.org/licenses)

License Tag | Description
----------- | -----------

# SPDX Exceptions

|Exception name|
|--------------|
0BSD
AAL
ADSL
AFL-1.1
AFL-1.2
AFL-2.0
AFL-2.1
AFL-3.0
AGPL-1.0-only
AGPL-1.0-or-later
AGPL-3.0-only
AGPL-3.0-or-later
AMDPLPA
AML
AMPAS
ANTLR-PD
ANTLR-PD-fallback
APAFML
APL-1.0
APSL-1.0
APSL-1.1
APSL-1.2
APSL-2.0
ASWF-Digital-Assets-1.0
ASWF-Digital-Assets-1.1
Abstyles
AdaCore-doc
Adobe-2006
Adobe-Glyph
Adobe-Utopia
Afmparse
Aladdin
Apache-1.0
Apache-1.1
Apache-2.0
App-s2p
Arphic-1999
Artistic-1.0
Artistic-1.0-Perl
Artistic-1.0-cl8
Artistic-2.0
BSD-1-Clause
BSD-2-Clause
BSD-2-Clause-Patent
BSD-2-Clause-Views
BSD-3-Clause
BSD-3-Clause-Attribution
BSD-3-Clause-Clear
BSD-3-Clause-HP
BSD-3-Clause-LBNL
BSD-3-Clause-Modification
BSD-3-Clause-No-Military-License
BSD-3-Clause-No-Nuclear-License
BSD-3-Clause-No-Nuclear-License-2014
BSD-3-Clause-No-Nuclear-Warranty
BSD-3-Clause-Open-MPI
BSD-3-Clause-Sun
BSD-3-Clause-flex
BSD-4-Clause
BSD-4-Clause-Shortened
BSD-4-Clause-UC
BSD-4.3RENO
BSD-4.3TAHOE
BSD-Advertising-Acknowledgement
BSD-Attribution-HPND-disclaimer
BSD-Inferno-Nettverk
BSD-Protection
BSD-Source-Code
BSD-Systemics
BSL-1.0
BUSL-1.1
Baekmuk
Bahyph
Barr
Beerware
BitTorrent-1.0
BitTorrent-1.1
Bitstream-Charter
Bitstream-Vera
BlueOak-1.0.0
Boehm-GC
Borceux
Brian-Gladman-3-Clause
C-UDA-1.0
CAL-1.0
CAL-1.0-Combined-Work-Exception
CATOSL-1.1
CC-BY-1.0
CC-BY-2.0
CC-BY-2.5
CC-BY-2.5-AU
CC-BY-3.0
CC-BY-3.0-AT
CC-BY-3.0-DE
CC-BY-3.0-IGO
CC-BY-3.0-NL
CC-BY-3.0-US
CC-BY-4.0
CC-BY-NC-1.0
CC-BY-NC-2.0
CC-BY-NC-2.5
CC-BY-NC-3.0
CC-BY-NC-3.0-DE
CC-BY-NC-4.0
CC-BY-NC-ND-1.0
CC-BY-NC-ND-2.0
CC-BY-NC-ND-2.5
CC-BY-NC-ND-3.0
CC-BY-NC-ND-3.0-DE
CC-BY-NC-ND-3.0-IGO
CC-BY-NC-ND-4.0
CC-BY-NC-SA-1.0
CC-BY-NC-SA-2.0
CC-BY-NC-SA-2.0-DE
CC-BY-NC-SA-2.0-FR
CC-BY-NC-SA-2.0-UK
CC-BY-NC-SA-2.5
CC-BY-NC-SA-3.0
CC-BY-NC-SA-3.0-DE
CC-BY-NC-SA-3.0-IGO
CC-BY-NC-SA-4.0
CC-BY-ND-1.0
CC-BY-ND-2.0
CC-BY-ND-2.5
CC-BY-ND-3.0
CC-BY-ND-3.0-DE
CC-BY-ND-4.0
CC-BY-SA-1.0
CC-BY-SA-2.0
CC-BY-SA-2.0-UK
CC-BY-SA-2.1-JP
CC-BY-SA-2.5
CC-BY-SA-3.0
CC-BY-SA-3.0-AT
CC-BY-SA-3.0-DE
CC-BY-SA-3.0-IGO
CC-BY-SA-4.0
CC-PDDC
CC0-1.0
CDDL-1.0
CDDL-1.1
CDL-1.0
CDLA-Permissive-1.0
CDLA-Permissive-2.0
CDLA-Sharing-1.0
CECILL-1.0
CECILL-1.1
CECILL-2.0
CECILL-2.1
CECILL-B
CECILL-C
CERN-OHL-1.1
CERN-OHL-1.2
CERN-OHL-P-2.0
CERN-OHL-S-2.0
CERN-OHL-W-2.0
CFITSIO
CMU-Mach
CNRI-Jython
CNRI-Python
CNRI-Python-GPL-Compatible
COIL-1.0
CPAL-1.0
CPL-1.0
CPOL-1.02
CUA-OPL-1.0
Caldera
ClArtistic
Clips
Community-Spec-1.0
Condor-1.1
Cornell-Lossless-JPEG
Cronyx
Crossword
CrystalStacker
Cube
D-FSL-1.0
DL-DE-BY-2.0
DL-DE-ZERO-2.0
DOC
DRL-1.0
DSDP
Dotseqn
ECL-1.0
ECL-2.0
EFL-1.0
EFL-2.0
EPICS
EPL-1.0
EPL-2.0
EUDatagrid
EUPL-1.0
EUPL-1.1
EUPL-1.2
Elastic-2.0
Entessa
ErlPL-1.1
Eurosym
FBM
FDK-AAC
FSFAP
FSFUL
FSFULLR
FSFULLRWD
FTL
Fair
Ferguson-Twofish
Frameworx-1.0
FreeBSD-DOC
FreeImage
Furuseth
GD
GFDL-1.1-invariants-only
GFDL-1.1-invariants-or-later
GFDL-1.1-no-invariants-only
GFDL-1.1-no-invariants-or-later
GFDL-1.1-only
GFDL-1.1-or-later
GFDL-1.2-invariants-only
GFDL-1.2-invariants-or-later
GFDL-1.2-no-invariants-only
GFDL-1.2-no-invariants-or-later
GFDL-1.2-only
GFDL-1.2-or-later
GFDL-1.3-invariants-only
GFDL-1.3-invariants-or-later
GFDL-1.3-no-invariants-only
GFDL-1.3-no-invariants-or-later
GFDL-1.3-only
GFDL-1.3-or-later
GL2PS
GLWTPL
GPL-1.0-only
GPL-1.0-or-later
GPL-2.0-only
GPL-2.0-or-later
GPL-3.0-only
GPL-3.0-or-later
Giftware
Glide
Glulxe
Graphics-Gems
HP-1986
HP-1989
HPND
HPND-DEC
HPND-Markus-Kuhn
HPND-Pbmplus
HPND-UC
HPND-doc
HPND-doc-sell
HPND-export-US
HPND-export-US-modify
HPND-sell-regexpr
HPND-sell-variant
HPND-sell-variant-MIT-disclaimer
HTMLTIDY
HaskellReport
Hippocratic-2.1
IBM-pibs
ICU
IEC-Code-Components-EULA
IJG
IJG-short
IPA
IPL-1.0
ISC
ImageMagick
Imlib2
Info-ZIP
Inner-Net-2.0
Intel
Intel-ACPI
Interbase-1.0
JPL-image
JPNIC
JSON
Jam
JasPer-2.0
Kastrup
Kazlib
Knuth-CTAN
LAL-1.2
LAL-1.3
LGPL-2.0-only
LGPL-2.0-or-later
LGPL-2.1-only
LGPL-2.1-or-later
LGPL-3.0-only
LGPL-3.0-or-later
LGPLLR
LOOP
LPL-1.0
LPL-1.02
LPPL-1.0
LPPL-1.1
LPPL-1.2
LPPL-1.3a
LPPL-1.3c
LZMA-SDK-9.11-to-9.20
LZMA-SDK-9.22
Latex2e
Latex2e-translated-notice
Leptonica
LiLiQ-P-1.1
LiLiQ-R-1.1
LiLiQ-Rplus-1.1
Libpng
Linux-OpenIB
Linux-man-pages-1-para
Linux-man-pages-copyleft
Linux-man-pages-copyleft-2-para
Linux-man-pages-copyleft-var
Lucida-Bitmap-Fonts
MIT
MIT-0
MIT-CMU
MIT-Festival
MIT-Modern-Variant
MIT-Wu
MIT-advertising
MIT-enna
MIT-feh
MIT-open-group
MIT-testregex
MITNFA
MMIXware
MPEG-SSG
MPL-1.0
MPL-1.1
MPL-2.0
MPL-2.0-no-copyleft-exception
MS-LPL
MS-PL
MS-RL
MTLL
MakeIndex
Martin-Birgmeier
McPhee-slideshow
Minpack
MirOS
Motosoto
MulanPSL-1.0
MulanPSL-2.0
Multics
Mup
NAIST-2003
NASA-1.3
NBPL-1.0
NCGL-UK-2.0
NCSA
NGPL
NICTA-1.0
NIST-PD
NIST-PD-fallback
NIST-Software
NLOD-1.0
NLOD-2.0
NLPL
NOSL
NPL-1.0
NPL-1.1
NPOSL-3.0
NRL
NTP
NTP-0
Naumen
Net-SNMP
NetCDF
Newsletr
Nokia
Noweb
O-UDA-1.0
OCCT-PL
OCLC-2.0
ODC-By-1.0
ODbL-1.0
OFFIS
OFL-1.0
OFL-1.0-RFN
OFL-1.0-no-RFN
OFL-1.1
OFL-1.1-RFN
OFL-1.1-no-RFN
OGC-1.0
OGDL-Taiwan-1.0
OGL-Canada-2.0
OGL-UK-1.0
OGL-UK-2.0
OGL-UK-3.0
OGTSL
OLDAP-1.1
OLDAP-1.2
OLDAP-1.3
OLDAP-1.4
OLDAP-2.0
OLDAP-2.0.1
OLDAP-2.1
OLDAP-2.2
OLDAP-2.2.1
OLDAP-2.2.2
OLDAP-2.3
OLDAP-2.4
OLDAP-2.5
OLDAP-2.6
OLDAP-2.7
OLDAP-2.8
OLFL-1.3
OML
OPL-1.0
OPL-UK-3.0
OPUBL-1.0
OSET-PL-2.1
OSL-1.0
OSL-1.1
OSL-2.0
OSL-2.1
OSL-3.0
OpenPBS-2.3
OpenSSL
PADL
PDDL-1.0
PHP-3.0
PHP-3.01
PSF-2.0
Parity-6.0.0
Parity-7.0.0
Plexus
PolyForm-Noncommercial-1.0.0
PolyForm-Small-Business-1.0.0
PostgreSQL
Python-2.0
Python-2.0.1
QPL-1.0
QPL-1.0-INRIA-2004
Qhull
RHeCos-1.1
RPL-1.1
RPL-1.5
RPSL-1.0
RSA-MD
RSCPL
Rdisc
Ruby
SAX-PD
SCEA
SGI-B-1.0
SGI-B-1.1
SGI-B-2.0
SGI-OpenGL
SGP4
SHL-0.5
SHL-0.51
SISSL
SISSL-1.2
SL
SMLNJ
SMPPL
SNIA
SPL-1.0
SSH-OpenSSH
SSH-short
SSPL-1.0
SWL
Saxpath
SchemeReport
Sendmail
Sendmail-8.23
SimPL-2.0
Sleepycat
Soundex
Spencer-86
Spencer-94
Spencer-99
SugarCRM-1.1.3
SunPro
Symlinks
TAPR-OHL-1.0
TCL
TCP-wrappers
TMate
TORQUE-1.1
TOSL
TPDL
TPL-1.0
TTWL
TTYP0
TU-Berlin-1.0
TU-Berlin-2.0
TermReadKey
UCAR
UCL-1.0
UPL-1.0
URT-RLE
Unicode-DFS-2015
Unicode-DFS-2016
Unicode-TOU
UnixCrypt
Unlicense
VOSTROM
VSL-1.0
Vim
W3C
W3C-19980720
W3C-20150513
WTFPL
Watcom-1.0
Widget-Workshop
Wsuipa
X11
X11-distribute-modifications-variant
XFree86-1.1
XSkat
Xdebug-1.03
Xerox
Xfig
Xnet
YPL-1.0
YPL-1.1
ZPL-1.1
ZPL-2.0
ZPL-2.1
Zed
Zeeff
Zend-2.0
Zimbra-1.3
Zimbra-1.4
Zlib
blessing
bzip2-1.0.6
check-cvs
checkmk
copyleft-next-0.3.0
copyleft-next-0.3.1
curl
diffmark
dtoa
dvipdfm
eGenix
etalab-2.0
fwlw
gSOAP-1.3b
gnuplot
iMatix
libpng-2.0
libselinux-1.0
libtiff
libutil-David-Nugent
lsof
magaz
metamail
mpi-permissive
mpich2
mplus
pnmstitch
psfrag
psutils
python-ldap
snprintf
ssh-keyscan
swrule
ulem
w3m
xinetd
xlock
xpp
zlib-acknowledgement

# SUSE Additions

|License Tag|
|-----------|
|SUSE-BSD-3-Clause-with-non-nuclear-addition|
|SUSE-BSD-Mark-Modifications|
|SUSE-CC-Sampling-Plus-1.0|
|SUSE-CPL-0.5|
|SUSE-CacertRoot|
|SUSE-Copyleft-Next-0.3.0|
|SUSE-Curb|
|SUSE-DMTF|
|SUSE-Docbook-XSL|
|SUSE-EULA|
|SUSE-Egenix-1.1.0|
|SUSE-FHS|
|SUSE-FLTK|
|SUSE-Firmware|
|SUSE-Free-Art-1.3|
|SUSE-Freetype|
|SUSE-Freeware|
|SUSE-GL2PS-2.0|
|SUSE-GPL-2.0+-with-openssl-exception|
|SUSE-GPL-2.0+-with-sane-exception|
|SUSE-GPL-2.0-with-FLOSS-exception|
|SUSE-GPL-2.0-with-OSI-exception|
|SUSE-GPL-2.0-with-linking-exception|
|SUSE-GPL-2.0-with-openssl-exception|
|SUSE-GPL-2.0-with-plugin-exception|
|SUSE-GPL-3.0+-with-font-exception|
|SUSE-GPL-3.0+-with-openssl-exception|
|SUSE-GPL-3.0-with-FLOSS-exception|
|SUSE-GPL-3.0-with-font-exception|
|SUSE-GPL-3.0-with-openssl-exception|
|SUSE-GPL-3.0-with-template-exception|
|SUSE-Gitslave|
|SUSE-Gnuplot|
|SUSE-Hack-Open-Font-2.0|
|SUSE-IBPL-1.0|
|SUSE-IDPL-1.0|
|SUSE-IEEE|
|SUSE-Innernet-2.0|
|SUSE-Innernet-2.00|
|SUSE-LDPL-2.0|
|SUSE-LGPL-2.0-with-linking-exception|
|SUSE-LGPL-2.1-with-digia-exception-1.1|
|SUSE-LGPL-2.1-with-nokia-exception-1.1|
|SUSE-Liberation|
|SUSE-MIT-Khronos|
|SUSE-Manpages|
|SUSE-Matplotlib|
|SUSE-MgOpen|
|SUSE-Oasis-Specification-Notice|
|SUSE-OldFSFDocLicense|
|SUSE-OpenPublication-1.0|
|SUSE-PHP-2.02|
|SUSE-Permissive|
|SUSE-Permissive-Modify-By-Patch|
|SUSE-Public-Domain|
|SUSE-Python-1.6|
|SUSE-QWT-1.0|
|SUSE-Redistributable-Content|
|SUSE-Repoze|
|SUSE-SIP|
|SUSE-SLIB|
|SUSE-SNIA-1.0|
|SUSE-SNIA-1.1|
|SUSE-Scrot|
|SUSE-Sun-Laboratories|
|SUSE-TGPPL-1.0|
|SUSE-TeX|
|SUSE-Ubuntu-Font-License-1.0|
|SUSE-XDebug|
|SUSE-XFree86-with-font-exception|
|SUSE-XSL-Lint|
|SUSE-Xano|
|SUSE-Xenonsoft-1.00|
|SUSE-mirror|
|SUSE-wxWidgets-3.1|
