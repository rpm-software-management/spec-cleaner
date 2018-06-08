%install
grep -E file1
grep -F file2
# we can't run normal grep here thus we run fgrep
cat bla | grep -F something

%changelog
