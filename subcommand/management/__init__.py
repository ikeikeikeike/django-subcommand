import os
import collections

from django.utils.importlib import import_module
from django.core.management import find_management_module
from django.core.management.color import color_style


def embedded_color(usage, commands_dict):
    style = color_style()
    for app in sorted(commands_dict.keys()):
        usage.append("")
        usage.append(style.NOTICE("[%s]" % app))
        for name in sorted(commands_dict[app]):
            usage.append("    %s" % name)
    return '\n'.join(usage)


def load_subcommand_class(command, app_name, name):
    module = import_module('%s.management.commands.%s.%s' % (command, app_name, name))
    return module.Command()


def find_subcommands(management_dir, command):
    commands = []
    command_dir = os.path.join(management_dir, "commands", command)
    try:
        commands += [f[:-3] for f in os.listdir(command_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        pass
    return commands


def get_subcommands(command):
    commands_dict = collections.defaultdict(lambda: [])
    try:
        from django.conf import settings
        apps = settings.INSTALLED_APPS
    except (AttributeError, EnvironmentError, ImportError):
        apps = []
    for app_name in apps:
        try:
            path = find_management_module(app_name)
            for name in find_subcommands(path, command):
                commands_dict[app_name].append(name)
        except ImportError:
            pass
    return commands_dict
