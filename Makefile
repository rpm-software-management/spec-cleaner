# This is to force regenerating everytime you run make as we rely on web data
.PHONY: spec_cleaner/data/pkgconfig_conversions.txt spec_cleaner/data/licenses_changes.txt spec_cleaner/data/cmake_conversions.txt spec_cleaner/data/tex_conversions.txt spec_cleaner/data/perl_conversions.txt spec_cleaner/data/licenses.toml spec_cleaner/data/licenses-suse.toml

all: spec_cleaner/data/pkgconfig_conversions.txt spec_cleaner/data/licenses_changes.txt spec_cleaner/data/cmake_conversions.txt spec_cleaner/data/tex_conversions.txt spec_cleaner/data/perl_conversions.txt spec_cleaner/data/licenses.toml spec_cleaner/data/licenses-suse.toml

distro = leap/16.0

spec_cleaner/data/tex_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh tex $(distro) > $@

spec_cleaner/data/pkgconfig_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh pkgconfig $(distro) > $@

spec_cleaner/data/perl_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh perl $(distro) > $@

spec_cleaner/data/cmake_conversions.txt: conversions-update.pl conversions-update.sh
	sh conversions-update.sh cmake $(distro) > $@

spec_cleaner/data/licenses_changes.txt: license-update.sh
	bash license-update.sh

spec_cleaner/data/licenses.toml: generate-licenses-for-rpmlint.py spec_cleaner/data/licenses_changes.txt
	./generate-licenses-for-rpmlint.py $@

spec_cleaner/data/licenses-suse.toml: generate-licenses-for-rpmlint.py spec_cleaner/data/licenses_changes.txt
	./generate-licenses-for-rpmlint.py --suse $@
