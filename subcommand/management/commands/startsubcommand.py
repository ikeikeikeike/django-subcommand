raise NotImplementedError()
import os
from ..generate import GenerateCommand


class Command(GenerateCommand):

    def handle_generate(self, *args, **options):

        self.verbose = int(options.get('verbosity')) > 1
        self.dry_run = options.get("dry_run", False)
        self.destroy = options.get("destroy", False)


        src = os.path.join(self.app_dir, "management")
        self.empty_package(os.path.join(src))
        self.empty_package(os.path.join(src, "commands"))
        self.empty_package(os.path.join(src, "commands", self.subcommand_name))
        self.template("startsubcommand.py", os.path.join(
            src, "commands", self.subcommand_name, "sample.py"))

        src = os.path.abspath(os.path.dirname(__import__(__package__).__file__))
        self.create_file(os.path.join(
            src, "management", "commands", "{0}.py".format(self.subcommand_name)
        ), write="from ..commands import Command\n")

        self.run()
