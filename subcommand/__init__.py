VERSION = (0, 0, 1, 'alpha', 1)

from django.conf import settings
setattr(settings, "COMPRESS_PRECOMPILERS", getattr(settings, "COMPRESS_PRECOMPILERS", (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)))