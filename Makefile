# This is to force regenerating everytime you run make as we rely on web data
.PHONY: data/pkgconfig_conversions.txt data/licenses_changes.txt data/cmake_conversions.txt data/tex_conversions.txt data/perl_conversions.txt

all: data/pkgconfig_conversions.txt data/licenses_changes.txt data/cmake_conversions.txt data/tex_conversions.txt data/perl_conversions.txt

data/tex_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh tex leap/42.1 > $@

data/pkgconfig_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh pkgconfig leap/42.1 > $@

data/perl_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh perl leap/42.1 > $@

data/cmake_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh cmake leap/42.1 > $@

data/licenses_changes.txt: license-update.sh
	sh license-update.sh
