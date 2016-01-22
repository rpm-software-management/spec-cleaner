all: data/pkgconfig_conversions.txt data/licenses_changes.txt

data/pkgconfig_conversions.txt: pkgconfig-update.sed pkgconfig-update.sh
	@sh pkgconfig-update.sh leap/42.1 > $@

data/licenses_changes.txt: license-update.sh
	@sh license-update.sh
