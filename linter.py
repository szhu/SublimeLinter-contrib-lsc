#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2015 The SublimeLinter Community
#
# License: MIT
#

"""This module exports the Lsc plugin class."""

from SublimeLinter.lint import Linter, util


class MultiRegex:
    def __init__(self, *pattern_srcs):
        import re
        self.pattern_srcs = pattern_srcs
        self.patterns = list(map(re.compile, pattern_srcs))

    def finditer(self, *args, **kwargs):
        for pattern_src, pattern in zip(self.pattern_srcs, self.patterns):
            # print('DEBUG: Pattern:', pattern_src)
            matches = pattern.finditer(*args, **kwargs)
            if matches:
                for match in matches:
                    yield match


class Lsc(Linter):

    """Provides an interface to coffee --compile."""

    syntax = 'livescript'
    cmd = 'lsc --compile --stdin'
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 1.4'
    multiline = True
    regex = MultiRegex(
        r'''\[(?P<message>[^\r\n]+) on line (?P<line>\d+)\]''',
        r'''\[Error: Parse error on line (?P<line>\d+): (?P<message>[^\r\n]+)\]'''
    )
    error_stream = util.STREAM_STDERR
    comment_re = r'\s*/[/*]'
