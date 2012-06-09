import os
import sys
import collections

from django.utils import termcolors
from django.core.management.color import supports_color
from django.core.management import LaxOptionParser
from django.core.management.templates import TemplateCommand
from django.core.management.base import (
    BaseCommand,
    AppCommand,
    NoArgsCommand,
    LabelCommand,
    handle_default_options
)
from generate_scaffold.management.verbosity import VerboseCommandMixin

from ..management import (
    get_subcommands,
    embedded_color,
    load_subcommand_class
)


class SubCommand(BaseCommand):

    args = '<sub sub ...>'
    sub = 'sub'

    def __init__(self, argv=None):
        super(SubCommand, self).__init__()
        self.argv = argv or sys.argv[:]
        self.command_name = os.path.basename(self.argv[1])

    def create_parser(self, prog_name, subcommand):
        return LaxOptionParser(prog=prog_name,
                               usage=self.usage(subcommand),
                               version=self.get_version(),
                               option_list=self.option_list)

    def print_help(self, prog_name, subcommand):
        return self.create_parser(prog_name, subcommand).print_lax_help()

    def run_from_argv(self, argv):
        if argv[2:] in (['--help'], ['-h']):
            self.print_help(self.argv[0], self.argv[1])
            sys.stdout.write(self.help_text() + '\n')
            exit()
        super(SubCommand, self).run_from_argv(argv)

    def sub_usage(self, command_name=None):
        return [
            "",
            "Type '{0} help <subcommand>' for help on a specific" \
            " subcommand.".format(command_name or self.command_name),
            "",
            "Available subcommands:",
        ]

    def help_text(self, command_name=None):
        commands_dict = collections.defaultdict(lambda: [])
        for app, name in get_subcommands(command_name or self.command_name).iteritems():
            app = app.rpartition('.')[-1]
            commands_dict[app].extend(map(lambda n: "{0}:{1}".format(app, n), name))
        return embedded_color(self.sub_usage(), commands_dict)

    def handle(self, *subs, **options):
        if not subs:
            self.print_help(self.argv[0], self.argv[1])
            sys.stdout.write(self.help_text() + '\n')
            return
        output = []
        for sub in subs:
            sub_output = self.handle_sub(sub, **options)
            if sub_output:
                output.append(sub_output)
        return '\n'.join(output)

    def fetch_command(self, sub):
        try:
            app_name, subcommand = sub.split(":")
            if not subcommand in get_subcommands(self.command_name)[app_name]:
                raise ValueError
        except (KeyError, ValueError, IndexError):
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n" % (
                sub, self.command_name))
            sys.exit(1)

        return load_subcommand_class(app_name, self.command_name, subcommand)

    def handle_sub(self, sub, **options):
        self.fetch_command(sub).run_from_argv(self.argv)


class CommandMixin(VerboseCommandMixin):

    def __init__(self, *args, **kwargs):
        super(CommandMixin, self).__init__(*args, **kwargs)
        self.argv = kwargs.get("argv") or sys.argv[:]
        self.package = self.__class__.__module__.split(".")[0]
        self.basecommand = self.argv[1]
        try:
            self.usercommand = self.argv[2]
        except IndexError:
            self.usercommand = ""
        if supports_color():
            opts = ('bold',)
            self.style.DESTROY = termcolors.make_style(fg='red', opts=opts)
            self.style.NOTFOUND = termcolors.make_style(fg='white', opts=opts)
            self.style.NOTEMPTY = termcolors.make_style(fg='black', opts=opts)


class SubCommandMixin(CommandMixin):

    def usage(self, subcommand):
        usage = '%prog {0} {1} [options] {2}'.format(subcommand, self.usercommand, self.args)
        if self.help:
            return '{0}\n\n{1}'.format(usage, self.help)
        return usage

    def run_from_argv(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        options, args = parser.parse_args(argv[3:])
        handle_default_options(options)
        self.execute(*args, **options.__dict__)


class BaseSubCommand(SubCommandMixin, BaseCommand):
    pass


class AppSubCommand(SubCommandMixin, AppCommand):
    pass


class LabelSubCommand(SubCommandMixin, LabelCommand):
    pass


class NoArgsSubCommand(SubCommandMixin, NoArgsCommand):
    pass


class TemplateSubCommand(SubCommandMixin, TemplateCommand):
    pass


class BaseVerboseCommand(CommandMixin, BaseCommand):
    pass