import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import setup
import verify


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='spine-kit-test-')
        self.root = Path(self.temp.name)
        self.config = setup.read_json(ROOT / 'templates/config.json')
        self.config['project_name'] = 'fixture-project'
        self.config['checks'] = [{'name': 'unit', 'argv': [sys.executable, '-c', 'assert 2 + 2 == 4']}]

    def tearDown(self):
        self.temp.cleanup()

    def install(self):
        return setup.apply(self.root, self.config, ROOT)

    def adapt(self):
        self.install()
        for relative in self.config['paths'].values():
            p = self.root / relative
            p.write_text(p.read_text().replace('TODO', 'fixture-specific decision'))
        report = setup.read_json(self.root / '.spine/setup/report.json')
        report['actor'] = 'fixture-agent'
        for item in report['items'].values():
            item.update(status='passed', evidence='fixture review of explicit mapped files')
        setup.atomic_json(self.root, '.spine/setup/report.json', report)

    def test_plan_is_read_only(self):
        result = setup.apply(self.root, self.config, ROOT, preview=True)
        self.assertFalse(result['writes'])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_apply_never_claims_complete_and_logs_details(self):
        result = self.install()
        self.assertEqual(result['status'], 'needs-adaptation')
        records = [json.loads(line) for line in (self.root / f".spine/setup/{result['run_id']}.jsonl").read_text().splitlines()]
        self.assertEqual(records[0]['event'], 'apply-start')
        self.assertEqual(records[-1]['event'], 'apply-finished')
        self.assertTrue(any(r['event'] == 'file-result' and 'sha256' in r for r in records))
        self.assertTrue(setup.validate(self.root))

    def test_existing_files_preserved_and_repeatable(self):
        existing = self.root / 'AGENTS.md'
        existing.write_text('existing instruction with local customization')
        result = self.install()
        self.assertIn('AGENTS.md', result['preserved'])
        self.assertEqual(existing.read_text(), 'existing instruction with local customization')
        p = self.root / self.config['paths']['context']
        p.write_text('user changes after partial setup')
        again = self.install()
        self.assertEqual(p.read_text(), 'user changes after partial setup')
        self.assertNotEqual(result['run_id'], again['run_id'])
        self.assertEqual(len(list((self.root / '.spine/setup').glob('*.jsonl'))), 2)

    def test_complete_requires_adaptation_report_and_verification(self):
        self.install()
        with self.assertRaises(ValueError):
            setup.finalize(self.root)
        self.adapt()
        self.assertEqual(setup.validate(self.root), [])
        with self.assertRaises(FileNotFoundError):
            setup.finalize(self.root)
        result = verify.verify(self.root)
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(setup.finalize(self.root)['status'], 'complete')

    def test_failed_check_blocks_completion(self):
        self.config['checks'] = [{'name': 'fail', 'argv': [sys.executable, '-c', 'raise SystemExit(2)']}]
        self.adapt()
        self.assertEqual(verify.verify(self.root)['status'], 'failed')
        with self.assertRaises(ValueError):
            setup.finalize(self.root)

    def test_skip_is_explicit_and_visible(self):
        self.config['checks'] = [{'name': 'tests', 'skip_reason': 'No application code exists in this new project'}]
        self.adapt()
        self.assertEqual(verify.verify(self.root)['checks'][0]['status'], 'skipped')
        self.assertEqual(len(setup.finalize(self.root)['skipped_checks']), 1)

    def test_stale_evidence_blocks_completion(self):
        self.adapt()
        verify.verify(self.root)
        (self.root / 'new-code.py').write_text('print(1)')
        with self.assertRaisesRegex(ValueError, 'stale'):
            setup.finalize(self.root)

    def test_check_mutations_are_not_green(self):
        self.config['checks'] = [{'name': 'mutator', 'argv': [sys.executable, '-c', "from pathlib import Path; Path('changed').write_text('x')"]}]
        self.adapt()
        result = verify.verify(self.root)
        self.assertTrue(result['workspace_changed'])
        self.assertEqual(result['status'], 'failed')

    def test_timeout_and_missing_binary_record_failure(self):
        self.config['checks'] = [
            {'name': 'timeout', 'argv': [sys.executable, '-c', 'import time; time.sleep(10)'], 'timeout_seconds': 1},
            {'name': 'missing', 'argv': ['this-binary-does-not-exist-spine-kit']}]
        self.adapt()
        result = verify.verify(self.root)
        self.assertTrue(result['checks'][0]['timed_out'])
        self.assertEqual(result['checks'][1]['error_type'], 'FileNotFoundError')

    def test_path_traversal_and_symlink_are_rejected(self):
        with self.assertRaises(ValueError):
            setup.safe(self.root, '../outside')
        with self.assertRaises(ValueError):
            setup.safe(self.root, '/tmp/outside')
        (self.root / '.spine').symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.install()

    def test_vendor_tamper_detected(self):
        self.adapt()
        (self.root / '.spine/vendor/WORKFLOW.md').write_text('tampered')
        self.assertTrue(any('hash mismatch' in e for e in setup.validate(self.root)))
        with self.assertRaisesRegex(ValueError, 'Vendor drift'):
            self.install()

    def test_external_task_adapter_does_not_create_local_task_store(self):
        self.config['task_source'] = {'kind': 'external', 'location': 'https://example.org/issues'}
        self.adapt()
        self.assertFalse((self.root / 'docs/workflow/tasks').exists())
        self.assertEqual(setup.validate(self.root), [])

    def test_existing_trellis_adapter_is_reused(self):
        self.config['task_source'] = {'kind': 'local', 'location': '.trellis/tasks'}
        p = self.root / '.trellis/tasks/0001.md'
        p.parent.mkdir(parents=True)
        p.write_text('existing task')
        self.adapt()
        self.assertEqual(p.read_text(), 'existing task')
        self.assertFalse((self.root / 'docs/workflow/tasks').exists())

    def test_different_bundle_cannot_silently_upgrade(self):
        self.install()
        with patch.object(setup, 'bundle', return_value={**setup.bundle(ROOT), 'VERSION': b'0.2.0\n'}):
            with self.assertRaisesRegex(ValueError, 'Different bundle'):
                self.install()

    def test_interrupted_apply_is_logged_and_resumable(self):
        original = setup.atomic_json
        with patch.object(setup, 'atomic_json', side_effect=OSError('simulated interruption')):
            with self.assertRaises(OSError):
                self.install()
        logs = list((self.root / '.spine/setup').glob('*.jsonl'))
        self.assertIn('apply-failed', logs[0].read_text())
        self.install()
        self.assertTrue((self.root / '.spine/manifest.json').exists())

    def test_git_fingerprint_tracks_worktree_but_ignores_setup_logs(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.adapt()
        before = setup.fingerprint(self.root)
        setup.event(self.root, setup.run_id(), 'test')
        self.assertEqual(before, setup.fingerprint(self.root))
        (self.root / 'a.txt').write_text('changed')
        self.assertNotEqual(before, setup.fingerprint(self.root))

    def test_config_rejects_ambiguous_and_duplicate_checks(self):
        c = copy.deepcopy(self.config)
        c['checks'][0]['skip_reason'] = 'because'
        with self.assertRaises(ValueError):
            setup.config_check(c)
        c = copy.deepcopy(self.config)
        c['checks'] *= 2
        with self.assertRaises(ValueError):
            setup.config_check(c)

    def test_vendored_cli_runs_from_project(self):
        self.adapt()
        result = subprocess.run([sys.executable, str(self.root / '.spine/vendor/scripts/setup.py'),
                                 'validate', '--target', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


class DocumentationTests(unittest.TestCase):
    def test_local_markdown_links_resolve(self):
        for path in ROOT.rglob('*.md'):
            if 'templates' in path.parts:
                continue  # project-relative templates are verified after application
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if target.startswith(('https:', 'http:', '#', 'mailto:')):
                    continue
                target = target.split('#')[0]
                self.assertTrue((path.parent / target).exists(), f'{path}: {target}')


if __name__ == '__main__':
    unittest.main()
