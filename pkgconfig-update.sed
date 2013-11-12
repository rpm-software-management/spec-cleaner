/^[[:blank:]]*<location/{
# get package name from location
s@<location href="[^"]\+/\(.*\)-[^-]\+-[^-]\+\.rpm"/>@\1: @
# store it into holdspace
x
d
}

/^[[:blank:]]*<rpm:provides>/{
	# append next line until it is </rpm:provides>
	:provides_loop
	N
	s@[[:blank:]]*</rpm:provides>[[:blank:]]*$@@
	T provides_loop

	# get rid of opening tag as well
	s@^[[:blank:]]*<rpm:provides>[[:blank:]]*\n@@

	# clean-up check state
	t next
	:next

	# transform entries with pkgconfig
	s@[[:blank:]]*<rpm:entry name="pkgconfig(\([^)]\+\))"[^>]*/>[[:blank:]]*\n@\1 @g

	# if there is no pkgconfig entry, just end
	T nothing

	# remove entries without pkgconfig
	s@[[:blank:]]*<rpm:entry name="[^>]*/>[[:blank:]]*\n@@g

	# get back to stored package name
	x

	# append pkgconfig symbols
	G
	# get rid of newline
	s/: \n/: /
	p

	:nothing
	d
	x
	d
}

