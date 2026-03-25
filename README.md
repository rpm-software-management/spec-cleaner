
# spec-cleaner

![Build Status](https://github.com/rpm-software-management/spec-cleaner/workflows/Python%20package/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/rpm-software-management/spec-cleaner/badge.svg?branch=master)](https://coveralls.io/github/rpm-software-management/spec-cleaner?branch=master)
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
0BSD | BSD Zero Clause License
3D-Slicer-1.0 | 3D Slicer License v1.0
AAL | Attribution Assurance License
ADSL | Amazon Digital Services License
AFL-1.1 | Academic Free License v1.1
AFL-1.2 | Academic Free License v1.2
AFL-2.0 | Academic Free License v2.0
AFL-2.1 | Academic Free License v2.1
AFL-3.0 | Academic Free License v3.0
AGPL-1.0-only | Affero General Public License v1.0 only
AGPL-1.0-or-later | Affero General Public License v1.0 or later
AGPL-3.0-only | GNU Affero General Public License v3.0 only
AGPL-3.0-or-later | GNU Affero General Public License v3.0 or later
ALGLIB-Documentation | ALGLIB Documentation License
AMD-newlib | AMD newlib License
AMDPLPA | AMD's plpa_map.c License
AML-glslang | AML glslang variant License
AML | Apple MIT License
AMPAS | Academy of Motion Picture Arts and Sciences BSD
ANTLR-PD-fallback | ANTLR Software Rights Notice with license fallback
ANTLR-PD | ANTLR Software Rights Notice
APAFML | Adobe Postscript AFM License
APL-1.0 | Adaptive Public License 1.0
APSL-1.0 | Apple Public Source License 1.0
APSL-1.1 | Apple Public Source License 1.1
APSL-1.2 | Apple Public Source License 1.2
APSL-2.0 | Apple Public Source License 2.0
ASWF-Digital-Assets-1.0 | ASWF Digital Assets License version 1.0
ASWF-Digital-Assets-1.1 | ASWF Digital Assets License 1.1
Abstyles | Abstyles License
AdaCore-doc | AdaCore Doc License
Adobe-2006 | Adobe Systems Incorporated Source Code License Agreement
Adobe-Display-PostScript | Adobe Display PostScript License
Adobe-Glyph | Adobe Glyph List License
Adobe-Utopia | Adobe Utopia Font License
Advanced-Cryptics-Dictionary | Advanced Cryptics Dictionary License
Afmparse | Afmparse License
Aladdin | Aladdin Free Public License
Apache-1.0 | Apache License 1.0
Apache-1.1 | Apache License 1.1
Apache-2.0 | Apache License 2.0
App-s2p | App::s2p License
Arphic-1999 | Arphic Public License
Artistic-1.0-Perl | Artistic License 1.0 (Perl)
Artistic-1.0-cl8 | Artistic License 1.0 w/clause 8
Artistic-1.0 | Artistic License 1.0
Artistic-2.0 | Artistic License 2.0
Artistic-dist | Artistic License 1.0 (dist)
Aspell-RU | Aspell Russian License
BOLA-1.1 | Buena Onda License Agreement v1.1
BSD-1-Clause | BSD 1-Clause License
BSD-2-Clause-Darwin | BSD 2-Clause - Ian Darwin variant
BSD-2-Clause-Patent | BSD-2-Clause Plus Patent License
BSD-2-Clause-Views | BSD 2-Clause with views sentence
BSD-2-Clause-first-lines | BSD 2-Clause - first lines requirement
BSD-2-Clause-pkgconf-disclaimer | BSD 2-Clause pkgconf disclaimer variant
BSD-2-Clause | BSD 2-Clause "Simplified" License
BSD-3-Clause-Attribution | BSD with attribution
BSD-3-Clause-Clear | BSD 3-Clause Clear License
BSD-3-Clause-HP | Hewlett-Packard BSD variant license
BSD-3-Clause-LBNL | Lawrence Berkeley National Labs BSD variant license
BSD-3-Clause-Modification | BSD 3-Clause Modification
BSD-3-Clause-No-Military-License | BSD 3-Clause No Military License
BSD-3-Clause-No-Nuclear-License-2014 | BSD 3-Clause No Nuclear License 2014
BSD-3-Clause-No-Nuclear-License | BSD 3-Clause No Nuclear License
BSD-3-Clause-No-Nuclear-Warranty | BSD 3-Clause No Nuclear Warranty
BSD-3-Clause-Open-MPI | BSD 3-Clause Open MPI variant
BSD-3-Clause-Sun | BSD 3-Clause Sun Microsystems
BSD-3-Clause-Tso | BSD 3-Clause Tso variant
BSD-3-Clause-acpica | BSD 3-Clause acpica variant
BSD-3-Clause-flex | BSD 3-Clause Flex variant
BSD-3-Clause | BSD 3-Clause "New" or "Revised" License
BSD-4-Clause-Shortened | BSD 4 Clause Shortened
BSD-4-Clause-UC | BSD-4-Clause (University of California-Specific)
BSD-4-Clause | BSD 4-Clause "Original" or "Old" License
BSD-4.3RENO | BSD 4.3 RENO License
BSD-4.3TAHOE | BSD 4.3 TAHOE License
BSD-Advertising-Acknowledgement | BSD Advertising Acknowledgement License
BSD-Attribution-HPND-disclaimer | BSD with Attribution and HPND disclaimer
BSD-Inferno-Nettverk | BSD-Inferno-Nettverk
BSD-Mark-Modifications | BSD Mark Modifications License
BSD-Protection | BSD Protection License
BSD-Source-Code | BSD Source Code Attribution
BSD-Source-beginning-file | BSD Source Code Attribution - beginning of file variant
BSD-Systemics-W3Works | Systemics W3Works BSD variant license
BSD-Systemics | Systemics BSD variant license
BSL-1.0 | Boost Software License 1.0
BUSL-1.1 | Business Source License 1.1
Baekmuk | Baekmuk License
Bahyph | Bahyph License
Barr | Barr License
Beerware | Beerware License
BitTorrent-1.0 | BitTorrent Open Source License v1.0
BitTorrent-1.1 | BitTorrent Open Source License v1.1
Bitstream-Charter | Bitstream Charter Font License
Bitstream-Vera | Bitstream Vera Font License
BlueOak-1.0.0 | Blue Oak Model License 1.0.0
Boehm-GC-without-fee | Boehm-Demers-Weiser GC License (without fee)
Boehm-GC | Boehm-Demers-Weiser GC License
Borceux | Borceux license
Brian-Gladman-2-Clause | Brian Gladman 2-Clause License
Brian-Gladman-3-Clause | Brian Gladman 3-Clause License
Buddy | Buddy License
C-UDA-1.0 | Computational Use of Data Agreement v1.0
CAL-1.0-Combined-Work-Exception | Cryptographic Autonomy License 1.0 (Combined Work Exception)
CAL-1.0 | Cryptographic Autonomy License 1.0
CAPEC-tou | Common Attack    Pattern Enumeration and Classification License
CATOSL-1.1 | Computer Associates Trusted Open Source License 1.1
CC-BY-1.0 | Creative Commons Attribution 1.0 Generic
CC-BY-2.0 | Creative Commons Attribution 2.0 Generic
CC-BY-2.5-AU | Creative Commons Attribution 2.5 Australia
CC-BY-2.5 | Creative Commons Attribution 2.5 Generic
CC-BY-3.0-AT | Creative Commons Attribution 3.0 Austria
CC-BY-3.0-AU | Creative Commons Attribution 3.0 Australia
CC-BY-3.0-DE | Creative Commons Attribution 3.0 Germany
CC-BY-3.0-IGO | Creative Commons Attribution 3.0 IGO
CC-BY-3.0-NL | Creative Commons Attribution 3.0 Netherlands
CC-BY-3.0-US | Creative Commons Attribution 3.0 United States
CC-BY-3.0 | Creative Commons Attribution 3.0 Unported
CC-BY-4.0 | Creative Commons Attribution 4.0 International
CC-BY-NC-1.0 | Creative Commons Attribution Non Commercial 1.0 Generic
CC-BY-NC-2.0 | Creative Commons Attribution Non Commercial 2.0 Generic
CC-BY-NC-2.5 | Creative Commons Attribution Non Commercial 2.5 Generic
CC-BY-NC-3.0-DE | Creative Commons Attribution Non Commercial 3.0 Germany
CC-BY-NC-3.0 | Creative Commons Attribution Non Commercial 3.0 Unported
CC-BY-NC-4.0 | Creative Commons Attribution Non Commercial 4.0 International
CC-BY-NC-ND-1.0 | Creative Commons Attribution Non Commercial No Derivatives 1.0 Generic
CC-BY-NC-ND-2.0 | Creative Commons Attribution Non Commercial No Derivatives 2.0 Generic
CC-BY-NC-ND-2.5 | Creative Commons Attribution Non Commercial No Derivatives 2.5 Generic
CC-BY-NC-ND-3.0-DE | Creative Commons Attribution Non Commercial No Derivatives 3.0 Germany
CC-BY-NC-ND-3.0-IGO | Creative Commons Attribution Non Commercial No Derivatives 3.0 IGO
CC-BY-NC-ND-3.0 | Creative Commons Attribution Non Commercial No Derivatives 3.0 Unported
CC-BY-NC-ND-4.0 | Creative Commons Attribution Non Commercial No Derivatives 4.0 International
CC-BY-NC-SA-1.0 | Creative Commons Attribution Non Commercial Share Alike 1.0 Generic
CC-BY-NC-SA-2.0-DE | Creative Commons Attribution Non Commercial Share Alike 2.0 Germany
CC-BY-NC-SA-2.0-FR | Creative Commons Attribution-NonCommercial-ShareAlike 2.0 France
CC-BY-NC-SA-2.0-UK | Creative Commons Attribution Non Commercial Share Alike 2.0 England and Wales
CC-BY-NC-SA-2.0 | Creative Commons Attribution Non Commercial Share Alike 2.0 Generic
CC-BY-NC-SA-2.5 | Creative Commons Attribution Non Commercial Share Alike 2.5 Generic
CC-BY-NC-SA-3.0-DE | Creative Commons Attribution Non Commercial Share Alike 3.0 Germany
CC-BY-NC-SA-3.0-IGO | Creative Commons Attribution Non Commercial Share Alike 3.0 IGO
CC-BY-NC-SA-3.0 | Creative Commons Attribution Non Commercial Share Alike 3.0 Unported
CC-BY-NC-SA-4.0 | Creative Commons Attribution Non Commercial Share Alike 4.0 International
CC-BY-ND-1.0 | Creative Commons Attribution No Derivatives 1.0 Generic
CC-BY-ND-2.0 | Creative Commons Attribution No Derivatives 2.0 Generic
CC-BY-ND-2.5 | Creative Commons Attribution No Derivatives 2.5 Generic
CC-BY-ND-3.0-DE | Creative Commons Attribution No Derivatives 3.0 Germany
CC-BY-ND-3.0 | Creative Commons Attribution No Derivatives 3.0 Unported
CC-BY-ND-4.0 | Creative Commons Attribution No Derivatives 4.0 International
CC-BY-SA-1.0 | Creative Commons Attribution Share Alike 1.0 Generic
CC-BY-SA-2.0-UK | Creative Commons Attribution Share Alike 2.0 England and Wales
CC-BY-SA-2.0 | Creative Commons Attribution Share Alike 2.0 Generic
CC-BY-SA-2.1-JP | Creative Commons Attribution Share Alike 2.1 Japan
CC-BY-SA-2.5 | Creative Commons Attribution Share Alike 2.5 Generic
CC-BY-SA-3.0-AT | Creative Commons Attribution Share Alike 3.0 Austria
CC-BY-SA-3.0-DE | Creative Commons Attribution Share Alike 3.0 Germany
CC-BY-SA-3.0-IGO | Creative Commons Attribution-ShareAlike 3.0 IGO
CC-BY-SA-3.0 | Creative Commons Attribution Share Alike 3.0 Unported
CC-BY-SA-4.0 | Creative Commons Attribution Share Alike 4.0 International
CC-PDDC | Creative Commons Public Domain Dedication and Certification
CC-PDM-1.0 | Creative    Commons Public Domain Mark 1.0 Universal
CC-SA-1.0 | Creative Commons Share Alike 1.0 Generic
CC0-1.0 | Creative Commons Zero v1.0 Universal
CDDL-1.0 | Common Development and Distribution License 1.0
CDDL-1.1 | Common Development and Distribution License 1.1
CDL-1.0 | Common Documentation License 1.0
CDLA-Permissive-1.0 | Community Data License Agreement Permissive 1.0
CDLA-Permissive-2.0 | Community Data License Agreement Permissive 2.0
CDLA-Sharing-1.0 | Community Data License Agreement Sharing 1.0
CECILL-1.0 | CeCILL Free Software License Agreement v1.0
CECILL-1.1 | CeCILL Free Software License Agreement v1.1
CECILL-2.0 | CeCILL Free Software License Agreement v2.0
CECILL-2.1 | CeCILL Free Software License Agreement v2.1
CECILL-B | CeCILL-B Free Software License Agreement
CECILL-C | CeCILL-C Free Software License Agreement
CERN-OHL-1.1 | CERN Open Hardware Licence v1.1
CERN-OHL-1.2 | CERN Open Hardware Licence v1.2
CERN-OHL-P-2.0 | CERN Open Hardware Licence Version 2 - Permissive
CERN-OHL-S-2.0 | CERN Open Hardware Licence Version 2 - Strongly Reciprocal
CERN-OHL-W-2.0 | CERN Open Hardware Licence Version 2 - Weakly Reciprocal
CFITSIO | CFITSIO License
CMU-Mach-nodoc | CMU    Mach - no notices-in-documentation variant
CMU-Mach | CMU Mach License
CNRI-Jython | CNRI Jython License
CNRI-Python-GPL-Compatible | CNRI Python Open Source GPL Compatible License Agreement
CNRI-Python | CNRI Python License
COIL-1.0 | Copyfree Open Innovation License
CPAL-1.0 | Common Public Attribution License 1.0
CPL-1.0 | Common Public License 1.0
CPOL-1.02 | Code Project Open License 1.02
CUA-OPL-1.0 | CUA Office Public License v1.0
Caldera-no-preamble | Caldera License (without preamble)
Caldera | Caldera License
Catharon | Catharon License
ClArtistic | Clarified Artistic License
Clips | Clips License
Community-Spec-1.0 | Community Specification License 1.0
Condor-1.1 | Condor Public License v1.1
Cornell-Lossless-JPEG | Cornell Lossless JPEG License
Cronyx | Cronyx License
Crossword | Crossword License
CryptoSwift | CryptoSwift License
CrystalStacker | CrystalStacker License
Cube | Cube License
D-FSL-1.0 | Deutsche Freie Software Lizenz
DEC-3-Clause | DEC 3-Clause License
DL-DE-BY-2.0 | Data licence Germany – attribution – version 2.0
DL-DE-ZERO-2.0 | Data licence Germany – zero – version 2.0
DOC | DOC License
DRL-1.0 | Detection Rule License 1.0
DRL-1.1 | Detection Rule License 1.1
DSDP | DSDP License
DocBook-DTD | DocBook DTD License
DocBook-Schema | DocBook Schema License
DocBook-Stylesheet | DocBook Stylesheet License
DocBook-XML | DocBook XML License
Dotseqn | Dotseqn License
ECL-1.0 | Educational Community License v1.0
ECL-2.0 | Educational Community License v2.0
EFL-1.0 | Eiffel Forum License v1.0
EFL-2.0 | Eiffel Forum License v2.0
EPICS | EPICS Open License
EPL-1.0 | Eclipse Public License 1.0
EPL-2.0 | Eclipse Public License 2.0
ESA-PL-permissive-2.4 | European Space Agency Public License – v2.4 – Permissive (Type 3)
ESA-PL-strong-copyleft-2.4 | European Space Agency Public License (ESA-PL) - V2.4 - Strong Copyleft (Type 1)
ESA-PL-weak-copyleft-2.4 | European Space Agency Public License – v2.4 – Weak Copyleft (Type 2)
EUDatagrid | EU DataGrid Software License
EUPL-1.0 | European Union Public License 1.0
EUPL-1.1 | European Union Public License 1.1
EUPL-1.2 | European Union Public License 1.2
Elastic-2.0 | Elastic License 2.0
Entessa | Entessa Public License v1.0
ErlPL-1.1 | Erlang Public License v1.1
Eurosym | Eurosym License
FBM | Fuzzy Bitmap License
FDK-AAC | Fraunhofer FDK AAC Codec Library
FSFAP-no-warranty-disclaimer | FSF All Permissive License (without Warranty)
FSFAP | FSF All Permissive License
FSFUL | FSF Unlimited License
FSFULLR | FSF Unlimited License (with License Retention)
FSFULLRSD | FSF Unlimited License (with License Retention and Short Disclaimer)
FSFULLRWD | FSF Unlimited License (With License Retention and Warranty Disclaimer)
FSL-1.1-ALv2 | Functional Source License, Version 1.1, ALv2 Future License
FSL-1.1-MIT | Functional Source License, Version 1.1, MIT Future License
FTL | Freetype Project License
Fair | Fair License
Ferguson-Twofish | Ferguson Twofish License
Frameworx-1.0 | Frameworx Open License 1.0
FreeBSD-DOC | FreeBSD Documentation License
FreeImage | FreeImage Public License v1.0
Furuseth | Furuseth License
GCR-docs | Gnome GCR Documentation License
GD | GD License
GFDL-1.1-invariants-only | GNU Free Documentation License v1.1 only - invariants
GFDL-1.1-invariants-or-later | GNU Free Documentation License v1.1 or later - invariants
GFDL-1.1-no-invariants-only | GNU Free Documentation License v1.1 only - no invariants
GFDL-1.1-no-invariants-or-later | GNU Free Documentation License v1.1 or later - no invariants
GFDL-1.1-only | GNU Free Documentation License v1.1 only
GFDL-1.1-or-later | GNU Free Documentation License v1.1 or later
GFDL-1.2-invariants-only | GNU Free Documentation License v1.2 only - invariants
GFDL-1.2-invariants-or-later | GNU Free Documentation License v1.2 or later - invariants
GFDL-1.2-no-invariants-only | GNU Free Documentation License v1.2 only - no invariants
GFDL-1.2-no-invariants-or-later | GNU Free Documentation License v1.2 or later - no invariants
GFDL-1.2-only | GNU Free Documentation License v1.2 only
GFDL-1.2-or-later | GNU Free Documentation License v1.2 or later
GFDL-1.3-invariants-only | GNU Free Documentation License v1.3 only - invariants
GFDL-1.3-invariants-or-later | GNU Free Documentation License v1.3 or later - invariants
GFDL-1.3-no-invariants-only | GNU Free Documentation License v1.3 only - no invariants
GFDL-1.3-no-invariants-or-later | GNU Free Documentation License v1.3 or later - no invariants
GFDL-1.3-only | GNU Free Documentation License v1.3 only
GFDL-1.3-or-later | GNU Free Documentation License v1.3 or later
GL2PS | GL2PS License
GLWTPL | Good Luck With That Public License
GPL-1.0-only | GNU General Public License v1.0 only
GPL-1.0-or-later | GNU General Public License v1.0 or later
GPL-2.0-only | GNU General Public License v2.0 only
GPL-2.0-or-later | GNU General Public License v2.0 or later
GPL-3.0-only | GNU General Public License v3.0 only
GPL-3.0-or-later | GNU General Public License v3.0 or later
Game-Programming-Gems | Game Programming Gems License
Giftware | Giftware License
Glide | 3dfx Glide License
Glulxe | Glulxe License
Graphics-Gems | Graphics Gems License
Gutmann | Gutmann License
HDF5 | HDF5 License
HIDAPI | HIDAPI License
HP-1986 | Hewlett-Packard 1986 License
HP-1989 | Hewlett-Packard 1989 License
HPND-DEC | Historical Permission Notice and Disclaimer - DEC variant
HPND-Fenneberg-Livingston | Historical Permission Notice and Disclaimer - Fenneberg-Livingston variant
HPND-INRIA-IMAG | Historical Permission Notice and Disclaimer    - INRIA-IMAG variant
HPND-Intel | Historical Permission Notice and Disclaimer - Intel variant
HPND-Kevlin-Henney | Historical Permission Notice and Disclaimer - Kevlin Henney variant
HPND-MIT-disclaimer | Historical Permission Notice and Disclaimer with MIT disclaimer
HPND-Markus-Kuhn | Historical Permission Notice and Disclaimer - Markus Kuhn variant
HPND-Netrek | Historical Permission Notice and Disclaimer - Netrek variant
HPND-Pbmplus | Historical Permission Notice and Disclaimer - Pbmplus variant
HPND-SMC | Historical Permission Notice and Disclaimer - SMC variant
HPND-UC-export-US | Historical Permission Notice and Disclaimer - University of California, US export warning
HPND-UC | Historical Permission Notice and Disclaimer - University of California variant
HPND-doc-sell | Historical Permission Notice and Disclaimer - documentation sell variant
HPND-doc | Historical Permission Notice and Disclaimer - documentation variant
HPND-export-US-acknowledgement | HPND with US Government export control warning and acknowledgment
HPND-export-US-modify | HPND with US Government export control warning and modification rqmt
HPND-export-US | HPND with US Government export control warning
HPND-export2-US | HPND with US Government export control and 2 disclaimers
HPND-merchantability-variant | Historical Permission Notice and Disclaimer - merchantability variant
HPND-sell-MIT-disclaimer-xserver | Historical Permission Notice and Disclaimer - sell xserver variant with MIT disclaimer
HPND-sell-regexpr | Historical Permission Notice and Disclaimer - sell regexpr variant
HPND-sell-variant-MIT-disclaimer-rev | HPND sell variant with MIT disclaimer - reverse
HPND-sell-variant-MIT-disclaimer | HPND sell variant with MIT disclaimer
HPND-sell-variant-critical-systems | HPND - sell variant with safety critical systems clause
HPND-sell-variant | Historical Permission Notice and Disclaimer - sell variant
HPND | Historical Permission Notice and Disclaimer
HTMLTIDY | HTML Tidy License
HaskellReport | Haskell Language Report License
Hippocratic-2.1 | Hippocratic License 2.1
IBM-pibs | IBM PowerPC Initialization and Boot Software
ICU | ICU License
IEC-Code-Components-EULA | IEC    Code Components End-user licence agreement
IJG-short | Independent JPEG Group License - short
IJG | Independent JPEG Group License
IPA | IPA Font License
IPL-1.0 | IBM Public License v1.0
ISC-Veillard | ISC Veillard variant
ISC | ISC License
ISO-permission | ISO permission notice
ImageMagick | ImageMagick License
Imlib2 | Imlib2 License
Info-ZIP | Info-ZIP License
Inner-Net-2.0 | Inner Net License v2.0
InnoSetup | Inno Setup License
Intel-ACPI | Intel ACPI Software License Agreement
Intel | Intel Open Source License
Interbase-1.0 | Interbase Public License v1.0
JPL-image | JPL Image Use Policy
JPNIC | Japan Network Information Center License
JSON | JSON License
Jam | Jam License
JasPer-2.0 | JasPer License
Kastrup | Kastrup License
Kazlib | Kazlib License
Knuth-CTAN | Knuth CTAN License
LAL-1.2 | Licence Art Libre 1.2
LAL-1.3 | Licence Art Libre 1.3
LGPL-2.0-only | GNU Library General Public License v2 only
LGPL-2.0-or-later | GNU Library General Public License v2 or later
LGPL-2.1-only | GNU Lesser General Public License v2.1 only
LGPL-2.1-or-later | GNU Lesser General Public License v2.1 or later
LGPL-3.0-only | GNU Lesser General Public License v3.0 only
LGPL-3.0-or-later | GNU Lesser General Public License v3.0 or later
LGPLLR | Lesser General Public License For Linguistic Resources
LOOP | Common Lisp LOOP License
LPD-document | LPD Documentation License
LPL-1.02 | Lucent Public License v1.02
LPL-1.0 | Lucent Public License Version 1.0
LPPL-1.0 | LaTeX Project Public License v1.0
LPPL-1.1 | LaTeX Project Public License v1.1
LPPL-1.2 | LaTeX Project Public License v1.2
LPPL-1.3a | LaTeX Project Public License v1.3a
LPPL-1.3c | LaTeX Project Public License v1.3c
LZMA-SDK-9.11-to-9.20 | LZMA SDK License (versions 9.11 to 9.20)
LZMA-SDK-9.22 | LZMA SDK License (versions 9.22 and beyond)
Latex2e-translated-notice | Latex2e with translated notice permission
Latex2e | Latex2e License
Leptonica | Leptonica License
LiLiQ-P-1.1 | Licence Libre du Québec – Permissive version 1.1
LiLiQ-R-1.1 | Licence Libre du Québec – Réciprocité version 1.1
LiLiQ-Rplus-1.1 | Licence Libre du Québec – Réciprocité forte version 1.1
Libpng | libpng License
Linux-OpenIB | Linux Kernel Variant of OpenIB.org license
Linux-man-pages-1-para | Linux man-pages - 1 paragraph
Linux-man-pages-copyleft-2-para | Linux man-pages Copyleft - 2 paragraphs
Linux-man-pages-copyleft-var | Linux man-pages Copyleft Variant
Linux-man-pages-copyleft | Linux man-pages Copyleft
Lucida-Bitmap-Fonts | Lucida Bitmap Fonts License
MIPS | MIPS License
MIT-0 | MIT No Attribution
MIT-CMU | CMU License
MIT-Click | MIT Click License
MIT-Festival | MIT Festival Variant
MIT-Khronos-old | MIT Khronos - old variant
MIT-Modern-Variant | MIT License Modern Variant
MIT-STK | MIT-STK License
MIT-Wu | MIT Tom Wu Variant
MIT-advertising | Enlightenment License (e16)
MIT-enna | enna License
MIT-feh | feh License
MIT-open-group | MIT Open Group variant
MIT-testregex | MIT testregex Variant
MIT | MIT License
MITNFA | MIT +no-false-attribs license
MMIXware | MMIXware License
MMPL-1.0.1 | Minecraft Mod Public License v1.0.1
MPEG-SSG | MPEG Software Simulation
MPL-1.0 | Mozilla Public License 1.0
MPL-1.1 | Mozilla Public License 1.1
MPL-2.0-no-copyleft-exception | Mozilla Public License 2.0 (no copyleft exception)
MPL-2.0 | Mozilla Public License 2.0
MS-LPL | Microsoft Limited Public License
MS-PL | Microsoft Public License
MS-RL | Microsoft Reciprocal License
MTLL | Matrix Template Library License
Mackerras-3-Clause-acknowledgment | Mackerras 3-Clause - acknowledgment variant
Mackerras-3-Clause | Mackerras 3-Clause License
MakeIndex | MakeIndex License
Martin-Birgmeier | Martin Birgmeier License
McPhee-slideshow | McPhee Slideshow License
Minpack | Minpack License
MirOS | The MirOS Licence
Motosoto | Motosoto License
MulanPSL-1.0 | Mulan Permissive Software License, Version 1
MulanPSL-2.0 | Mulan Permissive Software License, Version 2
Multics | Multics License
Mup | Mup License
NAIST-2003 | Nara Institute of Science and Technology License (2003)
NASA-1.3 | NASA Open Source Agreement 1.3
NBPL-1.0 | Net Boolean Public License v1
NCBI-PD | NCBI Public Domain Notice
NCGL-UK-2.0 | Non-Commercial Government Licence
NCL | NCL Source Code License
NCSA | University of Illinois/NCSA Open Source License
NGPL | Nethack General Public License
NICTA-1.0 | NICTA Public Software License, Version 1.0
NIST-PD-TNT | NIST    Public Domain Notice TNT variant
NIST-PD-fallback | NIST Public Domain Notice with license fallback
NIST-PD | NIST Public Domain Notice
NIST-Software | NIST Software License
NLOD-1.0 | Norwegian Licence for Open Government Data (NLOD) 1.0
NLOD-2.0 | Norwegian Licence for Open Government Data (NLOD) 2.0
NLPL | No Limit Public License
NOSL | Netizen Open Source License
NPL-1.0 | Netscape Public License v1.0
NPL-1.1 | Netscape Public License v1.1
NPOSL-3.0 | Non-Profit Open Software License 3.0
NRL | NRL License
NTIA-PD | NTIA Public Domain Notice
NTP-0 | NTP No Attribution
NTP | NTP License
Naumen | Naumen Public License
NetCDF | NetCDF license
Newsletr | Newsletr License
Nokia | Nokia Open Source License
Noweb | Noweb License
O-UDA-1.0 | Open Use of Data Agreement v1.0
OAR | OAR License
OCCT-PL | Open CASCADE Technology Public License
OCLC-2.0 | OCLC Research Public License 2.0
ODC-By-1.0 | Open Data Commons Attribution License v1.0
ODbL-1.0 | Open Data Commons Open Database License v1.0
OFFIS | OFFIS License
OFL-1.0-RFN | SIL Open Font License 1.0 with Reserved Font Name
OFL-1.0-no-RFN | SIL Open Font License 1.0 with no Reserved Font Name
OFL-1.0 | SIL Open Font License 1.0
OFL-1.1-RFN | SIL Open Font License 1.1 with Reserved Font Name
OFL-1.1-no-RFN | SIL Open Font License 1.1 with no Reserved Font Name
OFL-1.1 | SIL Open Font License 1.1
OGC-1.0 | OGC Software License, Version 1.0
OGDL-Taiwan-1.0 | Taiwan Open Government Data License, version 1.0
OGL-Canada-2.0 | Open Government Licence - Canada
OGL-UK-1.0 | Open Government Licence v1.0
OGL-UK-2.0 | Open Government Licence v2.0
OGL-UK-3.0 | Open Government Licence v3.0
OGTSL | Open Group Test Suite License
OLDAP-1.1 | Open LDAP Public License v1.1
OLDAP-1.2 | Open LDAP Public License v1.2
OLDAP-1.3 | Open LDAP Public License v1.3
OLDAP-1.4 | Open LDAP Public License v1.4
OLDAP-2.0.1 | Open LDAP Public License v2.0.1
OLDAP-2.0 | Open LDAP Public License v2.0 (or possibly 2.0A and 2.0B)
OLDAP-2.1 | Open LDAP Public License v2.1
OLDAP-2.2.1 | Open LDAP Public License v2.2.1
OLDAP-2.2.2 | Open LDAP Public License 2.2.2
OLDAP-2.2 | Open LDAP Public License v2.2
OLDAP-2.3 | Open LDAP Public License v2.3
OLDAP-2.4 | Open LDAP Public License v2.4
OLDAP-2.5 | Open LDAP Public License v2.5
OLDAP-2.6 | Open LDAP Public License v2.6
OLDAP-2.7 | Open LDAP Public License v2.7
OLDAP-2.8 | Open LDAP Public License v2.8
OLFL-1.3 | Open Logistics Foundation License Version 1.3
OML | Open Market License
OPL-1.0 | Open Public License v1.0
OPL-UK-3.0 | United    Kingdom Open Parliament Licence v3.0
OPUBL-1.0 | Open Publication License v1.0
OSC-1.0 | OSC License 1.0
OSET-PL-2.1 | OSET Public License version 2.1
OSL-1.0 | Open Software License 1.0
OSL-1.1 | Open Software License 1.1
OSL-2.0 | Open Software License 2.0
OSL-2.1 | Open Software License 2.1
OSL-3.0 | Open Software License 3.0
OSSP | OSSP License
OpenMDW-1.0 | OpenMDW License Agreement v1.0
OpenPBS-2.3 | OpenPBS v2.3 Software License
OpenSSL-standalone | OpenSSL License - standalone
OpenSSL | OpenSSL License
OpenVision | OpenVision License
PADL | PADL License
PDDL-1.0 | Open Data Commons Public Domain Dedication & License 1.0
PHP-3.01 | PHP License v3.01
PHP-3.0 | PHP License v3.0
PPL | Peer Production License
PSF-2.0 | Python Software Foundation License 2.0
ParaType-Free-Font-1.3 | ParaType Free Font Licensing Agreement v1.3
Parity-6.0.0 | The Parity Public License 6.0.0
Parity-7.0.0 | The Parity Public License 7.0.0
Pixar | Pixar License
Plexus | Plexus Classworlds License
PolyForm-Noncommercial-1.0.0 | PolyForm Noncommercial License 1.0.0
PolyForm-Small-Business-1.0.0 | PolyForm Small Business License 1.0.0
PostgreSQL | PostgreSQL License
Python-2.0.1 | Python License 2.0.1
Python-2.0 | Python License 2.0
QPL-1.0-INRIA-2004 | Q Public License 1.0 - INRIA 2004 variant
QPL-1.0 | Q Public License 1.0
Qhull | Qhull License
RHeCos-1.1 | Red Hat eCos Public License v1.1
RPL-1.1 | Reciprocal Public License 1.1
RPL-1.5 | Reciprocal Public License 1.5
RPSL-1.0 | RealNetworks Public Source License v1.0
RSA-MD | RSA Message-Digest License
RSCPL | Ricoh Source Code Public License
Rdisc | Rdisc License
Ruby-pty | Ruby pty extension license
Ruby | Ruby License
SAX-PD-2.0 | Sax Public Domain Notice 2.0
SAX-PD | Sax Public Domain Notice
SCEA | SCEA Shared Source License
SGI-B-1.0 | SGI Free Software License B v1.0
SGI-B-1.1 | SGI Free Software License B v1.1
SGI-B-2.0 | SGI Free Software License B v2.0
SGI-OpenGL | SGI OpenGL License
SGMLUG-PM | SGMLUG Parser Materials License
SGP4 | SGP4 Permission Notice
SHL-0.51 | Solderpad Hardware License, Version 0.51
SHL-0.5 | Solderpad Hardware License v0.5
SISSL-1.2 | Sun Industry Standards Source License v1.2
SISSL | Sun Industry Standards Source License v1.1
SL | SL License
SMAIL-GPL | SMAIL General Public License
SMLNJ | Standard ML of New Jersey License
SMPPL | Secure Messaging Protocol Public License
SNIA | SNIA Public License 1.1
SOFA | SOFA Software License
SPL-1.0 | Sun Public License v1.0
SSH-OpenSSH | SSH OpenSSH license
SSH-short | SSH short notice
SSLeay-standalone | SSLeay License - standalone
SSPL-1.0 | Server Side Public License, v 1
SUL-1.0 | Sustainable Use License v1.0
SWL | Scheme Widget Library (SWL) Software License Agreement
Saxpath | Saxpath License
SchemeReport | Scheme Language Report License
Sendmail-8.23 | Sendmail License 8.23
Sendmail-Open-Source-1.1 | Sendmail Open Source License v1.1
Sendmail | Sendmail License
SimPL-2.0 | Simple Public License 2.0
Sleepycat | Sleepycat License
Soundex | Soundex License
Spencer-86 | Spencer License 86
Spencer-94 | Spencer License 94
Spencer-99 | Spencer License 99
SugarCRM-1.1.3 | SugarCRM Public License v1.1.3
Sun-PPP-2000 | Sun PPP License (2000)
Sun-PPP | Sun PPP License
SunPro | SunPro License
Symlinks | Symlinks License
TAPR-OHL-1.0 | TAPR Open Hardware License v1.0
TCL | TCL/TK License
TCP-wrappers | TCP Wrappers License
TGPPL-1.0 | Transitive Grace Period Public Licence 1.0
TMate | TMate Open Source License
TORQUE-1.1 | TORQUE v2.5+ Software License v1.1
TOSL | Trusster Open Source License
TPDL | Time::ParseDate License
TPL-1.0 | THOR Public License 1.0
TTWL | Text-Tabs+Wrap License
TTYP0 | TTYP0 License
TU-Berlin-1.0 | Technische Universitaet Berlin License 1.0
TU-Berlin-2.0 | Technische Universitaet Berlin License 2.0
TekHVC | TekHVC License
TermReadKey | TermReadKey License
ThirdEye | ThirdEye License
TrustedQSL | TrustedQSL License
UCAR | UCAR License
UCL-1.0 | Upstream Compatibility License v1.0
UMich-Merit | Michigan/Merit Networks License
UPL-1.0 | Universal Permissive License v1.0
URT-RLE | Utah Raster Toolkit Run Length Encoded License
Ubuntu-font-1.0 | Ubuntu Font Licence v1.0
UnRAR | UnRAR License
Unicode-3.0 | Unicode License v3
Unicode-DFS-2015 | Unicode License Agreement - Data Files and Software (2015)
Unicode-DFS-2016 | Unicode License Agreement - Data Files and Software (2016)
Unicode-TOU | Unicode Terms of Use
UnixCrypt | UnixCrypt License
Unlicense-libtelnet | Unlicense - libtelnet variant
Unlicense-libwhirlpool | Unlicense - libwhirlpool variant
Unlicense | The Unlicense
VOSTROM | VOSTROM Public License for Open Source
VSL-1.0 | Vovida Software License v1.0
Vim | Vim License
Vixie-Cron | Vixie Cron License
W3C-19980720 | W3C Software Notice and License (1998-07-20)
W3C-20150513 | W3C Software Notice and Document License (2015-05-13)
W3C | W3C Software Notice and License (2002-12-31)
WTFNMFPL | Do What The F*ck You Want To But It's Not My Fault Public License
WTFPL | Do What The F*ck You Want To Public License
Watcom-1.0 | Sybase Open Watcom Public License 1.0
Widget-Workshop | Widget Workshop License
WordNet | WordNet License
Wsuipa | Wsuipa License
X11-distribute-modifications-variant | X11 License Distribution Modification Variant
X11-no-permit-persons | X11 no permit persons clause
X11-swapped | X11 swapped final paragraphs
X11 | X11 License
XFree86-1.1 | XFree86 License 1.1
XSkat | XSkat License
Xdebug-1.03 | Xdebug License v 1.03
Xerox | Xerox License
Xfig | Xfig License
Xnet | X.Net License
YPL-1.0 | Yahoo! Public License v1.0
YPL-1.1 | Yahoo! Public License v1.1
ZPL-1.1 | Zope Public License 1.1
ZPL-2.0 | Zope Public License 2.0
ZPL-2.1 | Zope Public License 2.1
Zed | Zed License
Zeeff | Zeeff License
Zend-2.0 | Zend License v2.0
Zimbra-1.3 | Zimbra Public License v1.3
Zimbra-1.4 | Zimbra Public License v1.4
Zlib | zlib License
any-OSI-perl-modules | Any OSI License - Perl Modules
any-OSI | Any OSI License
bcrypt-Solar-Designer | bcrypt Solar Designer License
blessing | SQLite Blessing
bzip2-1.0.6 | bzip2 and libbzip2 License v1.0.6
check-cvs | check-cvs License
checkmk | Checkmk License
copyleft-next-0.3.0 | copyleft-next 0.3.0
copyleft-next-0.3.1 | copyleft-next 0.3.1
curl | curl License
cve-tou | Common Vulnerability Enumeration ToU License
diffmark | diffmark license
dtoa | David M. Gay dtoa License
dvipdfm | dvipdfm License
eGenix | eGenix.com Public License 1.1.0
etalab-2.0 | Etalab Open License 2.0
fwlw | fwlw License
gSOAP-1.3b | gSOAP Public License v1.3b
generic-xts | Generic XTS License
gnuplot | gnuplot License
gtkbook | gtkbook License
hdparm | hdparm License
hyphen-bulgarian | hyphen-bulgarian License
iMatix | iMatix Standard Function Library Agreement
jove | Jove License
libpng-1.6.35 | PNG Reference Library License v1 (for libpng 0.5 through 1.6.35)
libpng-2.0 | PNG Reference Library version 2
libselinux-1.0 | libselinux public domain notice
libtiff | libtiff License
libutil-David-Nugent | libutil David Nugent License
lsof | lsof License
magaz | magaz License
mailprio | mailprio License
man2html | man2html License
metamail | metamail License
mpi-permissive | mpi Permissive License
mpich2 | mpich2 License
mplus | mplus Font License
ngrep | ngrep License
pkgconf | pkgconf License
pnmstitch | pnmstitch License
psfrag | psfrag License
psutils | psutils License
python-ldap | Python ldap License
radvd | radvd License
snprintf | snprintf License
softSurfer | softSurfer License
ssh-keyscan | ssh-keyscan License
swrule | swrule License
threeparttable | threeparttable License
ulem | ulem License
w3m | w3m License
wwl | WWL License
xinetd | xinetd License
xkeyboard-config-Zinoviev | xkeyboard-config Zinoviev License
xlock | xlock License
xpp | XPP License
xzoom | xzoom License
zlib-acknowledgement | zlib/libpng License with Acknowledgement

# SUSE Additions

|License Tag|
|-----------|
|LicenseRef-SUSE-EULA|
|LicenseRef-SUSE-Freeware|
|LicenseRef-SUSE-GPL-2.0-with-openssl-exception|
|LicenseRef-SUSE-NonFree|
|LicenseRef-SUSE-Permissive|
|LicenseRef-SUSE-Public-Domain|
|SUSE-BSD-3-Clause-with-non-nuclear-addition|
|SUSE-CC-Sampling-Plus-1.0|
|SUSE-CPL-0.5|
|SUSE-CacertRoot|
|SUSE-Copyleft-Next-0.3.0|
|SUSE-Curb|
|SUSE-DMTF|
|SUSE-Docbook-XSL|
|SUSE-Egenix-1.1.0|
|SUSE-FHS|
|SUSE-FLTK|
|SUSE-Firmware|
|SUSE-Free-Art-1.3|
|SUSE-GL2PS-2.0|
|SUSE-GPL-2.0+-with-openssl-exception|
|SUSE-GPL-2.0+-with-sane-exception|
|SUSE-GPL-2.0-with-FLOSS-exception|
|SUSE-GPL-2.0-with-OSI-exception|
|SUSE-GPL-2.0-with-linking-exception|
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
|SUSE-Permissive-Modify-By-Patch|
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
|SUSE-TeX|
|SUSE-Ubuntu-Font-License-1.0|
|SUSE-XDebug|
|SUSE-XFree86-with-font-exception|
|SUSE-XSL-Lint|
|SUSE-Xano|
|SUSE-Xenonsoft-1.00|
|SUSE-mirror|
|SUSE-wxWidgets-3.1|
