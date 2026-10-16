#!/usr/bin/env python3
"""spine-kit setup: stdlib only; no implicit installs, shell commands or overwrites."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from uuid import uuid4

SOURCE = Path(__file__).resolve().parent.parent
REPORT_ITEMS = ('inventory', 'project_adaptation', 'agent_entrypoints', 'single_task_source',
                'tools', 'recovery_and_handoff')


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()


def safe(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Expected a nonempty portable relative path')
    p = Path(relative)
    if p.is_absolute() or any(part in ('..', '.') for part in relative.split('/')):
        raise ValueError(f'Unsafe path: {relative}')
    current = root
    for part in p.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'Symlink is not supported: {relative}')
    if not current.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes target: {relative}')
    return current


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def atomic_json(root, relative, value):
    path = safe(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid4().hex + '.tmp')
    try:
        with temporary.open('xb') as stream:
            stream.write(encoded(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def event(root, run_id, event_type, **fields):
    path = safe(root, f'.spine/setup/{run_id}.jsonl')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps({'time': now(), 'run_id': run_id, 'event': event_type,
                                 **fields}, ensure_ascii=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


def run_id():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid4().hex[:8]


def git(root, *args):
    try:
        r = subprocess.run(['git', '-C', str(root), *args], capture_output=True, timeout=10)
        return r.stdout if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def bundle(source=SOURCE):
    names = ['VERSION', 'README.md', 'ADOPT.md', 'WORKFLOW.md', 'feedback/README.md']
    for directory in ('scripts', 'templates', 'tools'):
        names.extend(str(p.relative_to(source)) for p in (source / directory).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    names.extend(str(p.relative_to(source)) for p in (source / 'docs').glob('*.md'))
    return {name: (source / name).read_bytes() for name in sorted(set(names))}


def config_check(config):
    if config.get('schema_version') != 1:
        raise ValueError('Unsupported config schema_version')
    if not isinstance(config.get('project_name'), str) or not config['project_name'].strip():
        raise ValueError('project_name must be nonempty')
    paths = config.get('paths', {})
    required = ('spine', 'workflow', 'gate', 'context')
    if any(not isinstance(paths.get(k), str) for k in required):
        raise ValueError('Missing project path mappings')
    locations = [paths[k] for k in required] + ['AGENTS.md', 'CLAUDE.md']
    if len(set(locations)) != len(locations):
        raise ValueError('Project file mappings must be distinct')
    for location in locations:
        if location.startswith(('.spine/', '.git/')) or location in ('.spine', '.git'):
            raise ValueError('Project paths cannot use reserved directories')
    task = config.get('task_source', {})
    if task.get('kind') not in ('local', 'external') or not isinstance(task.get('location'), str) or not task['location'].strip():
        raise ValueError('task_source requires local/external and nonempty location')
    if not isinstance(config.get('tools'), dict):
        raise ValueError('tools selection is required')
    checks = config.get('checks')
    if not isinstance(checks, list) or not checks:
        raise ValueError('Configure at least one check, or an explicit justified skip')
    names = []
    for check in checks:
        if not isinstance(check, dict) or not isinstance(check.get('name'), str) or not check['name'].strip():
            raise ValueError('Each check needs a name')
        names.append(check['name'])
        if ('argv' in check) == ('skip_reason' in check):
            raise ValueError('Each check needs exactly one of argv / skip_reason')
        if 'argv' in check and (not isinstance(check['argv'], list) or not check['argv'] or
                               any(not isinstance(x, str) or not x for x in check['argv'])):
            raise ValueError('argv must be a nonempty string array')
        if 'skip_reason' in check and (not isinstance(check['skip_reason'], str) or not check['skip_reason'].strip()):
            raise ValueError('skip_reason must explain the omission')
        timeout = check.get('timeout_seconds', 120)
        if type(timeout) is not int or not 1 <= timeout <= 3600:
            raise ValueError('timeout_seconds must be an integer in 1..3600')
    if len(names) != len(set(names)):
        raise ValueError('Check names must be unique')


def validate_paths(root, config):
    for value in config['paths'].values():
        safe(root, value)
    task = config['task_source']
    if task['kind'] == 'local':
        if task['location'].split('/')[0] in ('.spine', '.git'):
            raise ValueError('Task source cannot use reserved directories')
        safe(root, task['location'])


def load_config(root, config_path=None):
    if config_path:
        config = read_json(Path(config_path))
    elif safe(root, '.spine/config.json').exists():
        config = read_json(safe(root, '.spine/config.json'))
    else:
        config = read_json(SOURCE / 'templates/config.json')
    config_check(config)
    validate_paths(root, config)
    return config


def desired(config, data):
    result = {'.spine/vendor/' + name: content for name, content in data.items()}
    mapping = {'AGENTS.md': 'AGENTS.md', 'CLAUDE.md': 'CLAUDE.md',
               config['paths']['spine']: 'PRODUCT_SPINE.md',
               config['paths']['workflow']: 'WORKFLOW.md',
               config['paths']['gate']: 'gate.md', config['paths']['context']: 'context.md'}
    for destination, template in mapping.items():
        result[destination] = data['templates/project/' + template]
    if config['task_source']['kind'] == 'local':
        result[config['task_source']['location'] + '/.gitkeep'] = b''
    result['.spine/config.json'] = encoded(config)
    result['.spine/setup/report.json'] = encoded({
        'actor': '', 'items': {k: {'status': 'pending', 'evidence': ''} for k in REPORT_ITEMS},
        'limitations': [], 'tool_inventory': []})
    return result


def source_info(source, data):
    hashes = {p: digest(content) for p, content in data.items()}
    commit = git(source, 'rev-parse', 'HEAD')
    status = git(source, 'status', '--porcelain')
    return {'repository': 'https://github.com/ganksolo/spine-kit',
            'version': data['VERSION'].decode().strip(),
            'commit': commit.decode().strip() if commit else None,
            'dirty': bool(status) if status is not None else None,
            'bundle_sha256': digest(encoded(hashes)), 'vendor_hashes': hashes}


def apply(root, config, source=SOURCE, preview=False):
    data = bundle(source)
    info = source_info(source, data)
    manifest_path = safe(root, '.spine/manifest.json')
    old = read_json(manifest_path) if manifest_path.exists() else None
    if old and old['source']['bundle_sha256'] != info['bundle_sha256']:
        raise ValueError('Different bundle: use the documented upgrade procedure; apply will not overwrite')
    files = desired(config, data)
    actions = []
    for relative, content in files.items():
        path = safe(root, relative)
        if path.exists() and not path.is_file():
            raise ValueError(f'Expected file, found directory: {relative}')
        action = 'create' if not path.exists() else ('identical' if path.read_bytes() == content else 'preserve')
        if action == 'preserve' and relative.startswith('.spine/vendor/'):
            raise ValueError(f'Vendor drift: {relative}; inspect before resuming')
        actions.append({'path': relative, 'action': action, 'sha256': digest(content)})
    if preview:
        return {'mode': 'plan', 'source': info, 'actions': actions, 'writes': False}
    rid = run_id()
    event(root, rid, 'apply-start', version=info['version'], bundle=info['bundle_sha256'])
    try:
        for item in actions:
            relative = item['path']
            event(root, rid, 'file-planned', **item)
            if item['action'] == 'create':
                path = safe(root, relative)
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('xb') as stream:
                    stream.write(files[relative])
                    stream.flush()
                    os.fsync(stream.fileno())
            event(root, rid, 'file-result', **item)
        if config['task_source']['kind'] == 'local':
            safe(root, config['task_source']['location']).mkdir(parents=True, exist_ok=True)
        state = {'schema_version': 1, 'source': info, 'status': 'needs-adaptation',
                 'created_at': old.get('created_at', now()) if old else now(),
                 'updated_at': now(), 'last_apply_run': rid}
        atomic_json(root, '.spine/manifest.json', state)
        event(root, rid, 'apply-finished', status='needs-adaptation')
        return {'status': 'needs-adaptation', 'run_id': rid,
                'preserved': [x['path'] for x in actions if x['action'] == 'preserve']}
    except BaseException as exc:
        event(root, rid, 'apply-failed', error_type=type(exc).__name__)
        raise


def placeholder(text):
    return bool(re.search(r'\bTODO\b|\bFIXME\b|\{\{[^}]+\}\}', text))


def validate(root):
    errors = []
    try:
        manifest = read_json(safe(root, '.spine/manifest.json'))
        if manifest.get('schema_version') != 1:
            raise ValueError('Unsupported manifest schema_version')
        config = load_config(root)
        if placeholder(json.dumps(config, ensure_ascii=False)):
            errors.append('Unresolved TODO/FIXME/template markers in config')
        for key, relative in config['paths'].items():
            path = safe(root, relative)
            if not path.is_file() or not path.read_text().strip():
                errors.append(f'Missing/empty project document: {relative}')
            elif placeholder(path.read_text()):
                errors.append(f'Unresolved project placeholders: {relative}')
        for entry in ('AGENTS.md', 'CLAUDE.md'):
            path = safe(root, entry)
            if not path.is_file() or '.spine/config.json' not in path.read_text():
                errors.append(f'{entry} needs an explicit .spine/config.json entry point')
        task = config['task_source']
        if task['kind'] == 'local' and not safe(root, task['location']).is_dir():
            errors.append('Local task source directory is missing')
        expected = manifest['source']['vendor_hashes']
        if not expected or digest(encoded(expected)) != manifest['source']['bundle_sha256']:
            errors.append('Invalid bundle manifest hash')
        for name, expected_hash in expected.items():
            path = safe(root, '.spine/vendor/' + name)
            if not path.is_file() or digest(path.read_bytes()) != expected_hash:
                errors.append(f'Vendor hash mismatch: {name}')
        vendor = safe(root, '.spine/vendor')
        actual = {str(p.relative_to(vendor)) for p in vendor.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
        if actual != set(expected):
            errors.append('Vendor file set differs from manifest')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(str(exc))
    return errors


def fingerprint(root):
    head = git(root, 'rev-parse', 'HEAD') or b'unborn-or-no-git'
    listing = git(root, 'ls-files', '-z', '--cached', '--others', '--exclude-standard')
    if listing is not None:
        names = sorted(set(os.fsdecode(x) for x in listing.split(b'\0') if x))
    else:
        ignored = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', '.cache'}
        names = []
        for directory, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in ignored and not (Path(directory) / d).is_symlink())
            names.extend(str((Path(directory) / f).relative_to(root)) for f in files)
        names.sort()
    hasher = hashlib.sha256(head)
    for name in names:
        if name.startswith('.spine/setup/') or name == '.spine/manifest.json' or '__pycache__' in Path(name).parts or name.endswith('.pyc'):
            continue
        p = root / name
        hasher.update(os.fsencode(name) + b'\0')
        # Symlinks are hashed as links, never read outside the repository.
        if p.is_symlink():
            hasher.update(os.fsencode(os.readlink(p)))
        elif p.is_file():
            hasher.update(p.read_bytes())
        else:
            hasher.update(b'<missing>')
    return hasher.hexdigest()


def finalize(root):
    errors = validate(root)
    if errors:
        raise ValueError('; '.join(errors))
    report = read_json(safe(root, '.spine/setup/report.json'))
    if not isinstance(report.get('actor'), str) or not report['actor'].strip():
        raise ValueError('Report requires an actor identity')
    for key in REPORT_ITEMS:
        item = report.get('items', {}).get(key, {})
        evidence = item.get('evidence')
        if item.get('status') != 'passed' or not isinstance(evidence, str) or not evidence.strip() or placeholder(evidence):
            raise ValueError(f'Report not ready: {key}')
    verification = read_json(safe(root, '.spine/setup/verification.json'))
    current_config = digest(safe(root, '.spine/config.json').read_bytes())
    if (verification.get('status') != 'passed' or verification.get('config_sha256') != current_config or
            verification.get('fingerprint') != fingerprint(root)):
        raise ValueError('Verification failed, missing or stale; run verify.py again')
    manifest = read_json(safe(root, '.spine/manifest.json'))
    manifest.update(status='complete', completed_at=now(), updated_at=now(),
                    verified_fingerprint=verification['fingerprint'],
                    report_sha256=digest(safe(root, '.spine/setup/report.json').read_bytes()))
    atomic_json(root, '.spine/manifest.json', manifest)
    rid = run_id()
    event(root, rid, 'setup-complete', actor=report['actor'],
          verification_run=verification['run_id'], report_sha256=manifest['report_sha256'])
    return {'status': 'complete', 'run_id': rid, 'limitations': report.get('limitations', []),
            'skipped_checks': [x for x in verification['checks'] if x['status'] == 'skipped']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'apply', 'validate', 'finalize'])
    parser.add_argument('--target', required=True)
    parser.add_argument('--config', help='plan/apply only; project adapter JSON')
    args = parser.parse_args()
    try:
        root = Path(args.target).resolve()
        if not root.is_dir():
            raise ValueError('Target must be an existing project directory')
        if args.config and args.command not in ('plan', 'apply'):
            raise ValueError('--config is only supported for plan/apply')
        if args.command in ('plan', 'apply'):
            result = apply(root, load_config(root, args.config), preview=args.command == 'plan')
        elif args.command == 'validate':
            errors = validate(root)
            result = {'status': 'failed' if errors else 'passed', 'errors': errors}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if errors else 0
        else:
            result = finalize(root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'spine-kit: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
