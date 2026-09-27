How to write tests for spec-cleaner
===================================

Generally speaking one of the most important parts of what spec-cleaner does is
the reliability. For that we need huge and comprehensive testsuite on
everything the tool is doing.

Even if you don't want/know how to fix the code the testsuite updates are
highly appreciated.

## Acceptance tests (fixture-driven)

The primary regression suite. Test cases are discovered from the
**expected-output** directories; the input is always `tests/in/<same name>.spec`:

+ in/ - SOMETHING.spec starting code/point for your test
+ out/ - SOMETHING.spec with regular spec-cleaner run
+ out-minimal/ - SOMETHING.spec with minimal (`-m`) spec-cleaner run
+ keep-space/ - SOMETHING.spec where spacing must be preserved
+ web/ - SOMETHING.spec exercising URL handling
+ https-probe/ - SOMETHING.spec with a patched urlopen whose https probe always succeeds
+ header/ - SOMETHING.spec with `minimal` and `suse_copyright` instead of `pkgconfig`

Every case runs twice: the cleaned output is cleaned again and must still
equal the expected file (idempotency). Non-idempotent changes fail here.

Tests run with `copyright_year=2013`; `out/`, `out-minimal/`, `web/` and
`https-probe/` also use `pkgconfig=True` (`keep-space/`, `header/` and the
one-off option tests do not). Generating a `keep-space/` or `header/`
expected file with `--pkgconfig` gives the wrong output. Generate expected
output with:

```bash
$ vi tests/in/myfeaturebug.spec
*hackyhacky*
$ spec-cleaner --pkgconfig --copyright-year 2013 tests/in/myfeaturebug.spec > tests/out/myfeaturebug.spec
$ vi tests/out/myfeaturebug.spec
*change any problematic part to what it should look like correctly*
$ spec-cleaner --pkgconfig --copyright-year 2013 -m tests/in/myfeaturebug.spec > tests/out-minimal/myfeaturebug.spec
$ vi tests/out-minimal/myfeaturebug.spec
*change any problematic part to what it shoudl look like correctly*
```

One-off option tests (`tex`, `perl`, `cmake`, `group`) are listed explicitly
in `test_single_output` in `tests/acceptance-tests.py`, not auto-discovered.

That's it. Now just git add . ; commit and pull request :-)

## Unit and CLI tests

Not everything fits the fixture model. Use the established test files:

+ tests/cli-tests.py - `process_args()`/`main()` via monkeypatched argv
+ tests/unit-tests.py - targeted unit tests for helpers
+ tests/rpmsection-tests.py, tests/rpmpreamble-tests.py, ... - per-module
  unit tests; add here when pinning behavior that fixtures cannot express
+ tests/dependency-parser-tests.py - `DependencyParser` tokenization

Prefer the acceptance fixtures when they can express the case; add unit
tests only where they pin something fixtures can't.

## Test environment notes

+ tests/conftest.py has an autouse fixture mocking
  `spec_cleaner.rpmcleaner.parse_rpm_showrc`, so the in-process tests run
  without the `rpm` binary; `test_utf8_in_non_utf8_locale` and the CLI
  used to generate fixtures still need it.
+ `test_web_output` (the `web/` fixtures) is marked `webtest`; skip it
  with `-m "not webtest"`. Some `out/` fixtures (e.g. `source_https.spec`)
  still probe the network.
+ Run from the repo root: `pytest` (pytest.ini adds `-n auto --cov`).
