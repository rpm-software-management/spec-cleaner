# spec-cleaner design notes

A 5-minute orientation for contributors (human or agent): what the tool
does, how the code is organized, and the non-obvious decisions you need
to know before changing anything. For commands, lint, and generated files
see `AGENTS.md`; for writing tests see `TESTSUITE.md`.

## What it does

spec-cleaner normalizes RPM spec files: whitespace, macro bracing,
dependency formatting, preamble ordering, license handling, and similar
cosmetic-but-consequential cleanups. It is **not** a linter — it rewrites
the file. The invariant is: cleaning must be **idempotent**
(`clean(clean(x)) == clean(x)`) and must not lose meaningful content
beyond the deliberate removals (changelog entries, the `%clean` body,
deprecated tags, Authors blocks, non-SUSE header lines under
`--suse-copyright`).

## Pipeline

```
spec file → RpmSpecCleaner.run() → line-by-line section detection
          → per-section Section.add() processing → Section.output()
          → rewritten spec file
```

1. `RpmSpecCleaner.__init__` pre-scans the file: defined macros
   (`_find_defined_macros`), bare `%patch` (`_find_bare_patch`),
   `%lang_package` (`_find_lang_package`), skip-parser markers.
2. `run()` walks lines. `_detect_new_section()` decides, for each line,
   whether it starts a new `Section` subclass instance. The current
   section's `add()` processes the line.
3. At the end (or on section transition), `Section.output()` writes the
   section's lines, appending a trailing empty line per its rules.

## Module guide

| Module | Role |
|---|---|
| `__init__.py` | `process_args()`, `main()` — CLI entry point |
| `rpmcleaner.py` | `RpmSpecCleaner` — orchestrator, section detection |
| `rpmsection.py` | `Section` — line storage, condition tracking, `output()`, and the shared per-line cleanups (`_complete_cleanup`: `embrace_macros`, `replace_known_dirs`, `replace_utils`, ...) |
| `rpmpreamble.py` | `RpmPreamble` — `Name:`/`Version:`/deps header; the largest class. Also `RpmPreambleChunk` (preamble lines between sections) |
| `rpmpackage.py` | `RpmPackage(RpmPreamble)` — `%package` subpackage headers, `-lang` / `%lang_package` logic |
| `rpmpreambleelements.py` | `RpmPreambleElements` — per-paragraph category store: ordering, sorting, dedup and `flatten_output()` (tag parsing is in `RpmPreamble._handle_*`) |
| `rpmdescription.py` | `RpmDescription` — `%description` bodies |
| `rpmprune.py` | `RpmClean` (`%clean`), `RpmChangelog` (`%changelog`) |
| `rpmfiles.py` | `RpmFiles` — `%files` sections |
| `rpmscriplets.py` | `RpmScriptlets` — `%pre`/`%post`/triggers |
| `rpmbuild.py` / `rpminstall.py` / `rpmprep.py` | `%build`, `%install`, `%prep` |
| `rpmcopyright.py` | SUSE copyright header handling |
| `rpmsourcelist.py` | `RpmSourceList` — `%sourcelist` / `%patchlist` sections (plain pass-through; `Source:`/`Patch:` tags are handled in `RpmPreamble`) |
| `rpmcheck.py` | `RpmCheck` — `%check` section |
| `rpmexception.py` | exception hierarchy |
| `dependency_parser.py` | `DependencyParser` — parses `Requires:`/`BuildRequires:` tokens |
| `rpmrequirestoken.py` | `RpmRequiresToken` — single dependency token |
| `rpmregexp.py` | `Regexp` — the shared compiled regexes (the dependency tokenizer and a few helpers keep their own) |
| `rpmhelpers.py` | `parse_rpm_showrc()` and small shared helpers |
| `fileutils.py` | file I/O helpers |

## Live runtime dependencies

The tool's output depends on the host it runs on. Know these before
debugging "works on my machine" differences:

- **`rpm --showrc`.** Without `rpm` (e.g. macOS) the tool aborts with
  `Could not run "rpm --showrc"`. With a different rpm macro set the
  unbrace list differs, and so does the output. Tests mock this via
  `tests/conftest.py` (but `test_utf8_in_non_utf8_locale` runs the
  tool in a subprocess, where the mock does not apply).
- **HTTPS probes.** The `https-probe/` tests patch `rpmpreamble.urlopen`
  so every probe succeeds; the `webtest` mark gates the `web/` tests.
  Some unmarked `out/` cases (e.g. `source_https.spec`) still probe the
  network, so `-m "not webtest"` is not fully offline.
- **Generated data files.** `data/licenses_changes.txt` (always used) and
  `data/*_conversions.txt` (with `--pkgconfig`/`--perl`/`--cmake`/`--tex`)
  are refreshed from the network by `make` — output can shift after a
  refresh without any code change. (`licenses*.toml` are regenerated too
  but only feed rpmlint.)

## Key decisions and gotchas

- **Macros on the unbrace list stay braceless.** `embrace_macros` braces
  every macro and then unbraces the names on the list, which is
  `data/excludes-bracketing.txt`, plus parametric macros from
  `rpm --showrc`, plus parametric `%define`/`%global` in the spec.
  `%ldconfig_scriptlets -n foo` stays braceless because it is listed in
  `excludes-bracketing.txt` — `%{macro} args` does not pass args to the
  macro, so bracing it would break the build. To keep a new args-taking
  macro braceless on every host, add it to `excludes-bracketing.txt`.
- **`RpmPreamble` is the complex core.** It handles multi-line
  `%define`/`%global` bodies and continued `%if` lines, conditional
  blocks, and dependency tokenization via `DependencyParser`; subpackage
  headers use its subclass `RpmPackage`. Most bugs live here.
- **`--perl` rewrites perl package dependencies to `perl()` symbols**,
  one per module listed in `data/perl_conversions.txt`;
  Provides/Obsoletes are left alone. `--pkgconfig`, `--cmake` and
  `--tex` work the same way.
- **TeX Live specs are excluded from sweeps, permanently.**
  `texlive.spec` and `texlive-*` are generated, so the corpus sweep
  skips them. Nothing in the tool enforces this — it is a policy for
  sweeps and contributors.
- **Docstrings describe the present, never the past.** No "moved from X",
  "formerly Y", "split out of Z" — that's what `git log` is for.
  (Ruff enforces the format: single quotes, line length 100, summary on
  the *second* docstring line per pydocstyle.)

## Corpus sweeps

A monthly sweep (also manually dispatchable as a pre-release gate) runs
the cleaner over all openSUSE Tumbleweed (Factory) specs, looking for
crashes and non-idempotent output. Findings are filed as issues with the
`corpus-sweep` label. See `.github/workflows/distro-corpus-sweep.yml`.
