import argparse
import json
import sys
from pathlib import Path
from .core import analyze, generate_plan


def main():
    parser = argparse.ArgumentParser(description='Review supported OpenAPI breaking changes and optionally draft a Nemotron migration plan.')
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('--live', action='store_true', help='Call NVIDIA model on Nebius Token Factory using configured account credits')
    args = parser.parse_args()
    try:
        specs = []
        for path in (args.before, args.after):
            if path.stat().st_size > 500_000:
                raise ValueError('Each specification must be under 500 KB.')
            specs.append(json.loads(path.read_text()))
        report = analyze(*specs)
        report['mode'] = 'live' if args.live else 'analysis-only'
        if args.live:
            report['migration'] = generate_plan(report)
        print(json.dumps(report, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'ContractPilot: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
