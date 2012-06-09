import os
from optparse import make_option
from subcommand.management.base import BaseSubCommand


class Command(BaseSubCommand):
    command_name = os.path.split(__file__)[-1].split('.')[0]
    help = ("""General options:""".format(cmd_name=command_name))
    option_list = BaseSubCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'
        ),
    )

    def handle(self, *args, **options):
        print("NotImplemented!")