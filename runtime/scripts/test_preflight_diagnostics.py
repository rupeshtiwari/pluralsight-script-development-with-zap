"""The shareable diagnosis must identify failures without exposing credentials."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('preflight_diagnostics',HERE/'preflight_diagnostics.py')
diag=importlib.util.module_from_spec(spec)
spec.loader.exec_module(diag)

class Response:
    status=200
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self):return json.dumps({'vulnerable':True,'postgres':'ok','mongo':'ok','version':'2.17.0'}).encode()

class Opener:
    def open(self,request,timeout):return Response()

class PreflightDiagnosticsTests(unittest.TestCase):
    def test_diagnostic_report_redacts_credentials_and_personal_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'FAIL-module2-demo1.log').write_text('STEP 2 · command: ./steps/02-test.sh\n✘ FAIL: missing plan\nFAIL: /Users/recorder/trace ZAP-secret-fixture\n')
            env={'ZAP_API_KEY':'ZAP-secret-fixture','GITHUB_TOKEN':'GitHub-secret-fixture',
                 'GH_TOKEN':'GH-secret-fixture','POSTGRES_PASSWORD':'PG-secret-fixture'}
            def command(*args,**kwargs):
                return subprocess.CompletedProcess(args,0,stdout='GitHub-secret-fixture /Users/recorder/course/file\n',stderr='')
            with patch.dict(os.environ,env),patch.object(diag.subprocess,'run',side_effect=command),patch.object(diag.urllib.request,'build_opener',return_value=Opener()):
                text=diag.build_report(root)
            for value in env.values():self.assertNotIn(value,text)
            self.assertNotIn('/Users/recorder',text)
            self.assertIn('STEP 2',text)
            self.assertIn('missing plan',text)
            self.assertIn('ZAP_API_KEY: present (value hidden)',text)
            self.assertIn('ZAP API: HTTP 200',text)

    def test_secrets_are_redacted_before_tool_output_is_truncated(self):
        secret='SECRET-value-crossing-truncation-boundary'
        def command(*args,**kwargs):
            return subprocess.CompletedProcess(args,0,stdout='x'*3990+secret,stderr='')
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ,{'GH_TOKEN':secret}),patch.object(diag.subprocess,'run',side_effect=command),patch.object(diag.urllib.request,'build_opener',return_value=Opener()):
                text=diag.build_report(Path(folder))
        self.assertNotIn('SECRET',text)
        self.assertNotIn(secret,text)

    def test_path_shaped_credentials_are_redacted_before_display_normalization(self):
        secret='/Users/fixture-user/secret-token-fixture'
        def command(*args,**kwargs):
            return subprocess.CompletedProcess(args,0,stdout=secret,stderr='')
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ,{'GH_TOKEN':secret}),patch.object(diag.subprocess,'run',side_effect=command),patch.object(diag.urllib.request,'build_opener',return_value=Opener()):
                text=diag.build_report(Path(folder))
        self.assertNotIn('secret-token-fixture',text)
        self.assertIn('<redacted>',text)

    def test_missing_tools_and_failed_connections_are_diagnostic_not_crashes(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(diag.subprocess,'run',side_effect=FileNotFoundError),patch.object(Opener,'open',side_effect=OSError),patch.object(diag.urllib.request,'build_opener',return_value=Opener()):
                text=diag.build_report(Path(folder))
            self.assertIn('FileNotFoundError',text)
            self.assertIn('connection failed',text)
            self.assertIn('Preflight source lock: absent',text)

if __name__=='__main__':unittest.main()
