# This is to force regenerating everytime you run make as we rely on web data
.PHONY: data/pkgconfig_conversions.txt data/licenses_changes.txt data/cmake_conversions.txt data/tex_conversions.txt data/perl_conversions.txt data/licenses.toml data/licenses-suse.toml

all: data/pkgconfig_conversions.txt data/licenses_changes.txt data/cmake_conversions.txt data/tex_conversions.txt data/perl_conversions.txt data/licenses.toml data/licenses-suse.toml

distro = leap/15.2

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

data/licenses.toml: generate-licenses-for-rpmlint.py data/licenses_changes.txt
	./generate-licenses-for-rpmlint.py $@

data/licenses-suse.toml: generate-licenses-for-rpmlint.py data/licenses_changes.txt
	./generate-licenses-for-rpmlint.py --suse $@
