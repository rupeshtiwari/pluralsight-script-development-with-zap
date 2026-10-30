"""Run native Bash steps with controlled API responses; no live ZAP proof."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

class NativeZapTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'course checkout';self.root.mkdir()
        scripts=self.root/'runtime/scripts';scripts.mkdir(parents=True)
        for name in ('lib.sh','zap_scan.py'):
            shutil.copy2(HERE/name,scripts/name)
        self.env=dict(os.environ,TEST_ROOT=str(self.root))

    def run_library(self,folder,code):
        demo=self.root/folder
        (demo/'scripts').mkdir(parents=True,exist_ok=True)
        library=demo/'scripts/_steps.sh'
        shutil.copy2(ROOT/folder/'scripts/_steps.sh',library)
        return subprocess.run(['bash','-c','set -o pipefail\nsource "$1"\nfm() { printf "%s\\n" "$*"; }\n'+code,
                               'native-test',str(library)],cwd=demo,env=self.env,
                              capture_output=True,text=True,timeout=10)

    def marker(self,code):
        return self.run_library('demos/module1-demos/m1-demo2-javascript-http-sender',code)

    def scan(self,code):
        return self.run_library('demos/module2-demos/m2-demo2-zap-api-scan-evidence',code)

    def test_marker_finds_newest_request_after_long_history(self):
        # Reproduce the actual CoreAPI 1-based inclusive positive-start semantics.
        state=self.root/'history.json'
        state.write_text(json.dumps([{'requestHeader':f'GET /old/{i} HTTP/1.1\r\n'} for i in range(200)]))
        result=self.marker(r'''
PROBE_NAME=marker-current-123
PROBE_URL="${APP_INTERNAL}/greet?name=${PROBE_NAME}"
zap() {
 python3 - "$1" "${2:-}" <<'API'
import json,os,sys
from pathlib import Path
from urllib.parse import parse_qs
rows=json.loads((Path(os.environ['TEST_ROOT'])/'history.json').read_text())
rows.append({'requestHeader':'GET /greet?name=marker-current-123 HTTP/1.1\r\nX-Globomantics-Marker: GLOBO-DEMO\r\n'})
if sys.argv[1]=='core/view/numberOfMessages':print(json.dumps({'numberOfMessages':str(len(rows))}))
else:
 q=parse_qs(sys.argv[2]);base=q.get('baseurl',[''])[0]
 if '?name=marker-current-123' in base:rows=rows[-1:]
 start=int(q.get('start',['0'])[0]);count=int(q.get('count',['50'])[0])
 offset=start-1 if start>0 else 0
 print(json.dumps({'messages':rows[offset:offset+count]}))
API
}
marker_request_line
''')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('marker-current-123',result.stdout)
        self.assertIn('X-Globomantics-Marker: GLOBO-DEMO',result.stdout)

    def test_marker_does_not_accept_a_different_requests_header(self):
        result=self.marker(r'''
PROBE_NAME=marker-current-123
PROBE_URL="${APP_INTERNAL}/greet?name=${PROBE_NAME}"
zap() { printf '%s\n' '{"messages":[{"requestHeader":"GET /greet?name=marker-older-999 HTTP/1.1\r\nX-Globomantics-Marker: GLOBO-DEMO\r\n"}]}'; }
marker_request_line
''')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(result.stdout,'')

    def test_stale_console_registration_is_preserved_with_clear_recovery(self):
        result=self.marker(r'''
probe_until_marked() { printf '%s' 'GET /greet?name=marker-current-123 HTTP/1.1 || X-Globomantics-Marker: GLOBO-DEMO'; }
console_line() { printf ''; }
zap() { echo "MUST NOT REMOVE GUI WORK" >&2; return 1; }
step3_console_output
''')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('older in-memory copy',result.stdout)
        self.assertIn('save unsaved Script Console work first',result.stdout)
        self.assertNotIn('MUST NOT REMOVE',result.stderr)

    def test_scan_wait_and_display_follow_own_new_id_despite_shuffled_history(self):
        result=self.scan(r'''
# API snapshots deliberately put the old FINISHED scan last.
zap() {
 case "$1" in
 ascan/view/scans)
   if [ ! -e "$TEST_ROOT/plan-started" ]; then
     printf '%s' '{"scans":[{"id":"5","progress":"100","state":"FINISHED","reqCount":"4"}]}'
   else
     n="$(cat "$TEST_ROOT/polls" 2>/dev/null || echo 0)";n=$((n+1));echo "$n" > "$TEST_ROOT/polls"
     if [ "$n" -le 2 ]; then progress=66;state=RUNNING;else progress=100;state=FINISHED;fi
     printf '{"scans":[{"id":"6","progress":"%s","state":"%s","reqCount":"3"},{"id":"5","progress":"100","state":"FINISHED","reqCount":"4"}]}' "$progress" "$state"
   fi ;;
 core/view/version) echo '{"version":"2.17.0"}' ;;
 automation/view/planProgress) echo '{"error":[]}' ;;
 context/view/context) echo '{"context":{"id":"1"}}' ;;
 users/view/usersList) echo '{"usersList":[{"name":"alice"}]}' ;;
 *) echo '{"error":[]}' ;;
 esac
}
run_plan() { touch "$TEST_ROOT/plan-started";PLAN_ID=7; }
plan_finished() { return 0; }
custom_present() { printf yes; }
sleep() { echo waited >> "$TEST_ROOT/waits"; }
step1_api_status
''')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('id=6 · progress=100% · state=FINISHED',result.stdout)
        self.assertTrue((self.root/'waits').exists(),'an older finished scan must not bypass the wait')
        state=self.root/'demos/module2-demos/m2-demo2-zap-api-scan-evidence/logs/.m2demo2-state'
        self.assertEqual(state.read_text(),'plan=7\nscan=6\n')

    def test_direct_step_failure_is_nonzero_and_invalidates_old_scan_state(self):
        result=self.scan(r'''
printf 'plan=1\nscan=old\n' > "$STATE"
zap() { echo '{}';return 1; }
step1_api_status
''')
        self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertNotIn('ok ',result.stdout)
        self.assertFalse((self.root/'demos/module2-demos/m2-demo2-zap-api-scan-evidence/logs/.m2demo2-state').exists())

    def test_later_step_requires_persisted_scan_not_another_finished_scan(self):
        result=self.scan(r'''
printf 'plan=1\nscan=6\n' > "$STATE"
custom_present() { printf yes; }
zap() { echo '{"scans":[{"id":"6","progress":"66","state":"RUNNING"},{"id":"7","progress":"100","state":"FINISHED"}]}'; }
ensure_scan
''')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('no finished authenticated scan',result.stdout)

    def test_final_plan_validation_failure_cannot_enable_later_steps(self):
        for defect in ('error','user'):
            with self.subTest(defect=defect):
                self.env['TEST_DEFECT']=defect
                (self.root/'plan-started').unlink(missing_ok=True)
                result=self.scan(r'''
zap() {
 case "$1" in
 ascan/view/scans)
  if [ -e "$TEST_ROOT/plan-started" ];then echo '{"scans":[{"id":"6","progress":"100","state":"FINISHED","reqCount":"3"}]}';else echo '{"scans":[]}';fi ;;
 core/view/version) echo '{"version":"2.17.0"}' ;;
 automation/view/planProgress)
  if [ "$TEST_DEFECT" = error ];then echo '{"error":["fixture error"]}';else echo '{"error":[]}';fi ;;
 context/view/context) echo '{"context":{"id":"1"}}' ;;
 users/view/usersList)
  if [ "$TEST_DEFECT" = user ];then echo '{"usersList":[]}';else echo '{"usersList":[{"name":"alice"}]}';fi ;;
 *) echo '{"error":[]}' ;;
 esac
}
run_plan() { touch "$TEST_ROOT/plan-started";PLAN_ID=1; }
plan_finished() { return 0; }
custom_present() { printf yes; }
step1_api_status;first=$?
ensure_scan;later=$?
printf 'FIRST=%s LATER=%s\n' "$first" "$later"
[ "$first" -ne 0 ] && [ "$later" -ne 0 ] && [ ! -e "$STATE" ]
''')
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertIn('FIRST=1 LATER=1',result.stdout)

    def test_real_plan_completion_predicate_rejects_empty_null_and_unrelated_timestamps(self):
        for folder in ('m2-demo1-authenticated-zap-github-actions','m2-demo2-zap-api-scan-evidence'):
            for finished in ('',None,False,[],{},'bad-time','2026-10-30T12:00:00Z'):
                with self.subTest(folder=folder,finished=finished):
                    self.env['TEST_PROGRESS']=json.dumps({'finished':finished,'started':'2026-10-30T11:00:00Z','info':['finished job2026-10-30T11:00:00Z']})
                    result=self.run_library('demos/module2-demos/'+folder,r'''
PLAN_ID=0
zap() { printf '%s' "$TEST_PROGRESS"; }
plan_finished
''')
                    self.assertEqual(result.returncode==0,finished=='2026-10-30T12:00:00Z',result.stdout+result.stderr)

    def test_fresh_engine_waits_for_actual_plan_completion_before_looking_for_scan(self):
        result=self.scan(r'''
zap() {
 case "$1" in
 automation/view/planProgress)
  n="$(cat "$TEST_ROOT/plan-polls" 2>/dev/null || echo 0)";n=$((n+1));echo "$n" > "$TEST_ROOT/plan-polls"
  if [ "$n" -lt 3 ];then
   echo '{"finished":"","error":[],"started":"2026-10-30T11:00:00Z"}'
  else
   touch "$TEST_ROOT/plan-complete"
   echo '{"finished":"2026-10-30T12:00:00Z","error":[]}'
  fi ;;
 ascan/view/scans)
  if [ -e "$TEST_ROOT/plan-complete" ];then echo '{"scans":[{"id":"6","progress":"100","state":"FINISHED","reqCount":"3"}]}';else echo '{"scans":[]}';fi ;;
 core/view/version) echo '{"version":"2.17.0"}' ;;
 context/view/context) echo '{"context":{"id":"1"}}' ;;
 users/view/usersList) echo '{"usersList":[{"name":"alice"}]}' ;;
 *) echo '{"error":[]}' ;;
 esac
}
run_plan() { PLAN_ID=1; }
custom_present() { printf yes; }
sleep() { echo waited >> "$TEST_ROOT/waits"; }
step1_api_status
''')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual((self.root/'waits').read_text().splitlines(),['waited','waited'])
        self.assertIn('id=6 · progress=100% · state=FINISHED',result.stdout)

    def test_later_m2_demo1_commands_stop_when_real_priming_wait_fails(self):
        folder='demos/module2-demos/m2-demo1-authenticated-zap-github-actions'
        self.assertEqual(self.run_library(folder,'true').returncode,0)
        scripts=self.root/folder/'scripts'
        (scripts/'_steps.sh').rename(scripts/'_actual_steps.sh')
        (scripts/'_steps.sh').write_text(r'''
source "$(dirname "${BASH_SOURCE[0]}")/_actual_steps.sh"
fm() { printf '%s\n' "$*"; }
ensure_ready() { return 0; }
reflection_reached() { printf ''; }
run_plan() { PLAN_ID=0; }
zap() { echo '{"finished":"","error":[]}'; }
seq() { echo 1; }
sleep() { :; }
step2_context_config() { touch "$TEST_ROOT/WRONG_STEP"; }
step3_script_job() { touch "$TEST_ROOT/WRONG_STEP"; }
step4_custom_alert() { touch "$TEST_ROOT/WRONG_STEP"; }
''')
        entry=scripts/'_run_step.sh'
        shutil.copy2(ROOT/folder/'scripts/_run_step.sh',entry)
        for number in ('2','3','4'):
            with self.subTest(step=number):
                result=subprocess.run(['bash',str(entry),number],cwd=scripts.parent,
                                      env=self.env,capture_output=True,text=True,timeout=10)
                self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertIn('priming plan did not finish successfully',result.stdout)
                self.assertFalse((self.root/'WRONG_STEP').exists())

    def test_headless_error_gate_rejects_missing_and_wrong_type_error_lists(self):
        for document,expected in (({},'?'),({'error':''},'?'),({'error':{}},'?'),({'error':[]},'0')):
            with self.subTest(document=document):
                self.env['TEST_PROGRESS']=json.dumps(document)
                result=self.run_library('demos/module2-demos/m2-demo1-authenticated-zap-github-actions',r'''
PLAN_ID=0
zap() { printf '%s' "$TEST_PROGRESS"; }
plan_field error
''')
                self.assertEqual(result.stdout.strip(),expected)

    def test_ambiguous_new_scan_ids_are_rejected(self):
        result=self.scan(r'''
zap() {
 if [ -e "$TEST_ROOT/plan-started" ];then echo '{"scans":[{"id":"6"},{"id":"7"}],"error":[]}';else echo '{"scans":[],"error":[]}';fi
}
run_plan() { touch "$TEST_ROOT/plan-started";PLAN_ID=1; }
plan_finished() { return 0; }
step1_api_status
''')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('exactly one new',result.stdout+result.stderr)

if __name__=='__main__':unittest.main()
