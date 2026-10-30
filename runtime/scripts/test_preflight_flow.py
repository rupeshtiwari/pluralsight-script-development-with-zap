"""Exercise real preflight orchestration with controlled runtime boundaries.

These regressions test working directories, runtime startup, output streaming,
reference cleanup and failure propagation; they are not live ZAP scan evidence.
"""
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parent
FOLDERS = {
 'm1-demo1': 'demos/module1-demos/m1-demo1-targeted-injection-xss-csrf',
 'm1-demo2': 'demos/module1-demos/m1-demo2-javascript-http-sender',
 'm1-demo3': 'demos/module1-demos/m1-demo3-python-scanning-authentication',
 'm2-demo1': 'demos/module2-demos/m2-demo1-authenticated-zap-github-actions',
 'm2-demo2': 'demos/module2-demos/m2-demo2-zap-api-scan-evidence',
 'm2-demo3': 'demos/module2-demos/m2-demo3-security-quality-gates',
}
ARTIFACTS = {
 'marker': ('m1-demo2','zap-scripts/globomantics-marker.js'),
 'rule': ('m1-demo3','zap-scripts/globomantics-active-rule.py'),
 'auth': ('m1-demo3','zap-scripts/globomantics-auth.py'),
 'plan': ('m2-demo1','ci/af-plan.yaml'),
 'gate': ('m2-demo3','ci/gate-plan.yaml'),
}
NEEDS = {'m1-demo1':(), 'm1-demo2':('marker',), 'm1-demo3':('rule','auth'),
         'm2-demo1':('marker','rule','auth','plan'), 'm2-demo2':('marker','rule','auth','plan'),
         'm2-demo3':('gate',)}

class PreflightFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # macOS may spell its temp parent /var while child cwd reports /private/var.
        # Canonicalize the fixture identity; retain strict working-directory assertions.
        temp_root = Path(self.temp.name).resolve()
        # Include spaces in the checkout path as on many real recording Macs.
        self.root = temp_root / 'course checkout'
        self.root.mkdir()
        self.bin = temp_root / 'bin'
        self.bin.mkdir()
        scripts = self.root / 'runtime/scripts'
        scripts.mkdir(parents=True)
        for name in ('preflight_course.sh', 'preflight_all_steps.sh', 'recording_step.py',
                     'preflight_runtime.sh', 'preflight_start.py', 'lib.sh', 'capture_ci_source.py', 'preflight_workspace.py'):
            shutil.copy2(SOURCE / name, scripts / name)
        shutil.copy2(SOURCE.parents[1] / 'preflight-check', self.root / 'preflight-check')
        self.write_exec(self.bin / 'docker', '''#!/usr/bin/env python3
import os,sys
from pathlib import Path
root=Path(os.environ['TEST_ROOT'])
a=sys.argv[1:]
ready=(root/'ready').exists()
if a==['info']:
 if (root/'ready-pause').exists():
  import time; time.sleep(60)
 sys.exit(0)
if a[:2]==['compose','up']:
 (root/'selected-build').write_text(os.environ.get('APP_BUILD',''))
 (root/'ready').touch(); sys.exit(0)
if a[:3]==['compose','ps','-q']:
 print(a[3] if ready else ''); sys.exit(0)
if a and a[0]=='inspect': print('healthy' if ready else 'starting'); sys.exit(0)
sys.exit(1)
''')
        self.write_exec(self.bin / 'curl', '''#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
root=Path(os.environ['TEST_ROOT'])
if not (root/'ready').exists(): sys.exit(7)
if 'health' in sys.argv[-1]:
 print(json.dumps({'vulnerable':not (root/'remediated').exists(),'postgres':'ok','mongo':'ok'}))
else: print(json.dumps({'version':'2.17.0'}))
''')
        self.write_exec(scripts / 'lab-up.sh', '''#!/usr/bin/env python3
import os,sys,time
from pathlib import Path
root=Path(os.environ['TEST_ROOT'])
assert Path.cwd()==root, 'startup must run from repo root'
with (root/'start-count').open('a') as f:f.write('start\\n')
print('STARTUP: controlled test startup',flush=True)
if (root/'startup-fail').exists(): print('STARTUP ERROR: engine unavailable',flush=True); sys.exit(9)
if (root/'startup-pause').exists():
 (root/'startup-active').touch(); time.sleep(60)
(root/'remediated').unlink(missing_ok=True)
(root/'ready').touch()
''')
        self.write_exec(scripts / 'preflight_diagnose.sh', '#!/bin/bash\necho "DIAGNOSTICS: controlled runtime boundary"\necho "DIAGNOSTICS: controlled runtime boundary" > "$TEST_ROOT/preflight-diagnostics.txt"\n')
        (self.root / '.env').write_text('ZAP_API_KEY=test-only\n')
        self.env = dict(os.environ, PATH=str(self.bin)+os.pathsep+os.environ['PATH'], TEST_ROOT=str(self.root))
        self.git('init','-q')
        self.git('config','user.name','Test')
        self.git('config','user.email','test@example.invalid')
        for demo, folder in FOLDERS.items():
            steps = self.root / folder / 'steps'
            steps.mkdir(parents=True)
            required = [FOLDERS[ARTIFACTS[key][0]]+'/'+ARTIFACTS[key][1] for key in NEEDS[demo]]
            for n in range(1,5):
                self.write_exec(steps / f'0{n}-test-step.sh', '''#!/usr/bin/env python3
import os,sys,time
from pathlib import Path
root=Path(os.environ['TEST_ROOT'])
'''+f'''expected=root/{folder!r}
assert Path.cwd()==expected, 'WRONG WORKING DIRECTORY: '+str(Path.cwd())
for relative in {required!r}:
 assert (root/relative).is_file(), 'MISSING REFERENCE: '+relative
with (root/'executions').open('a') as f:f.write({demo!r}+':{n}:'+str(Path.cwd())+'\\n')
print('STEP LIVE: {demo} {n}',flush=True)
if (root/'pause').exists(): (root/'step-active').touch(); time.sleep(60)
if (root/'step-fail').exists() and {n}==2 and os.environ.get('FAIL_DEMO', {demo!r})=={demo!r}:
 print('✘ FAIL: deliberate test failure',flush=True);sys.exit(7)
print('✔ PASS: cwd and prerequisites verified',flush=True)
''')
        for owner, name in ARTIFACTS.values():
            p=self.root/FOLDERS[owner]/name
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text('reference fixture\n')
        self.git('add','.')
        self.git('commit','-qm','references')
        for demo in FOLDERS:
            self.git('update-ref',f'refs/remotes/origin/{demo}-after','HEAD')
        for owner,name in ARTIFACTS.values():
            (self.root/FOLDERS[owner]/name).unlink()
        self.git('add','-A')
        self.git('commit','-qm','starter')
        self.head=self.git('rev-parse','HEAD')
        self.index=(self.root/'.git/index').read_bytes()

    def write_exec(self,path,data):
        path.write_text(data)
        path.chmod(0o755)

    def git(self,*args):
        return subprocess.check_output(['git','-C',str(self.root),*args],text=True).strip()

    def run_scope(self,option='',cwd=None):
        self.export = Path(tempfile.mkdtemp(dir=self.temp.name)) / 'evidence'
        self.env['PREFLIGHT_EVIDENCE_DIR'] = str(self.export)
        return subprocess.run([str(self.root/'preflight-check')]+([option] if option else []),
                              cwd=cwd or self.root,env=self.env,capture_output=True,text=True,timeout=20)

    def assert_restored(self,keep=()):
        for owner,name in ARTIFACTS.values():
            path=self.root/FOLDERS[owner]/name
            if path not in keep:self.assertFalse(path.exists(),path)
        self.assertEqual(self.git('rev-parse','HEAD'),self.head)
        self.assertEqual((self.root/'.git/index').read_bytes(),self.index)
        self.assertFalse((self.root/'.preflight-reference.lock').exists())
        self.assertFalse(list(self.root.glob('.preflight-output.*')))
        self.assertFalse((self.root/'.preflight-workspace').exists())
        self.assertFalse(list(self.root.rglob('*.pyc')))

    def cleanup_retained(self):
        self.assertTrue((self.root/'.preflight-workspace/manifest.json').is_file())
        result=self.run_scope('--cleanup', cwd=self.root/FOLDERS['m2-demo2'])
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assert_restored()

    def test_symlinked_temp_parent_keeps_strict_working_directory_checks(self):
        # Reproduce macOS /var -> /private/var using a real alias on Linux too.
        with tempfile.TemporaryDirectory() as parent:
            physical = Path(parent) / 'physical'
            physical.mkdir()
            alias = Path(parent) / 'alias'
            alias.symlink_to(physical, target_is_directory=True)
            fixture = PreflightFlowTests('test_healthy_lab_is_reused_without_starting')
            try:
                with patch.object(tempfile, 'tempdir', str(alias)):
                    fixture.setUp()
                aliased_checkout = Path(fixture.temp.name) / 'course checkout'
                self.assertNotEqual(aliased_checkout, aliased_checkout.resolve())
                result = fixture.run_scope('--m2d1', cwd=aliased_checkout)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(fixture.root, aliased_checkout.resolve())
                rows = (fixture.root / 'executions').read_text().splitlines()
                expected = fixture.root / FOLDERS['m2-demo1']
                self.assertEqual(rows, [f'm2-demo1:{n}:{expected}' for n in range(1, 5)])
                fixture.assert_restored()
            finally:
                fixture.doCleanups()

    def test_each_demo_runs_four_steps_in_its_own_directory_from_anywhere(self):
        for demo,folder in FOLDERS.items():
            with self.subTest(demo=demo):
                option='--'+demo.replace('-demo','d')
                result=self.run_scope(option,cwd=self.root/FOLDERS['m2-demo2'])
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertIn('1 passed, 0 failed',result.stdout)
                for n in range(1, 5):
                    logs = self.export / folder / 'logs'
                    self.assertEqual((logs / f'preflight-step-{n:02d}.exit').read_text(), '0\n')
                    expected = (f'STEP LIVE: {demo} {n}\n'
                                '✔ PASS: cwd and prerequisites verified\n').encode()
                    self.assertEqual((logs / f'preflight-step-{n:02d}.log').read_bytes(), expected)
                    self.assertEqual((logs / '.producer' / f'preflight-step-{n:02d}.raw.log').read_bytes(), expected)
                self.assert_restored()
        rows=(self.root/'executions').read_text().splitlines()
        self.assertEqual(len(rows),24)
        for demo,folder in FOLDERS.items():
            self.assertEqual([r for r in rows if r.startswith(demo+':')],
                             [f'{demo}:{n}:{self.root/folder}' for n in range(1,5)])
        self.assertEqual((self.root/'start-count').read_text().splitlines(),['start'])

    def test_entire_course_and_modules_from_root(self):
        for option,count in [('',6),('--m1',3),('--m2',3)]:
            result=self.run_scope(option)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertIn(f'{count} passed, 0 failed',result.stdout)
            self.assert_restored()

    def test_healthy_lab_is_reused_without_starting(self):
        (self.root/'ready').touch()
        result=self.run_scope('--m2d1')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('reusing',result.stdout)
        self.assertFalse((self.root/'start-count').exists())

    def test_actual_lab_up_honors_caller_build_override_over_dotenv(self):
        shutil.copy2(SOURCE/'lab-up.sh',self.root/'runtime/scripts/lab-up.sh')
        with (self.root/'.env').open('a') as config:config.write('APP_BUILD=remediated\n')
        result=self.run_scope('--m2d1')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual((self.root/'selected-build').read_text(),'vulnerable')
        self.assert_restored()

    def test_remediated_lab_is_restarted_for_vulnerable_exercises(self):
        (self.root/'ready').touch();(self.root/'remediated').touch()
        result=self.run_scope('--m2d1')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue((self.root/'start-count').exists())

    def test_setup_failure_shows_error_once_and_executes_no_demos(self):
        (self.root/'startup-fail').touch()
        result=self.run_scope()
        self.assertNotEqual(result.returncode,0)
        self.assertIn('STARTUP ERROR: engine unavailable',result.stdout)
        self.assertIn('no demo steps executed',result.stdout)
        self.assertFalse((self.root/'executions').exists())
        self.assertEqual([p.name for p in self.root.glob('FAIL-*.log')],['FAIL-setup.log'])
        self.cleanup_retained()

    def test_real_step_failure_keeps_sources_and_logs_until_manual_cleanup(self):
        (self.root/'step-fail').touch()
        result=self.run_scope('--m2d1')
        self.assertEqual(result.returncode,1)
        self.assertIn('✘ FAIL: deliberate test failure',result.stdout)
        self.assertIn('Step 2 failed',result.stdout)
        self.assertIn('0 passed, 1 failed',result.stdout)
        self.assertNotIn('Broken pipe',result.stderr)
        logs = self.root / FOLDERS['m2-demo1'] / 'logs'
        self.assertEqual((logs / 'preflight-step-01.exit').read_text(), '0\n')
        self.assertEqual((logs / 'preflight-step-02.exit').read_text(), '7\n')
        self.assertIn('✘ FAIL', (logs / 'preflight-step-02.log').read_text())
        self.assertFalse((logs / 'preflight-step-03.exit').exists())
        self.assertFalse((logs / 'preflight-step-04.log').exists())
        for label in NEEDS['m2-demo1']:
            owner,name=ARTIFACTS[label]
            self.assertTrue((self.root/FOLDERS[owner]/name).exists())
        self.assertIn('--cleanup',result.stdout)
        self.cleanup_retained()

    def test_ci_source_describes_actual_temporary_prerequisites_and_preserves_index(self):
        import hashlib
        after = self.git('rev-parse', 'refs/remotes/origin/m2-demo1-after')
        workflow_sha = self.head
        # Mirror CI's distinct local authored commit before the runner supplies reused files.
        authored = self.root / FOLDERS['m2-demo1'] / 'ci/af-plan.yaml'
        authored.write_text('reference fixture\n')
        self.git('add', str(authored))
        self.git('commit', '-qm', 'local authored plan')
        self.head = self.git('rev-parse', 'HEAD')
        self.index = (self.root / '.git/index').read_bytes()
        (self.root / 'SOURCE.txt').write_text(workflow_sha + '\n')
        (self.root / 'AFTER_SHA.txt').write_text(after + '\n')
        self.env.update(PREFLIGHT_CI_SOURCE='1', GITHUB_SHA=workflow_sha)
        result = self.run_scope('--m2d1')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        manifest = json.loads((self.export / 'EXECUTION.json').read_text())
        self.assertEqual(manifest['workflow_sha'], workflow_sha)
        self.assertNotEqual(manifest['workflow_sha'], manifest['executed_head'])
        self.assertEqual(manifest['executed_head'], self.head)
        self.assertEqual(manifest['after_sha'], after)
        self.assertEqual((self.export / 'EXECUTED_TREE.txt').read_text().strip(), manifest['executed_tree'])
        self.assertEqual((self.export / 'EXECUTED_HEAD.txt').read_text().strip(), manifest['executed_head'])
        self.assertEqual(manifest['authored_patch_sha256'],
                         hashlib.sha256((self.export / 'AUTHORED.patch').read_bytes()).hexdigest())
        self.assertNotEqual(manifest['executed_tree'], self.git('rev-parse', 'HEAD^{tree}'))
        for key in NEEDS['m2-demo1']:
            owner, name = ARTIFACTS[key]
            relative = FOLDERS[owner] + '/' + name
            captured = subprocess.check_output(['git', '-C', str(self.root), 'show',
                                                manifest['executed_tree'] + ':' + relative])
            self.assertEqual(manifest['source_hashes'][relative], hashlib.sha256(captured).hexdigest())
        self.assertFalse(any('/logs/' in path for path in manifest['source_hashes']))
        # Reconstruct the executed tree from the immutable workflow base and captured patch.
        with tempfile.TemporaryDirectory() as temporary:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(temporary) / 'index'))
            for args in (['read-tree', workflow_sha],
                         ['apply', '--cached', '--binary', str(self.export / 'AUTHORED.patch')]):
                subprocess.run(['git', '-C', str(self.root), *args], env=env, check=True,
                               capture_output=True)
            rebuilt = subprocess.check_output(['git', '-C', str(self.root), 'write-tree'],
                                              env=env, text=True).strip()
        self.assertEqual(rebuilt, manifest['executed_tree'])
        self.assert_restored([authored])

    def test_second_failure_clears_stale_unexecuted_step_evidence(self):
        self.assertEqual(self.run_scope('--m2d1').returncode, 0)
        (self.root / 'step-fail').touch()
        result = self.run_scope('--m2d1')
        self.assertEqual(result.returncode, 1)
        logs = self.root / FOLDERS['m2-demo1'] / 'logs'
        self.assertEqual((logs / 'preflight-step-02.exit').read_text(), '7\n')
        for n in (3, 4):
            self.assertFalse((logs / f'preflight-step-{n:02d}.exit').exists())
            self.assertFalse((logs / f'preflight-step-{n:02d}.log').exists())
        self.cleanup_retained()

    def test_timed_out_step_records_actual_killed_exit_and_no_unexecuted_exits(self):
        (self.root / 'pause').touch()
        self.env['PREFLIGHT_STEP_TIMEOUT'] = '0.2'
        result = self.run_scope('--m2d1')
        self.assertEqual(result.returncode, 1)
        logs = self.root / FOLDERS['m2-demo1'] / 'logs'
        self.assertEqual((logs / 'preflight-step-01.exit').read_text(), '-15\n')
        self.assertIn('STEP LIVE', (logs / 'preflight-step-01.log').read_text())
        self.assertFalse((logs / 'preflight-step-02.exit').exists())
        self.cleanup_retained()

    def test_existing_modified_reference_is_preserved(self):
        path=self.root/FOLDERS['m1-demo3']/'zap-scripts/globomantics-auth.py'
        path.write_text('learner work\n')
        result=self.run_scope('--m2d1')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(path.read_text(),'learner work\n')
        self.assert_restored([path])

    def test_invalid_scope_never_starts_lab(self):
        result=self.run_scope('--m2d9')
        self.assertEqual(result.returncode,2)
        self.assertFalse((self.root/'start-count').exists())

    def test_live_output_and_cancel_cleanup(self):
        (self.root/'pause').touch()
        with tempfile.TemporaryFile() as log:
            child=subprocess.Popen([str(self.root/'preflight-check'),'--m2d1'],cwd=self.root,
                                   env=self.env,stdout=log,stderr=log)
            try:
                deadline=time.monotonic()+10
                while time.monotonic()<deadline:
                    log.seek(0);data=log.read().decode()
                    if 'STEP LIVE: m2-demo1 1' in data:break
                    if child.poll() is not None:break
                    time.sleep(.02)
                self.assertIn('STEP LIVE: m2-demo1 1',data)
                self.assertIsNone(child.poll(),'progress must appear before the command finishes')
                self.assertIn('STEP LIVE: m2-demo1 1',(self.root/'course-evidence.txt').read_text())
                child.send_signal(signal.SIGTERM)
                self.assertEqual(child.wait(timeout=12),143)
            finally:
                if child.poll() is None:child.kill();child.wait()
        self.cleanup_retained()

    def test_hung_readiness_is_bounded_before_and_after_startup(self):
        (self.root/'ready-pause').touch()
        self.env['PREFLIGHT_READY_TIMEOUT']='0.1'
        result=self.run_scope('--m2d1')
        self.assertEqual(result.returncode,1)
        self.assertIn('readiness checks still fail',result.stdout)
        self.assertFalse((self.root/'executions').exists())
        self.cleanup_retained()

    def test_startup_timeout_is_bounded_and_leaves_no_ready_lab(self):
        (self.root/'startup-pause').touch()
        self.env['PREFLIGHT_START_TIMEOUT']='0.2'
        result=self.run_scope('--m2d1')
        self.assertEqual(result.returncode,1)
        self.assertIn('exceeded PREFLIGHT_START_TIMEOUT',result.stdout)
        self.assertFalse((self.root/'ready').exists())
        self.cleanup_retained()

    def test_cancel_startup_stops_owned_process(self):
        (self.root/'startup-pause').touch()
        with tempfile.TemporaryFile() as log:
            child=subprocess.Popen([str(self.root/'preflight-check'),'--m2d1'],cwd=self.root,
                                   env=self.env,stdout=log,stderr=log)
            try:
                deadline=time.monotonic()+10
                while not (self.root/'startup-active').exists() and time.monotonic()<deadline:
                    time.sleep(.02)
                self.assertTrue((self.root/'startup-active').exists())
                child.send_signal(signal.SIGTERM)
                self.assertEqual(child.wait(timeout=12),143)
                self.assertFalse((self.root/'ready').exists())
            finally:
                if child.poll() is None:child.kill();child.wait()
        self.cleanup_retained()

    def test_success_restores_prior_outputs_and_removes_all_new_native_artifacts(self):
        from preflight_workspace import LOG_PATTERNS
        logs=self.root/FOLDERS['m2-demo1']/'logs'
        logs.mkdir()
        gate=logs/'.gate';gate.mkdir();gate.chmod(0o750)
        old=logs/'preflight-step-01.log'
        old.write_text('my previous evidence\n');old.chmod(0o640)
        (logs/'.gitkeep').touch()
        (logs/'personal-notes.txt').write_text('keep me')
        evidence=self.root/'course-evidence.txt';evidence.write_text('previous course evidence')
        stale=self.root/'FAIL-old.log';stale.write_text('previous failure')
        step=self.root/FOLDERS['m2-demo1']/'steps/04-test-step.sh'
        with step.open('a') as script:
            script.write("\nlogs=Path.cwd()/'logs'\n(logs/'.gate').chmod(0o777)\n")
            for relative in ('alert-disposition.md','.m1demo3-state','custom-alert-record.json',
                             '.m2demo2-state','globo-api-report-test.json','.gate/run.log',
                             '.gate/gate-plan.yaml','.gate/globo-gate-report.json','.gate/exit',
                             '.producer/reference-step-01-candidate.log'):
                script.write(f"p=logs/{relative!r};p.parent.mkdir(parents=True,exist_ok=True);p.write_text('generated')\n")
        result=self.run_scope('--m2d1')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(old.read_text(),'my previous evidence\n')
        self.assertEqual(old.stat().st_mode & 0o777,0o640)
        self.assertEqual(gate.stat().st_mode & 0o777,0o750)
        self.assertFalse(list(gate.iterdir()))
        self.assertEqual(evidence.read_text(),'previous course evidence')
        self.assertEqual(stale.read_text(),'previous failure')
        self.assertEqual(sorted(p.name for p in logs.iterdir()),['.gate','.gitkeep','personal-notes.txt','preflight-step-01.log'])
        self.assert_restored()

    def test_late_course_failure_retains_earlier_demo_files_and_blocks_rerun(self):
        (self.root/'step-fail').touch();self.env['FAIL_DEMO']='m2-demo3'
        result=self.run_scope()
        self.assertEqual(result.returncode,1,result.stdout+result.stderr)
        self.assertIn('5 passed, 1 failed',result.stdout)
        for owner,name in ARTIFACTS.values():
            self.assertTrue((self.root/FOLDERS[owner]/name).is_file())
        earlier=self.root/FOLDERS['m1-demo1']/'logs/preflight-step-04.exit'
        self.assertEqual(earlier.read_text(),'0\n')
        evidence=(self.root/'course-evidence.txt').read_bytes()
        second=self.run_scope('--m2d1')
        self.assertNotEqual(second.returncode,0)
        self.assertIn('--cleanup',second.stderr)
        self.assertEqual((self.root/'course-evidence.txt').read_bytes(),evidence)
        self.cleanup_retained()
        self.assertFalse((self.root/'course-evidence.txt').exists())
        self.assertFalse(earlier.exists())

    def test_manual_cleanup_preserves_edits_without_partial_deletion(self):
        (self.root/'step-fail').touch()
        self.assertEqual(self.run_scope('--m2d1').returncode,1)
        path=self.root/FOLDERS['m1-demo2']/'zap-scripts/globomantics-marker.js'
        original=path.read_bytes();path.write_text('edited after failure')
        result=self.run_scope('--cleanup')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(path.read_text(),'edited after failure')
        self.assertTrue((self.root/'course-evidence.txt').exists())
        path.write_bytes(original)
        self.cleanup_retained()

    def test_cleanup_preserves_same_content_replacement_and_accepts_manual_deletion(self):
        (self.root/'step-fail').touch()
        self.assertEqual(self.run_scope('--m2d1').returncode,1)
        path=self.root/FOLDERS['m1-demo2']/'zap-scripts/globomantics-marker.js'
        replacement=path.with_name('replacement')
        replacement.write_bytes(path.read_bytes());replacement.replace(path)
        result=self.run_scope('--cleanup')
        self.assertNotEqual(result.returncode,0)
        self.assertTrue(path.exists())
        self.assertIn('replaced',result.stderr)
        path.unlink()  # Explicit manual deletion is also supported.
        self.cleanup_retained()

    def test_manual_cleanup_keeps_edited_report_and_unrelated_files(self):
        (self.root/'step-fail').touch()
        self.assertEqual(self.run_scope('--m2d1').returncode,1)
        output=self.root/FOLDERS['m2-demo1']/'logs/preflight-step-01.log'
        original=output.read_bytes();output.write_text('my edited log')
        note=output.parent/'personal-note.txt';note.write_text('unrelated')
        result=self.run_scope('--cleanup')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(output.read_text(),'my edited log')
        self.assertTrue((self.root/'course-evidence.txt').exists())
        output.write_bytes(original)
        self.cleanup_retained()
        self.assertEqual(note.read_text(),'unrelated')

    def test_cleanup_refuses_symlink_and_active_run(self):
        (self.root/'pause').touch()
        with tempfile.TemporaryFile() as log:
            child=subprocess.Popen([str(self.root/'preflight-check'),'--m2d1'],cwd=self.root,
                                   env=self.env,stdout=log,stderr=log)
            try:
                deadline=time.monotonic()+10
                while not (self.root/'step-active').exists() and time.monotonic()<deadline:time.sleep(.02)
                self.assertTrue((self.root/'step-active').exists())
                manifest_path=self.root/'.preflight-workspace/manifest.json'
                manifest=json.loads(manifest_path.read_text());manifest['phase']='retained'
                manifest_path.write_text(json.dumps(manifest))
                result=self.run_scope('--cleanup')
                self.assertNotEqual(result.returncode,0)
                self.assertIn('still running',result.stderr)
                child.terminate();self.assertEqual(child.wait(timeout=12),143)
            finally:
                if child.poll() is None:child.kill();child.wait()
        path=self.root/FOLDERS['m1-demo2']/'zap-scripts/globomantics-marker.js'
        original=path.with_name('preserved-original');path.rename(original)
        outside=Path(self.temp.name)/'personal-file';outside.write_text('personal')
        path.symlink_to(outside)
        result=self.run_scope('--cleanup')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(outside.read_text(),'personal')
        path.unlink();original.rename(path)
        self.cleanup_retained()

    def test_cleanup_checks_native_owner_and_recovers_only_its_dead_lock(self):
        (self.root/'step-fail').touch()
        self.assertEqual(self.run_scope('--m2d1').returncode,1)
        manifest=json.loads((self.root/'.preflight-workspace/manifest.json').read_text())
        lock=self.root/'.preflight-reference.lock';lock.mkdir()
        owner=lock/'owner'
        owner.write_text(f"pid={os.getpid()}\nworkspace_run={manifest['run_id']}\n")
        result=self.run_scope('--cleanup')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('native preflight runner is still running',result.stderr)
        owner.write_text(f"pid=999999999\nworkspace_run={manifest['run_id']}\n")
        (lock/'source-0').write_text('owned snapshot')
        self.cleanup_retained()
        self.assertFalse(lock.exists())

    def test_default_success_leaves_no_evidence_or_imported_sources(self):
        env=dict(self.env);env.pop('PREFLIGHT_EVIDENCE_DIR',None)
        result=subprocess.run([str(self.root/'preflight-check'),'--m2d1'],cwd=self.root,
                              env=env,capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertFalse((self.root/'course-evidence.txt').exists())
        self.assertFalse((self.root/FOLDERS['m2-demo1']/'logs').exists())
        self.assertIn('CLEANUP COMPLETE',result.stdout)
        self.assert_restored()


if __name__=='__main__':unittest.main()
