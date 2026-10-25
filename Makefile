# This is to force regenerating everytime you run make as we rely on web data
.PHONY: spec_cleaner/data/pkgconfig_conversions.txt spec_cleaner/data/licenses_changes.txt spec_cleaner/data/license_exceptions.txt spec_cleaner/data/cmake_conversions.txt spec_cleaner/data/tex_conversions.txt spec_cleaner/data/perl_conversions.txt spec_cleaner/data/licenses.toml spec_cleaner/data/licenses-suse.toml spec_cleaner/data/macro_functions.txt

all: spec_cleaner/data/pkgconfig_conversions.txt spec_cleaner/data/licenses_changes.txt spec_cleaner/data/license_exceptions.txt spec_cleaner/data/cmake_conversions.txt spec_cleaner/data/tex_conversions.txt spec_cleaner/data/perl_conversions.txt spec_cleaner/data/licenses.toml spec_cleaner/data/licenses-suse.toml

distro = leap/16.0

spec_cleaner/data/tex_conversions.txt: conversions-update.pl conversions-update.sh
	bash conversions-update.sh tex $(distro) > $@.tmp && mv $@.tmp $@ || { rm -f $@.tmp; false; }

spec_cleaner/data/pkgconfig_conversions.txt: conversions-update.pl conversions-update.sh
	bash conversions-update.sh pkgconfig $(distro) > $@.tmp && mv $@.tmp $@ || { rm -f $@.tmp; false; }

spec_cleaner/data/perl_conversions.txt: conversions-update.pl conversions-update.sh
	bash conversions-update.sh perl $(distro) > $@.tmp && mv $@.tmp $@ || { rm -f $@.tmp; false; }

spec_cleaner/data/cmake_conversions.txt: conversions-update.pl conversions-update.sh
	bash conversions-update.sh cmake $(distro) > $@.tmp && mv $@.tmp $@ || { rm -f $@.tmp; false; }

# The macro snapshot tracks the rolling development distribution, not
# $(distro): it has to cover the macros the Factory corpus uses. It is
# deliberately not part of 'all' -- a release-time regeneration would
# diff on ordinary Tumbleweed drift; the macro-sync workflow owns its
# freshness instead. The builtin section is carried over on refresh; it
# is re-recorded by a manual generator run on a current-rpm host.
spec_cleaner/data/macro_functions.txt: generate-macro-functions.py
	python3 generate-macro-functions.py --keep-builtins --out $@

# one license-update.sh run produces both files; the empty recipe keeps plain
# make (and make -j) from running the script twice
spec_cleaner/data/licenses_changes.txt: license-update.sh
	bash license-update.sh

spec_cleaner/data/license_exceptions.txt: spec_cleaner/data/licenses_changes.txt

spec_cleaner/data/licenses.toml: generate-licenses-for-rpmlint.py spec_cleaner/data/licenses_changes.txt spec_cleaner/data/license_exceptions.txt
	python3 generate-licenses-for-rpmlint.py $@

spec_cleaner/data/licenses-suse.toml: generate-licenses-for-rpmlint.py spec_cleaner/data/licenses_changes.txt spec_cleaner/data/license_exceptions.txt
	python3 generate-licenses-for-rpmlint.py --suse $@
