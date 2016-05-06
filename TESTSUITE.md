How to write tests for spec-cleaner
===================================

Generally speaking one of the most important parts of what spec-cleaner does is
the reliability. For that we need huge and comprehensive testsuite on
everything the tool is doing.

Even if you don't want/know how to fix the code the testsuite updates are
highly appreciated.

Testsuite of spec-cleaner is pretty straight-forward it has input and expected
output for regular and minimal output. For that we have 3 folders:

+ in/ - SOMETHING.spec starting code/point for your test
+ out/ - SOMETHING.spec with regular spec-cleaner run
+ out-minimal/ - SOMETHING.spec with minimal spec-cleaner run

Since sometimes spec-cleaner produces large differences following commands will
help you to achieve the easiest workflow:

```bash
$ vi tests/in/myfeaturebug.spec
*hackyhacky*
$ spec-cleaner --no-header tests/in/myfeaturebug.spec > tests/out/myfeaturebug.spec
$ vi tests/out/myfeaturebug.spec
*change any problematic part to what it should look like correctly*
$ spec-cleaner --no-header -m tests/in/myfeaturebug.spec > tests/out-minimal/myfeaturebug.spec
$ vi tests/out-minimal/myfeaturebug.spec
*change any problematic part to what it shoudl look like correctly*
```

That's it. Now just git add . ; commit and pull request :-)
