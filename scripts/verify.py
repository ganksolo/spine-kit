#!/usr/bin/env python3
"""Run explicitly configured checks. Output is streamed, never persisted by this script."""
import argparse
from pathlib import Path
import json
import os
import signal
import subprocess
import sys
from setup import (atomic_json, digest, event, fingerprint, load_config, now,
                   run_id, safe, validate)


def execute(argv, root, timeout):
    # A separate POSIX session lets timeout stop child processes as well as the parent.
    process = subprocess.Popen(argv, cwd=root, start_new_session=os.name == 'posix')
    try:
        return process.wait(timeout=timeout), False
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        if os.name == 'posix':
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.wait()
        if sys.exc_info()[0] is KeyboardInterrupt:
            raise
        return None, True


def verify(root):
    errors = validate(root)
    if errors:
        raise ValueError('; '.join(errors))
    config = load_config(root)
    rid = run_id()
    before = fingerprint(root)
    config_hash = digest(safe(root, '.spine/config.json').read_bytes())
    event(root, rid, 'verification-start', fingerprint=before, config_sha256=config_hash)
    results = []
    try:
        for check in config['checks']:
            event(root, rid, 'check-start', name=check['name'])
            if 'skip_reason' in check:
                result = {'name': check['name'], 'status': 'skipped', 'reason': check['skip_reason']}
            else:
                try:
                    code, timed_out = execute(check['argv'], root, check.get('timeout_seconds', 120))
                    result = {'name': check['name'], 'status': 'passed' if code == 0 else 'failed',
                              'exit_code': code, 'timed_out': timed_out}
                except OSError as exc:
                    result = {'name': check['name'], 'status': 'failed', 'error_type': type(exc).__name__}
            results.append(result)
            event(root, rid, 'check-result', **result)
        after = fingerprint(root)
        passed = all(r['status'] in ('passed', 'skipped') for r in results) and before == after
        record = {'run_id': rid, 'time': now(), 'status': 'passed' if passed else 'failed',
                  'config_sha256': config_hash, 'fingerprint': after, 'workspace_changed': before != after,
                  'checks': results}
        atomic_json(root, '.spine/setup/verification.json', record)
        event(root, rid, 'verification-finished', **{k: v for k, v in record.items() if k != 'run_id'})
        return record
    except BaseException as exc:
        atomic_json(root, '.spine/setup/verification.json', {'status': 'interrupted', 'run_id': rid})
        event(root, rid, 'verification-interrupted', error_type=type(exc).__name__)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True)
    args = parser.parse_args()
    try:
        result = verify(Path(args.target).resolve())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['status'] == 'passed' else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'spine-kit verify: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
