import sys

from ..base import SubCommand
from ...management import (
    get_subcommands,
    load_subcommand_class
)

class Command(SubCommand):

    def help_text(self):
        return super(Command, self).help_text("generate")

    def fetch_command(self, sub):
        try:
            app_name, subcommand = sub.split(":")
            if not subcommand in get_subcommands("generate")[app_name]:
                raise ValueError
        except (KeyError, ValueError, IndexError):
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n" % (
                sub, self.command_name))
            sys.exit(1)

        return load_subcommand_class(app_name, "generate", subcommand)