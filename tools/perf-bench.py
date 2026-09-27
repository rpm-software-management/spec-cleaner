#!/usr/bin/env python3
"""
Perf benchmark harness.

Times RpmSpecCleaner over the fixed subset in tests/perf-specs/.

JSON with per-spec median wall times goes to stdout; the human-readable
summary table goes to stderr so stdout stays parseable.
"""

import argparse
import json
import statistics
import sys
import tempfile
import time
from pathlib import Path

from spec_cleaner import RpmSpecCleaner

OPTION_PRESETS = {
    'pkgconfig': False,
    'inline': False,
    'diff': False,
    'diff_prog': 'vimdiff',
    'minimal': False,
    'no_curlification': False,
    'suse_copyright': False,
    'copyright_year': 2013,
    'remove_groups': False,
    'tex': False,
    'perl': False,
    'cmake': False,
    'keep_space': False,
}

MODES = ('normal', 'minimal')


def parse_args(argv=None):
    """Parse command-line flags."""
    parser = argparse.ArgumentParser(
        description='Benchmark RpmSpecCleaner on tests/perf-specs/ (JSON to stdout).'
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=3,
        help='Clean runs per spec per mode; median is reported (default: 3).',
    )
    parser.add_argument(
        '--mode',
        choices=('normal', 'minimal', 'both'),
        default='both',
        help='Which cleaner mode(s) to benchmark (default: both).',
    )
    parser.add_argument(
        '--manifest',
        type=Path,
        default=Path('tests/perf-specs/MANIFEST.txt'),
        help='Manifest listing the benchmark specs (default: %(default)s).',
    )
    args = parser.parse_args(argv)
    if args.runs < 1:
        parser.error('--runs must be >= 1')
    return args


def load_manifest(manifest):
    """
    Collect spec filenames from manifest entry lines in order.

    Returns the names plus any non-comment line that did not parse, so a
    typo cannot silently shrink the benchmark.
    """
    specs = []
    malformed = []
    for line in Path(manifest).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        head, sep, _ = line.partition('|')
        name = head.strip()
        if sep and name.endswith('.spec') and '/' not in name and name not in specs:
            specs.append(name)
        else:
            malformed.append(line)
    return specs, malformed


def clean_once(spec_path, minimal):
    """Clean one spec once, timing constructor plus run."""
    if minimal:
        mode_options = {'pkgconfig': True, 'minimal': True}
    else:
        mode_options = {'pkgconfig': True}
    with tempfile.NamedTemporaryFile(suffix='.spec', delete=False) as tmp:
        out_path = tmp.name
    try:
        full_options = {'specfile': str(spec_path), 'output': out_path}
        full_options.update(OPTION_PRESETS)
        full_options.update(mode_options)
        start = time.perf_counter()
        cleaner = RpmSpecCleaner(full_options)
        cleaner.run()
        return time.perf_counter() - start
    finally:
        Path(out_path).unlink(missing_ok=True)


def main(argv=None):
    """Run the benchmark and report JSON plus a summary table."""
    args = parse_args(argv)
    if args.mode == 'both':
        modes = list(MODES)
    else:
        modes = [args.mode]
    try:
        specs, malformed = load_manifest(args.manifest)
    except OSError as exc:
        print(f'ERROR: cannot read manifest {args.manifest}: {exc}', file=sys.stderr)
        return 2
    if malformed:
        print(f'ERROR: {len(malformed)} malformed manifest line(s):', file=sys.stderr)
        for line in malformed:
            print(f'ERROR: {line}', file=sys.stderr)
        return 2
    if not specs:
        print(f'ERROR: no specs found in manifest {args.manifest}', file=sys.stderr)
        return 2
    spec_dir = args.manifest.parent
    failures = []
    results = []
    wall_start = time.perf_counter()
    for spec in specs:
        spec_path = spec_dir / spec
        if not spec_path.is_file():
            failures.append(f'{spec}: manifest entry missing ({spec_path})')
            continue
        size_b = spec_path.stat().st_size
        with open(spec_path, encoding='utf-8', errors='replace') as handle:
            lines = sum(1 for _ in handle)
        for mode in modes:
            minimal = mode == 'minimal'
            times = []
            error = None
            for _ in range(args.runs):
                try:
                    times.append(clean_once(spec_path, minimal))
                except Exception as exc:  # noqa: BLE001 - report, don't skip
                    error = f'{spec} [{mode}]: {type(exc).__name__}: {exc}'
                    break
            if error is not None:
                failures.append(error)
                continue
            results.append(
                {
                    'spec': spec,
                    'mode': mode,
                    'runs': args.runs,
                    'times_s': times,
                    'median_s': statistics.median(times),
                    'size_b': size_b,
                    'lines': lines,
                }
            )
    wall_s = time.perf_counter() - wall_start
    payload = {'runs': args.runs, 'modes': modes, 'wall_s': wall_s, 'results': results}
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write('\n')
    total_median = sum(r['median_s'] for r in results)
    print(f'perf-bench: {len(results)} spec-mode cleans, {args.runs} run(s) each', file=sys.stderr)
    print(f'{"spec":42s} {"mode":7s} {"bytes":>7s} {"median_ms":>10s}', file=sys.stderr)
    for entry in results:
        print(
            f'{entry["spec"]:42s} {entry["mode"]:7s} '
            f'{entry["size_b"]:7d} {entry["median_s"] * 1000:10.2f}',
            file=sys.stderr,
        )
    print(f'total median sum: {total_median:.3f}s, wall: {wall_s:.3f}s', file=sys.stderr)
    if failures:
        print(f'ERROR: {len(failures)} spec(s) failed to clean:', file=sys.stderr)
        for failure in failures:
            print(f'ERROR: {failure}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
