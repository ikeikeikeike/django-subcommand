from __future__ import with_statement
from optparse import make_option
import shutil
import os

from django.core.management.base import CommandError
from django.template import Context
from django.template.loader import get_template
from django_spine import settings
from generate_scaffold.management.transactions import (
    FilesystemTransaction,
    FileModification,
    FileCreation,
    Filelike,
    DirectoryCreation
)

# external
import inflection
from generate_scaffold.utils.cacheclear import (
    reload_django_appcache,
    clean_pyc_in_dir
)

# ...
from .base import (
    BaseSubCommand
    # AppSubCommand,
    # LabelSubCommand,
    # NoArgsSubCommand,
    # TemplateSubCommand
)
from subcommand.management.base import BaseVerboseCommand
from ..utils import (
    dictmap,
    strext
)


class FileDestroy(object):
    def __init__(self, transaction, filename):
        self.transaction = transaction
        self.filename = filename
        self.backup_path = None

    def execute(self):
        self.backup_path = self.transaction.generate_path()
        if os.path.exists(self.filename):
            shutil.copy2(self.filename, self.backup_path)
#            self.transaction.msg("backup", self.filename)
        else:
            self.transaction.msg("notfound", self.filename)

    def rollback(self):
        if not self.transaction.is_dry_run:
            shutil.copy2(self.backup_path, self.filename)
        self.transaction.msg("revert", self.filename)

    def commit(self):
        if os.path.exists(self.filename):
            self.transaction.msg("destroy", self.filename)
            os.remove(self.filename)
            os.remove(self.backup_path)


class DirectoryDestroy(object):
    def __init__(self, transaction, dirname):
        self.transaction = transaction
        self.dirname = dirname

    def execute(self):
        self.backup_path = self.transaction.generate_path()
        if os.path.exists(self.dirname):
            os.mkdir(self.backup_path)
#            self.transaction.msg("backup", self.dirname)
        else:
            self.transaction.msg("notfound", self.dirname)

    def rollback(self):
        if not self.transaction.is_dry_run:
            shutil.copy2(self.backup_path, self.dirname)
        self.transaction.msg("revert", self.dirname)

    def commit(self):
        if os.path.exists(self.dirname):
            try:
                os.rmdir(self.dirname)
                self.transaction.msg("destroy", self.dirname)
            except OSError:
                self.transaction.msg("notempty", self.dirname)
            os.rmdir(self.backup_path)


class FilesystemTransactionWrapper(FilesystemTransaction):

    def __init__(self, is_dry_run=False, delegate=None, destroy=False):
        super(FilesystemTransactionWrapper, self).__init__(is_dry_run, delegate)
        self.destroy = destroy

    def rollback(self):
        for entry in self.log[::-1]:
            entry.rollback()

    def commit(self):
        for entry in self.log[::-1] if self.destroy else self.log:
            entry.commit()

    def open(self, filename, mode):
        if self.destroy:
            modification = FileDestroy(self, filename)
        elif os.path.exists(filename):
            modification = FileModification(self, filename)
        else:
            modification = FileCreation(self, filename)
        modification.execute()
        self.log.append(modification)
        if self.is_dry_run or self.destroy:
            return Filelike()
        else:
            return open(filename, mode)

    def mkdir(self, dirname):
        if self.destroy:
            modification = DirectoryDestroy(self, dirname)
            modification.execute()
            self.log.append(modification)
        elif os.path.exists(dirname):
            self.msg("exists", dirname)
        else:
            modification = DirectoryCreation(self, dirname)
            modification.execute()
            self.log.append(modification)


def transaction_wrapper(self, dry_run=False, destroy=False):
    # TODO: implement decorator.
    return FilesystemTransactionWrapper(dry_run, self, destroy)


class GenerateMixin(object):

    def __init__(self, *arg, **kwargs):
        super(GenerateMixin, self).__init__(*arg, **kwargs)
        self.app_name = ""
        self.app_dir = ""
        self.app_module = None
        self.class_name = ""
        self.fields = []
        self.verbose = 1
        self.dry_run = False
        self.nodes = []
        self.destroy = False
        self.inflect = inflection

    def template(self, template, src, **options):
        self.nodes.append({"src": src, "template": template, "options": options})

    def empty_directory(self, src, **options):
        self.nodes.append({"src": src, "template": False, "options": options})

    def create_file(self, src, **options):
        # TODO: direct input data.
        self.nodes.append({"src": src, "template": "dummy", "options": options})

    def empty_package(self, src, **options):
        self.empty_directory(src)
        self.create_file(os.path.join(src, "__init__.py"))

    def run(self, dry_run=False):
        with transaction_wrapper(self, dry_run, self.destroy) as transaction:
            for n in self.nodes:
                src = n.get("src")
                template = n.get("template")
                options = n.get("options")
                if template:
                    with transaction.open(src, "w+") as f:
                        data = self.render_template(template, **options)
                        f.seek(0)
                        f.write(options.get("write", "" if self.destroy else data))
                        self.log(f.read())
                else:
                    transaction.mkdir(src)
            reload_django_appcache()
        clean_pyc_in_dir(self.app_dir)

    def render_template(self, template, **options):
        c = {"package": self.package,
             "basecommand": self.basecommand,
             "usercommand": self.usercommand,
             "class_name": self.class_name,
             "app_name": self.app_name,
             "app_class": self.app_name,
             "app_dir": self.app_dir,
             "fields": map(lambda field: strext(field), self.fields),
             "template": template,
             "options": dictmap(strext, options)
        }
        dictmap(strext, c)

        try:
            return get_template("{0}/{1}".format(self.package, template)).render(Context(c))
        except Exception:
            return ""

    def handle(self, *args, **options):
        try:
            app_name = args[0]
        except IndexError:
            raise CommandError("You must provide an app_name.")

        if app_name not in settings.INSTALLED_APPS:
            raise CommandError(
                "{1}. App with label {0} could not be found. " \
                "Are you sure your INSTALLED_APPS setting is correct?".format(
                    app_name, self.usercommand))
        try:
            app_module = __import__(app_name)
        except ImportError:
            raise CommandError(
                "Could not import app with name: {0}".format(app_name))

        self.app_name = app_name
        self.app_module = app_module
        self.app_dir = app_module.__path__[0]
        self.destroy = self.basecommand == "destroy"

        self._handle_generate(*args, **options)
        exit()


class GenerateSubCommand(GenerateMixin, BaseSubCommand):

    def _handle_generate(self, *args, **options):
        self.handle_generate(*args, **options)


class GenerateCommand(GenerateMixin, BaseVerboseCommand):

    help = ("generate template command generator.")

    option_list = BaseVerboseCommand.option_list + (
        make_option('--destroy', action='store_true', dest='destroy', default=False,
            help='Destroy flg.'
        ),
    )

    def _handle_generate(self, *args, **options):
        try:
            self.subcommand_name = args[1]
        except IndexError:
            raise CommandError("You must provide an subcommand name.")

        self.handle_generate(*args, **options)
