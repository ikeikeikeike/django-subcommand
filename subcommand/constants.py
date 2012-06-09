from django.conf import settings

STYLETAGS = getattr(settings, "SUBCOMMAND_STYLETAGS", ["css", "less"])
SCRIPTTAGS = getattr(settings, "SUBCOMMAND_SCRIPTTAGS", ["js", "coffee"])
