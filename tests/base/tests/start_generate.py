import re
import os.path
import shutil
from subcommand.management.commands.startsubcommand import Command
from .base import BaseTest


class StartGenerateTest(BaseTest):
    """ self.assertNotRaises
    """
    def setUp(self):
        super(StartGenerateTest, self).setUp()
        self.new_setUp()
        self.command = Command()

    def tearDown(self):
        super(StartGenerateTest, self).tearDown()
        sub = self.command.get_subcommand_dir()
        base = self.command.get_basecommand_dir()
        if os.path.exists(sub):
            shutil.rmtree(sub)
            if os.path.exists(base):
                shutil.rmtree(base)
        self.new_tearDown()
        self.command = None

    def test_exit(self):
        self.assertRaises(
            SystemExit, self.command.execute, "ExceptionTest",
            stdout=self.stdout, stderr=self.stderr)

    def test_help1(self):
        self.assertRaises(
            SystemExit, self.command.execute, stdout=self.stdout, stderr=self.stderr)

    def test_validate1(self):
        """ check base validation buffer """
        self.assertRaises(
            SystemExit, self.command.execute, stdout=self.stdout, stderr=self.stderr)

        bufs = self.stderr.buflist
        test_bufs = ['Error: You must provide an app_name.\n']

        for buf, test_buf in zip(bufs, test_bufs):
            self.assertTrue(re.search(test_buf, buf))
        self.assertTrue(len(bufs) == 1)

    def test_validate2(self):
        """ check installed_apps """
        self.assertRaises(
            SystemExit, self.command.execute, "INSTALLED_APPS",
            stdout=self.stdout, stderr=self.stderr)

        bufs = self.stderr.buflist
        test_bufs = [('Error: base. App with label INSTALLED_APPS '
                      'could not be found. Are you sure your INSTALLED_APPS '
                      'setting is correct?\n')]

        for buf, test_buf in zip(bufs, test_bufs):
            self.assertTrue(re.search("not be found. Are you sure your INSTALLED_APPS", buf))
        self.assertTrue(len(bufs) == 1)

    def test_validate3(self):
        """ check subcommand name """
        self.assertRaises(
            SystemExit, self.command.execute, "base",
            stdout=self.stdout, stderr=self.stderr)

        bufs = self.stderr.buflist
        test_bufs = ['Error: You must provide an subcommand name.\n']

        for buf, test_buf in zip(bufs, test_bufs):
            self.assertTrue(re.search(test_buf, buf))
        self.assertTrue(len(bufs) == 1)

    def test_generate1(self):
        """ generate child command """
        self.assertRaises(
            SystemExit, self.command.execute, "base", "child",
            stdout=self.stdout, stderr=self.stderr)

        self.assertTrue(len(self.stderr.buflist) == 0, "Error: No buffer.")

        bufs = self.stdout.buflist
        self.assertTrue(len(bufs) == 9, bufs)
