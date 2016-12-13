# This is to force regenerating everytime you run make as we rely on web data
.PHONY: data/pkgconfig_conversions.txt data/licenses_changes.txt data/cmake_conversions.txt data/tex_conversions.txt data/perl_conversions.txt

all: data/pkgconfig_conversions.txt data/licenses_changes.txt data/cmake_conversions.txt data/tex_conversions.txt data/perl_conversions.txt

distro = leap/42.2

data/tex_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh tex $(distro) > $@

data/pkgconfig_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh pkgconfig $(distro) > $@

data/perl_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh perl $(distro) > $@

data/cmake_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh cmake $(distro) > $@

data/licenses_changes.txt: license-update.sh
	sh license-update.sh
