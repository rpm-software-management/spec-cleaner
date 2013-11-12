%prep
dos2unix some files
dos2unix -c ascii some files
dos2unix -c iso some files

perl -i -pe 's/\r\n/\n/gs' some files
%__perl -i -pe 's/\r\n/\n/gs' some files
%{__perl} -i -pe 's/\r\n/\n/gs' some files

perl -i -pe "s/\r\n/\n/gs" some files
%__perl -i -pe "s/\r\n/\n/gs" some files
%{__perl} -i -pe "s/\r\n/\n/gs" some files

sed -i 's/\r//' some files
%__sed -i 's/\r//' some files
%{__sed} -i 's/\r//' some files

sed -i "s/\r//" some files
%__sed -i "s/\r//" some files
%{__sed} -i "s/\r//" some files

sed -i 's/\r$//' some files
%__sed -i 's/\r$//' some files
%{__sed} -i 's/\r$//' some files

sed -i "s/\r$//" some files
%__sed -i "s/\r$//" some files
%{__sed} -i "s/\r$//" some files

%build
dos2unix some files
dos2unix -c ascii some files
dos2unix -c iso some files

perl -i -pe 's/\r\n/\n/gs' some files
%__perl -i -pe 's/\r\n/\n/gs' some files
%{__perl} -i -pe 's/\r\n/\n/gs' some files

perl -i -pe "s/\r\n/\n/gs" some files
%__perl -i -pe "s/\r\n/\n/gs" some files
%{__perl} -i -pe "s/\r\n/\n/gs" some files

sed -i 's/\r//' some files
%__sed -i 's/\r//' some files
%{__sed} -i 's/\r//' some files

sed -i "s/\r//" some files
%__sed -i "s/\r//" some files
%{__sed} -i "s/\r//" some files


sed -i 's/\r$//' some files
%__sed -i 's/\r$//' some files
%{__sed} -i 's/\r$//' some files

sed -i "s/\r$//" some files
%__sed -i "s/\r$//" some files
%{__sed} -i "s/\r$//" some files

%install
dos2unix some files
dos2unix -c ascii some files
dos2unix -c iso some files

perl -i -pe 's/\r\n/\n/gs' some files
%__perl -i -pe 's/\r\n/\n/gs' some files
%{__perl} -i -pe 's/\r\n/\n/gs' some files

perl -i -pe "s/\r\n/\n/gs" some files
%__perl -i -pe "s/\r\n/\n/gs" some files
%{__perl} -i -pe "s/\r\n/\n/gs" some files

sed -i 's/\r//' some files
%__sed -i 's/\r//' some files
%{__sed} -i 's/\r//' some files

sed -i "s/\r//" some files
%__sed -i "s/\r//" some files
%{__sed} -i "s/\r//" some files

sed -i 's/\r$//' some files
%__sed -i 's/\r$//' some files
%{__sed} -i 's/\r$//' some files

sed -i "s/\r$//" some files
%__sed -i "s/\r$//" some files
%{__sed} -i "s/\r$//" some files
