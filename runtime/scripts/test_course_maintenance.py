#!/usr/bin/env python3
"""Offline tests. Mock branch repositories are not course/runtime evidence."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

HERE=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj

# The author-guide generator and its tests moved to the private production repository.
sync=load('sync_all_branches')

class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.remote=self.base/'origin.git';self.root=self.base/'checkout'
        sync.run(['git','init','--bare',str(self.remote)],self.base)
        sync.run(['git','init','-b','main',str(self.root)],self.base)
        sync.run(['git','config','user.name','Test Author'],self.root)
        sync.run(['git','config','user.email','test@example.invalid'],self.root)
        (self.root/'base.txt').write_text('base\n')
        sync.run(['git','add','.'],self.root);sync.run(['git','commit','-m','base'],self.root)
        sync.run(['git','remote','add','origin',str(self.remote)],self.root)
        sync.run(['git','push','origin','main'],self.root)
    def child(self,name):
        sync.run(['git','switch','-c',name,'main'],self.root)
        (self.root/'unique.txt').write_text(name+'\n')
        sync.run(['git','add','.'],self.root);sync.run(['git','commit','-m','unique'],self.root)
        sync.run(['git','push','origin',name],self.root)
        sync.run(['git','switch','main'],self.root)
    def advance(self):
        (self.root/'foundation.txt').write_text('shared update\n')
        sync.run(['git','add','.'],self.root);sync.run(['git','commit','-m','shared update'],self.root)
        sync.run(['git','push','origin','main'],self.root)
    def test_more_than_twenty_branches_keep_unique_work(self):
        for i in range(21):self.child('team/demo-'+str(i))
        self.advance()
        result=sync.synchronize(self.root,apply=True,validator=lambda root,branch:None)
        self.assertTrue(result['synchronization_verified'])
        self.assertEqual(result['child_branches_discovered'],21)
        for row in result['branches']:
            self.assertEqual(row['behind_main'],0)
            self.assertTrue(sync.ancestor(self.root,row['before_sha'],row['after_sha']))
            content=sync.run(['git','show',row['after_sha']+':unique.txt'],self.root).stdout.strip()
            self.assertEqual(content,row['branch'])
    def test_conflict_does_not_reset_branch(self):
        self.child('work/in-progress')
        sync.run(['git','switch','work/in-progress'],self.root)
        (self.root/'base.txt').write_text('branch change\n')
        sync.run(['git','commit','-am','child conflict'],self.root);sync.run(['git','push','origin','work/in-progress'],self.root)
        old=sync.run(['git','rev-parse','HEAD'],self.root).stdout.strip()
        sync.run(['git','switch','main'],self.root)
        (self.root/'base.txt').write_text('main change\n')
        sync.run(['git','commit','-am','main conflict'],self.root);sync.run(['git','push','origin','main'],self.root)
        result=sync.synchronize(self.root,apply=True,validator=lambda root,branch:None)
        self.assertFalse(result['synchronization_verified'])
        self.assertEqual(result['branches'][0]['status'],'CONFLICT — NOT PUSHED')
        self.assertEqual(result['branches'][0]['verified_remote_sha'],old)

if __name__=='__main__':unittest.main()
