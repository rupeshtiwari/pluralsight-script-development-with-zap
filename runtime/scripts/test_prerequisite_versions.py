"""Check copied prerequisites against real temporary branch trees, without a live lab."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from check_prerequisite_versions import check, TAUGHT

class PrerequisiteVersionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.git('init','-q','-b','main');self.git('config','user.name','Test');self.git('config','user.email','test@example.invalid')
        for demo,paths in TAUGHT.items():
            for path in paths:
                target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text('canonical '+path+'\n')
        self.git('add','.');self.git('commit','-qm','canonical')
        for demo in TAUGHT:self.git('update-ref','refs/remotes/origin/'+demo+'-after','HEAD')

    def git(self,*args):
        return subprocess.check_output(['git','-C',str(self.root),*args],text=True).strip()

    def save_ref(self,name):
        self.git('add','-A');self.git('commit','-qm',name);self.git('update-ref','refs/remotes/origin/'+name,'HEAD')

    def test_matching_before_after_pair_still_fails_when_reused_files_are_old(self):
        marker=next(iter(TAUGHT['m1-demo2']));plan=next(iter(TAUGHT['m2-demo1']))
        for path in (marker,plan):(self.root/path).write_text('old reused version\n')
        self.save_ref('m2-demo2-before')
        self.git('update-ref','refs/remotes/origin/m2-demo2-after','HEAD')
        problems=check(self.root)
        self.assertEqual(len(problems),4)
        self.assertTrue(all('m2-demo2-' in problem for problem in problems))
        self.assertTrue(any(marker in problem for problem in problems))
        self.assertTrue(any(plan in problem for problem in problems))

    def test_intentionally_absent_starter_answer_is_preserved(self):
        for path in TAUGHT['m1-demo2']:(self.root/path).unlink()
        self.save_ref('m1-demo2-before')
        self.assertEqual(check(self.root),[])
        self.assertFalse((self.root/next(iter(TAUGHT['m1-demo2']))).exists())

    def test_unrelated_branch_changes_remain_valid(self):
        (self.root/'notes.md').write_text('other course work\n');self.save_ref('integration/notes')
        self.assertEqual(check(self.root),[])

if __name__=='__main__':unittest.main()
