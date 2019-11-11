
# spec-cleaner

[![Build Status](https://travis-ci.org/rpm-software-management/spec-cleaner.svg?branch=master)](https://travis-ci.org/rpm-software-management/spec-cleaner)
[![Coverage Status](https://coveralls.io/repos/github/rpm-software-management/spec-cleaner/badge.svg?branch=master)](https://coveralls.io/github/rpm-software-management/spec-cleaner?branch=master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/rpm-software-management/spec-cleaner.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/rpm-software-management/spec-cleaner/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/rpm-software-management/spec-cleaner.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/rpm-software-management/spec-cleaner/context:python)


spec-cleaner is a tool that cleans the given RPM spec file according to the style guide and returns the result. It's planned to be a replacement for `osc service localrun format_spec_file` and it is intended to provide the same or better features in order to be able to unify all the spec files in [OBS](https://build.opensuse.org/).

# Packages
spec-cleaner is provided as an RPM package for openSUSE Leap ([15.0](https://build.opensuse.org/package/show/openSUSE:Leap:15.0:Update/spec-cleaner) and [15.1](https://build.opensuse.org/package/show/openSUSE:Leap:15.1:Update/spec-cleaner)) and [openSUSE Tumbleweed](https://build.opensuse.org/package/show/openSUSE:Factory/spec-cleaner). When the new spec-cleaner is released then the version updates are done for all maintained openSUSE codestreams. That means that there is always the latest version available as a package in OBS.

The latest version is also available on [PyPI](https://pypi.org/project/spec_cleaner/). You can install it via `pip install spec-cleaner`.


# Tests

## Running the tests
spec-cleaner provides quite an extensive testsuite. You can run these tests locally either directly via `pytest` or in a clean environment via`tox` where besides pytest also flake8 or mypy is called.

### pytest
Just install `python3-pytest`, `python3-pytest-cov` and `python3-pytest-sugar` (for a nice progress bar) and then run all test via:

    pytest

### tox
Install `tox` and run

    tox
for running tests for the test environments stated in `tox.ini` configuration file. Or you can run the tests for a specified environment (e.g. Python 3.7) via calling

	tox -epy37


## Adding new tests
When a new feature is added to spec-cleaner then a test for this piece of code must be added. See

[how to write tests for spec-cleaner](TESTSUITE.md).

## mypy

Recently, optional static type checker support was implemented for the most important parts of the code. It runs automatically (using the recent mypy version) when you run `tox`. If you want to run it on your own, just install `python3-mypy` and run

    mypy spec_cleaner

## Contributing
You are more than welcome to contribute to this project. If your are not sure about your changes, feel free to create an issue where you can discuss it prior to the implementation.

When changing anything in the code, make sure that you don't forget to
  * add proper comments and docstrings
  * run and pass all tests, `flake8` and `mypy` (just run `tox`)
  * add  [tests](TESTSUITE.md) (mainly if you implement a new feature)
  * add `mypy` support for the new code


## Versioning and releasing
For the versions available, see the [tags on this repository](https://github.com/openSUSE/spec-cleaner/releases).

If you have proper permissions you can find handy [how to do a new release](RELEASE.md).


## Authors

* **Tomas Chvatal** [scarabeusiv](https://github.com/scarabeusiv)  - *Initial work*

See also the list of [contributors](AUTHORS) who participated in this project.


# [SPDX Licenses](http://spdx.org/licenses)

License Tag | Description
----------- | -----------
0BSD | BSD Zero Clause License
AAL | Attribution Assurance License
Abstyles | Abstyles License
Adobe-2006 | Adobe Systems Incorporated Source Code License Agreement
Adobe-Glyph | Adobe Glyph List License
ADSL | Amazon Digital Services License
AFL-1.1 | Academic Free License v1.1
AFL-1.2 | Academic Free License v1.2
AFL-2.0 | Academic Free License v2.0
AFL-2.1 | Academic Free License v2.1
AFL-3.0 | Academic Free License v3.0
Afmparse | Afmparse License
AGPL-1.0-only | Affero General Public License v1.0 only
AGPL-1.0-or-later | Affero General Public License v1.0 or later
AGPL-3.0-only | GNU Affero General Public License v3.0 only
AGPL-3.0-or-later | GNU Affero General Public License v3.0 or later
Aladdin | Aladdin Free Public License
AMDPLPA | AMD's plpa_map.c License
AML | Apple MIT License
AMPAS | Academy of Motion Picture Arts and Sciences BSD
ANTLR-PD | ANTLR Software Rights Notice
Apache-1.0 | Apache License 1.0
Apache-1.1 | Apache License 1.1
Apache-2.0 | Apache License 2.0
APAFML | Adobe Postscript AFM License
APL-1.0 | Adaptive Public License 1.0
APSL-1.0 | Apple Public Source License 1.0
APSL-1.1 | Apple Public Source License 1.1
APSL-1.2 | Apple Public Source License 1.2
APSL-2.0 | Apple Public Source License 2.0
Artistic-1.0 | Artistic License 1.0
Artistic-1.0-cl8 | Artistic License 1.0 w/clause 8
Artistic-1.0-Perl | Artistic License 1.0 (Perl)
Artistic-2.0 | Artistic License 2.0
Bahyph | Bahyph License
Barr | Barr License
Beerware | Beerware License
BitTorrent-1.0 | BitTorrent Open Source License v1.0
BitTorrent-1.1 | BitTorrent Open Source License v1.1
blessing | SQLite Blessing
BlueOak-1.0.0 | Blue Oak Model License 1.0.0
Borceux | Borceux license
BSD-1-Clause | BSD 1-Clause License
BSD-2-Clause | BSD 2-Clause "Simplified" License
BSD-2-Clause-FreeBSD | BSD 2-Clause FreeBSD License
BSD-2-Clause-NetBSD | BSD 2-Clause NetBSD License
BSD-2-Clause-Patent | BSD-2-Clause Plus Patent License
BSD-3-Clause | BSD 3-Clause "New" or "Revised" License
BSD-3-Clause-Attribution | BSD with attribution
BSD-3-Clause-Clear | BSD 3-Clause Clear License
BSD-3-Clause-LBNL | Lawrence Berkeley National Labs BSD variant license
BSD-3-Clause-No-Nuclear-License | BSD 3-Clause No Nuclear License
BSD-3-Clause-No-Nuclear-License-2014 | BSD 3-Clause No Nuclear License 2014
BSD-3-Clause-No-Nuclear-Warranty | BSD 3-Clause No Nuclear Warranty
BSD-3-Clause-Open-MPI | BSD 3-Clause Open MPI variant
BSD-4-Clause | BSD 4-Clause "Original" or "Old" License
BSD-4-Clause-UC | BSD-4-Clause (University of California-Specific)
BSD-Protection | BSD Protection License
BSD-Source-Code | BSD Source Code Attribution
BSL-1.0 | Boost Software License 1.0
bzip2-1.0.5 | bzip2 and libbzip2 License v1.0.5
bzip2-1.0.6 | bzip2 and libbzip2 License v1.0.6
Caldera | Caldera License
CATOSL-1.1 | Computer Associates Trusted Open Source License 1.1
CC-BY-1.0 | Creative Commons Attribution 1.0 Generic
CC-BY-2.0 | Creative Commons Attribution 2.0 Generic
CC-BY-2.5 | Creative Commons Attribution 2.5 Generic
CC-BY-3.0 | Creative Commons Attribution 3.0 Unported
CC-BY-4.0 | Creative Commons Attribution 4.0 International
CC-BY-NC-1.0 | Creative Commons Attribution Non Commercial 1.0 Generic
CC-BY-NC-2.0 | Creative Commons Attribution Non Commercial 2.0 Generic
CC-BY-NC-2.5 | Creative Commons Attribution Non Commercial 2.5 Generic
CC-BY-NC-3.0 | Creative Commons Attribution Non Commercial 3.0 Unported
CC-BY-NC-4.0 | Creative Commons Attribution Non Commercial 4.0 International
CC-BY-NC-ND-1.0 | Creative Commons Attribution Non Commercial No Derivatives 1.0 Generic
CC-BY-NC-ND-2.0 | Creative Commons Attribution Non Commercial No Derivatives 2.0 Generic
CC-BY-NC-ND-2.5 | Creative Commons Attribution Non Commercial No Derivatives 2.5 Generic
CC-BY-NC-ND-3.0 | Creative Commons Attribution Non Commercial No Derivatives 3.0 Unported
CC-BY-NC-ND-4.0 | Creative Commons Attribution Non Commercial No Derivatives 4.0 International
CC-BY-NC-SA-1.0 | Creative Commons Attribution Non Commercial Share Alike 1.0 Generic
CC-BY-NC-SA-2.0 | Creative Commons Attribution Non Commercial Share Alike 2.0 Generic
CC-BY-NC-SA-2.5 | Creative Commons Attribution Non Commercial Share Alike 2.5 Generic
CC-BY-NC-SA-3.0 | Creative Commons Attribution Non Commercial Share Alike 3.0 Unported
CC-BY-NC-SA-4.0 | Creative Commons Attribution Non Commercial Share Alike 4.0 International
CC-BY-ND-1.0 | Creative Commons Attribution No Derivatives 1.0 Generic
CC-BY-ND-2.0 | Creative Commons Attribution No Derivatives 2.0 Generic
CC-BY-ND-2.5 | Creative Commons Attribution No Derivatives 2.5 Generic
CC-BY-ND-3.0 | Creative Commons Attribution No Derivatives 3.0 Unported
CC-BY-ND-4.0 | Creative Commons Attribution No Derivatives 4.0 International
CC-BY-SA-1.0 | Creative Commons Attribution Share Alike 1.0 Generic
CC-BY-SA-2.0 | Creative Commons Attribution Share Alike 2.0 Generic
CC-BY-SA-2.5 | Creative Commons Attribution Share Alike 2.5 Generic
CC-BY-SA-3.0 | Creative Commons Attribution Share Alike 3.0 Unported
CC-BY-SA-4.0 | Creative Commons Attribution Share Alike 4.0 International
CC-PDDC | Creative Commons Public Domain Dedication and Certification
CC0-1.0 | Creative Commons Zero v1.0 Universal
CDDL-1.0 | Common Development and Distribution License 1.0
CDDL-1.1 | Common Development and Distribution License 1.1
CDLA-Permissive-1.0 | Community Data License Agreement Permissive 1.0
CDLA-Sharing-1.0 | Community Data License Agreement Sharing 1.0
CECILL-1.0 | CeCILL Free Software License Agreement v1.0
CECILL-1.1 | CeCILL Free Software License Agreement v1.1
CECILL-2.0 | CeCILL Free Software License Agreement v2.0
CECILL-2.1 | CeCILL Free Software License Agreement v2.1
CECILL-B | CeCILL-B Free Software License Agreement
CECILL-C | CeCILL-C Free Software License Agreement
CERN-OHL-1.1 | CERN Open Hardware Licence v1.1
CERN-OHL-1.2 | CERN Open Hardware Licence v1.2
ClArtistic | Clarified Artistic License
CNRI-Jython | CNRI Jython License
CNRI-Python | CNRI Python License
CNRI-Python-GPL-Compatible | CNRI Python Open Source GPL Compatible License Agreement
Condor-1.1 | Condor Public License v1.1
copyleft-next-0.3.0 | copyleft-next 0.3.0
copyleft-next-0.3.1 | copyleft-next 0.3.1
CPAL-1.0 | Common Public Attribution License 1.0
CPL-1.0 | Common Public License 1.0
CPOL-1.02 | Code Project Open License 1.02
Crossword | Crossword License
CrystalStacker | CrystalStacker License
CUA-OPL-1.0 | CUA Office Public License v1.0
Cube | Cube License
curl | curl License
D-FSL-1.0 | Deutsche Freie Software Lizenz
diffmark | diffmark license
DOC | DOC License
Dotseqn | Dotseqn License
DSDP | DSDP License
dvipdfm | dvipdfm License
ECL-1.0 | Educational Community License v1.0
ECL-2.0 | Educational Community License v2.0
EFL-1.0 | Eiffel Forum License v1.0
EFL-2.0 | Eiffel Forum License v2.0
eGenix | eGenix.com Public License 1.1.0
Entessa | Entessa Public License v1.0
EPL-1.0 | Eclipse Public License 1.0
EPL-2.0 | Eclipse Public License 2.0
ErlPL-1.1 | Erlang Public License v1.1
etalab-2.0 | Etalab Open License 2.0
EUDatagrid | EU DataGrid Software License
EUPL-1.0 | European Union Public License 1.0
EUPL-1.1 | European Union Public License 1.1
EUPL-1.2 | European Union Public License 1.2
Eurosym | Eurosym License
Fair | Fair License
Frameworx-1.0 | Frameworx Open License 1.0
FreeImage | FreeImage Public License v1.0
FSFAP | FSF All Permissive License
FSFUL | FSF Unlimited License
FSFULLR | FSF Unlimited License (with License Retention)
FTL | Freetype Project License
GFDL-1.1-only | GNU Free Documentation License v1.1 only
GFDL-1.1-or-later | GNU Free Documentation License v1.1 or later
GFDL-1.2-only | GNU Free Documentation License v1.2 only
GFDL-1.2-or-later | GNU Free Documentation License v1.2 or later
GFDL-1.3-only | GNU Free Documentation License v1.3 only
GFDL-1.3-or-later | GNU Free Documentation License v1.3 or later
Giftware | Giftware License
GL2PS | GL2PS License
Glide | 3dfx Glide License
Glulxe | Glulxe License
gnuplot | gnuplot License
GPL-1.0-only | GNU General Public License v1.0 only
GPL-1.0-or-later | GNU General Public License v1.0 or later
GPL-2.0-only | GNU General Public License v2.0 only
GPL-2.0-or-later | GNU General Public License v2.0 or later
GPL-3.0-only | GNU General Public License v3.0 only
GPL-3.0-or-later | GNU General Public License v3.0 or later
gSOAP-1.3b | gSOAP Public License v1.3b
HaskellReport | Haskell Language Report License
HPND | Historical Permission Notice and Disclaimer
HPND-sell-variant | Historical Permission Notice and Disclaimer - sell variant
IBM-pibs | IBM PowerPC Initialization and Boot Software
ICU | ICU License
IJG | Independent JPEG Group License
ImageMagick | ImageMagick License
iMatix | iMatix Standard Function Library Agreement
Imlib2 | Imlib2 License
Info-ZIP | Info-ZIP License
Intel | Intel Open Source License
Intel-ACPI | Intel ACPI Software License Agreement
Interbase-1.0 | Interbase Public License v1.0
IPA | IPA Font License
IPL-1.0 | IBM Public License v1.0
ISC | ISC License
JasPer-2.0 | JasPer License
JPNIC | Japan Network Information Center License
JSON | JSON License
LAL-1.2 | Licence Art Libre 1.2
LAL-1.3 | Licence Art Libre 1.3
Latex2e | Latex2e License
Leptonica | Leptonica License
LGPL-2.0-only | GNU Library General Public License v2 only
LGPL-2.0-or-later | GNU Library General Public License v2 or later
LGPL-2.1-only | GNU Lesser General Public License v2.1 only
LGPL-2.1-or-later | GNU Lesser General Public License v2.1 or later
LGPL-3.0-only | GNU Lesser General Public License v3.0 only
LGPL-3.0-or-later | GNU Lesser General Public License v3.0 or later
LGPLLR | Lesser General Public License For Linguistic Resources
Libpng | libpng License
libpng-2.0 | PNG Reference Library version 2
libtiff | libtiff License
LiLiQ-P-1.1 | Licence Libre du Qu?bec ? Permissive version 1.1
LiLiQ-R-1.1 | Licence Libre du Qu?bec ? R?ciprocit? version 1.1
LiLiQ-Rplus-1.1 | Licence Libre du Qu?bec ? R?ciprocit? forte version 1.1
Linux-OpenIB | Linux Kernel Variant of OpenIB.org license
LPL-1.0 | Lucent Public License Version 1.0
LPL-1.02 | Lucent Public License v1.02
LPPL-1.0 | LaTeX Project Public License v1.0
LPPL-1.1 | LaTeX Project Public License v1.1
LPPL-1.2 | LaTeX Project Public License v1.2
LPPL-1.3a | LaTeX Project Public License v1.3a
LPPL-1.3c | LaTeX Project Public License v1.3c
MakeIndex | MakeIndex License
MirOS | The MirOS Licence
MIT | MIT License
MIT-0 | MIT No Attribution
MIT-advertising | Enlightenment License (e16)
MIT-CMU | CMU License
MIT-enna | enna License
MIT-feh | feh License
MITNFA | MIT +no-false-attribs license
Motosoto | Motosoto License
mpich2 | mpich2 License
MPL-1.0 | Mozilla Public License 1.0
MPL-1.1 | Mozilla Public License 1.1
MPL-2.0 | Mozilla Public License 2.0
MPL-2.0-no-copyleft-exception | Mozilla Public License 2.0 (no copyleft exception)
MS-PL | Microsoft Public License
MS-RL | Microsoft Reciprocal License
MTLL | Matrix Template Library License
MulanPSL-1.0 | Mulan Permissive Software License, Version 1
Multics | Multics License
Mup | Mup License
NASA-1.3 | NASA Open Source Agreement 1.3
Naumen | Naumen Public License
NBPL-1.0 | Net Boolean Public License v1
NCSA | University of Illinois/NCSA Open Source License
Net-SNMP | Net-SNMP License
NetCDF | NetCDF license
Newsletr | Newsletr License
NGPL | Nethack General Public License
NLOD-1.0 | Norwegian Licence for Open Government Data
NLPL | No Limit Public License
Nokia | Nokia Open Source License
NOSL | Netizen Open Source License
Noweb | Noweb License
NPL-1.0 | Netscape Public License v1.0
NPL-1.1 | Netscape Public License v1.1
NPOSL-3.0 | Non-Profit Open Software License 3.0
NRL | NRL License
NTP | NTP License
OCCT-PL | Open CASCADE Technology Public License
OCLC-2.0 | OCLC Research Public License 2.0
ODbL-1.0 | ODC Open Database License v1.0
ODC-By-1.0 | Open Data Commons Attribution License v1.0
OFL-1.0 | SIL Open Font License 1.0
OFL-1.1 | SIL Open Font License 1.1
OGL-Canada-2.0 | Open Government Licence - Canada
OGL-UK-1.0 | Open Government Licence v1.0
OGL-UK-2.0 | Open Government Licence v2.0
OGL-UK-3.0 | Open Government Licence v3.0
OGTSL | Open Group Test Suite License
OLDAP-1.1 | Open LDAP Public License v1.1
OLDAP-1.2 | Open LDAP Public License v1.2
OLDAP-1.3 | Open LDAP Public License v1.3
OLDAP-1.4 | Open LDAP Public License v1.4
OLDAP-2.0 | Open LDAP Public License v2.0 (or possibly 2.0A and 2.0B)
OLDAP-2.0.1 | Open LDAP Public License v2.0.1
OLDAP-2.1 | Open LDAP Public License v2.1
OLDAP-2.2 | Open LDAP Public License v2.2
OLDAP-2.2.1 | Open LDAP Public License v2.2.1
OLDAP-2.2.2 | Open LDAP Public License 2.2.2
OLDAP-2.3 | Open LDAP Public License v2.3
OLDAP-2.4 | Open LDAP Public License v2.4
OLDAP-2.5 | Open LDAP Public License v2.5
OLDAP-2.6 | Open LDAP Public License v2.6
OLDAP-2.7 | Open LDAP Public License v2.7
OLDAP-2.8 | Open LDAP Public License v2.8
OML | Open Market License
OpenSSL | OpenSSL License
OPL-1.0 | Open Public License v1.0
OSET-PL-2.1 | OSET Public License version 2.1
OSL-1.0 | Open Software License 1.0
OSL-1.1 | Open Software License 1.1
OSL-2.0 | Open Software License 2.0
OSL-2.1 | Open Software License 2.1
OSL-3.0 | Open Software License 3.0
Parity-6.0.0 | The Parity Public License 6.0.0
PDDL-1.0 | ODC Public Domain Dedication & License 1.0
PHP-3.0 | PHP License v3.0
PHP-3.01 | PHP License v3.01
Plexus | Plexus Classworlds License
PostgreSQL | PostgreSQL License
psfrag | psfrag License
psutils | psutils License
Python-2.0 | Python License 2.0
Qhull | Qhull License
QPL-1.0 | Q Public License 1.0
Rdisc | Rdisc License
RHeCos-1.1 | Red Hat eCos Public License v1.1
RPL-1.1 | Reciprocal Public License 1.1
RPL-1.5 | Reciprocal Public License 1.5
RPSL-1.0 | RealNetworks Public Source License v1.0
RSA-MD | RSA Message-Digest License
RSCPL | Ricoh Source Code Public License
Ruby | Ruby License
SAX-PD | Sax Public Domain Notice
Saxpath | Saxpath License
SCEA | SCEA Shared Source License
Sendmail | Sendmail License
Sendmail-8.23 | Sendmail License 8.23
SGI-B-1.0 | SGI Free Software License B v1.0
SGI-B-1.1 | SGI Free Software License B v1.1
SGI-B-2.0 | SGI Free Software License B v2.0
SHL-0.5 | Solderpad Hardware License v0.5
SHL-0.51 | Solderpad Hardware License, Version 0.51
SimPL-2.0 | Simple Public License 2.0
SISSL | Sun Industry Standards Source License v1.1
SISSL-1.2 | Sun Industry Standards Source License v1.2
Sleepycat | Sleepycat License
SMLNJ | Standard ML of New Jersey License
SMPPL | Secure Messaging Protocol Public License
SNIA | SNIA Public License 1.1
Spencer-86 | Spencer License 86
Spencer-94 | Spencer License 94
Spencer-99 | Spencer License 99
SPL-1.0 | Sun Public License v1.0
SSH-OpenSSH | SSH OpenSSH license
SSH-short | SSH short notice
SSPL-1.0 | Server Side Public License, v 1
SugarCRM-1.1.3 | SugarCRM Public License v1.1.3
SWL | Scheme Widget Library (SWL) Software License Agreement
TAPR-OHL-1.0 | TAPR Open Hardware License v1.0
TCL | TCL/TK License
TCP-wrappers | TCP Wrappers License
TMate | TMate Open Source License
TORQUE-1.1 | TORQUE v2.5+ Software License v1.1
TOSL | Trusster Open Source License
TU-Berlin-1.0 | Technische Universitaet Berlin License 1.0
TU-Berlin-2.0 | Technische Universitaet Berlin License 2.0
UCL-1.0 | Upstream Compatibility License v1.0
Unicode-DFS-2015 | Unicode License Agreement - Data Files and Software (2015)
Unicode-DFS-2016 | Unicode License Agreement - Data Files and Software (2016)
Unicode-TOU | Unicode Terms of Use
Unlicense | The Unlicense
UPL-1.0 | Universal Permissive License v1.0
Vim | Vim License
VOSTROM | VOSTROM Public License for Open Source
VSL-1.0 | Vovida Software License v1.0
W3C | W3C Software Notice and License (2002-12-31)
W3C-19980720 | W3C Software Notice and License (1998-07-20)
W3C-20150513 | W3C Software Notice and Document License (2015-05-13)
Watcom-1.0 | Sybase Open Watcom Public License 1.0
Wsuipa | Wsuipa License
WTFPL | Do What The F*ck You Want To Public License
X11 | X11 License
Xerox | Xerox License
XFree86-1.1 | XFree86 License 1.1
xinetd | xinetd License
Xnet | X.Net License
xpp | XPP License
XSkat | XSkat License
YPL-1.0 | Yahoo! Public License v1.0
YPL-1.1 | Yahoo! Public License v1.1
Zed | Zed License
Zend-2.0 | Zend License v2.0
Zimbra-1.3 | Zimbra Public License v1.3
Zimbra-1.4 | Zimbra Public License v1.4
Zlib | zlib License
zlib-acknowledgement | zlib/libpng License with Acknowledgement
ZPL-1.1 | Zope Public License 1.1
ZPL-2.0 | Zope Public License 2.0
ZPL-2.1 | Zope Public License 2.1

# SPDX Exceptions

|Exception name|
|--------------|
389-exception
Autoconf-exception-2.0
Autoconf-exception-3.0
Bison-exception-2.2
Bootloader-exception
CLISP-exception-2.0
Classpath-exception-2.0
DigiRule-FOSS-exception
FLTK-exception
Fawkes-Runtime-exception
Font-exception-2.0
GCC-exception-2.0
GCC-exception-3.1
GPL-CC-1.0
LLVM-exception
LZMA-exception
Libtool-exception
Linux-syscall-note
OCCT-exception-1.0
OCaml-LGPL-linking-exception
OpenJDK-assembly-exception-1.0
PS-or-PDF-font-exception-20170817
Qt-GPL-exception-1.0
Qt-LGPL-exception-1.1
Qwt-exception-1.0
Swift-exception
Universal-FOSS-exception-1.0
WxWindows-exception-3.1
eCos-exception-2.0
freertos-exception-2.0
gnu-javamail-exception
i2p-gpl-java-exception
mif-exception
openvpn-openssl-exception
u-boot-exception-2.0

# SUSE Additions

|License Tag|
|-----------|
|SUSE-Arphic|
|SUSE-BSD-3-Clause-with-non-nuclear-addition|
|SUSE-BSD-Mark-Modifications|
|SUSE-Bitstream-Vera|
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
|SUSE-SGI-FreeB-2.0|
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
|SUSE-mplus|
|SUSE-wxWidgets-3.1|
