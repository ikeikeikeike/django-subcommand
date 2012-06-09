import os
from ..base import SubCommand

class Command(SubCommand):
    command_name = os.path.split(__file__)[-1].split('.')[0]
    help = ("""General options:  """.format(cmd_name=command_name))