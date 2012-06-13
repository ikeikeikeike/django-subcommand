import os
import re
from django import template
from django.conf import settings
from django.template import Node
from django.contrib.staticfiles.finders import AppDirectoriesFinder
from ..constants import (
    STYLETAGS,
    SCRIPTTAGS
)
from ..utils import regexconv

register = template.Library()

ext_ptn = re.compile("\.(?:{0})$".format(regexconv(STYLETAGS + SCRIPTTAGS)))
script_ptn = re.compile("\.(?:{0})$".format(regexconv(SCRIPTTAGS)))
style_ptn = re.compile("\.(?:{0})$".format(regexconv(STYLETAGS)))


class Staticfinder(object):

    def __init__(self, apps=list()):
        assert isinstance(apps, list), "Error: please input a list type"
        self.finder = AppDirectoriesFinder(apps=apps)

    def get_scriptfiles(self, ignore_patterns=ext_ptn):
        return [i[0] for i in self.finder.list(None) if ignore_patterns.search(i[0])]

    def get_scriptroot(self):
        return self.finder.find("")


class Tags(Node):

    def __init__(self, apps=list(), directory=None, url_root=None, finder=None):
        assert isinstance(apps, list), "Error: please input a list type"
        self.finder = finder or Staticfinder(apps=apps)
        self.directory = directory
        self.url_root = url_root or settings.STATIC_URL

    def join(self, src):
        return os.path.join(self.url_root, src)

    def _ext_type(self, ext):
        if "coffee" == ext:
            return "coffeescript"
        elif "js" == ext:
            return "javascript"
        else:
            return ext

    def render(self, context):
        dir_ptn = re.compile(self.directory or "")
        output = []
        for s in self.finder.get_scriptfiles():
            if not dir_ptn.search(s):
                continue
            elif script_ptn.search(s):
                output.append(self.script_tag(self.join(s), self._ext_type(s.split(".")[-1])))
            elif style_ptn.search(s):
                output.append(self.style_tag(self.join(s), self._ext_type(s.split(".")[-1])))
        return "\n".join(output)

    def script_tag(self, src, ext="javascript"):
        return '<script type="text/{ext}" charset="utf-8" \
                     src="{src}"></script>'.format(ext=ext, src=src)

    def style_tag(self, src, ext="css"):
        return '<link rel="stylesheet" type="text/{ext}" charset="utf-8" \
                     href="{src}"></link>'.format(ext=ext, src=src)


def do_generate(parser, token=list()):
    args = token.contents.split()
    assert len(args) > 1, "Error: arg length"
    app, directory = args[1], args[2] if len(args) > 2 else None
    return Tags([app], directory)


register.tag('generate', do_generate)
