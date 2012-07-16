from distutils.sysconfig import get_python_lib
import os
import shutil
from ..generate import GenerateCommand


class Command(GenerateCommand):

    def handle_generate(self, *args, **options):

        self.destroy = options.get("destroy", False)

        src = self.get_subcommand_dir()
        self.empty_package(os.path.join(src))
        self.empty_package(os.path.join(src, "commands"))
        self.empty_package(os.path.join(src, "commands", self.subcommand_name))
        self.template("startsubcommand.py", os.path.join(
            src, "commands", self.subcommand_name, "sample.py"))

        # copy subcommand package.
        to_package = self.get_basecommand_dir()
        self.create_subcommand_lib(to_package)

        # create
        self.create_file(os.path.join(
            to_package, "management", "commands", "{0}.py".format(self.subcommand_name)
        ), write="from ..commands import Command\n")

        self.run()

    def create_subcommand_lib(self, to_package):
        if not os.path.exists(to_package):
            shutil.copytree(self.package_dir, to_package)
            self.stdout.write("\n   Note!! Copy package from site-package ({0})\n\n".format(to_package))

    def get_subcommand_dir(self):
        return os.path.join(self.app_dir, "management")

    def get_basecommand_dir(self):
        return os.path.join(self.app_dir, "..", "subcommand")
