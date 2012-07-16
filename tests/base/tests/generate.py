from subcommand.management.commands.generate import Command
from .base import BaseTest


class GenerateTest(BaseTest):

    def setUp(self):
        super(GenerateTest, self).setUp()
        self.new_setUp()

    def tearDown(self):
        super(GenerateTest, self).tearDown()
        self.new_tearDown()

    def test_exit(self):
        command = Command()
        self.assertRaises(
            SystemExit,
            command.execute,
            "ExceptionTest",
#            stdout=self.stdout,
#            stderr=self.stderr
        )

    def test_help(self):
#        command = Command()
#        self.assertRaises(
#            SystemExit,
#            command.execute,
##            stdout=self.stdout,
##            stderr=self.stderr
#        )
        pass

    def test_generate(self):
#        command = controller.Command()
#        self.assertRaises(
#            SystemExit,
#            command.execute,
#            "gencmd", "classname",
##            stdout=self.stdout,
##            stderr=self.stderr
#        )
        pass

    def test_controller(self):
#        command = controller.Command()
#        self.assertRaises(
#            SystemExit,
#            command.execute,
#            "gencmd", "classname",
##            stdout=self.stdout,
##            stderr=self.stderr
#        )
        pass