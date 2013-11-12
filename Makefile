all: upkg

upkg: pkgconfig-update.sed pkgconfig-update.sh 
	sh pkgconfig-update.sh 13.1

test: check

check:
	echo "true"
