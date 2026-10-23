#!BuildIgnore: headerone headertwo
#
# Copyright header for the pragma minimal test
Name:           pragmaminimal
BuildRequires:  bar
BuildRequires:  compiler
BuildRequires:  foo >= 1.0
BuildRequires:  other
#!BuildRequires: qualified [i586]
#!BuildIgnore:  kernelfour
#!BuildIgnore:  kernelone
#!BuildIgnore:  kernelthree
#!BuildIgnore:  kerneltwo
#!BuildIgnore:  secondeight
#!BuildIgnore:  secondfive
#!BuildIgnore:  secondfour
#!BuildIgnore:  secondone
#!BuildIgnore:  secondseven
#!BuildIgnore:  secondsix
#!BuildIgnore:  secondthree
#!BuildIgnore:  secondtwo

%changelog
