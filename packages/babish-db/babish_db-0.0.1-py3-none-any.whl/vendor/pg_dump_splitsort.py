#!/usr/bin/env python
"""
pgtricks:0.9.2.dev
https://github.com/akaihola/pgtricks/blob/master/pgtricks/pg_dump_splitsort.py

Copyright (c) 2010, Antti Kaihola
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of pgtricks nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import functools
import io
import os
import re
from typing import Tuple, Union, cast, Pattern, Match, Optional, List, IO, Any

import sys

COPY_RE = re.compile(r'COPY .*? \(.*?\) FROM stdin;\n$')


def try_float(s1: str, s2: str) -> Union[Tuple[str, str], Tuple[float, float]]:
    if not s1 or not s2 or s1[0] not in '0123456789.-' or s2[0] not in '0123456789.-':
        # optimization
        return s1, s2
    try:
        return float(s1), float(s2)
    except ValueError:
        return s1, s2


def linecomp(l1: str, l2: str) -> int:
    p1 = l1.split('\t', 1)
    p2 = l2.split('\t', 1)
    v1, v2 = cast(Tuple[float, float], try_float(p1[0], p2[0]))
    result = (v1 > v2) - (v1 < v2)
    if not result and len(p1) == len(p2) == 2:
        return linecomp(p1[1], p2[1])
    return result

DATA_COMMENT_RE = re.compile('-- Data for Name: (?P<table>.*?); '
                             'Type: TABLE DATA; '
                             'Schema: (?P<schema>.*?);')
SEQUENCE_SET_RE = re.compile(r'-- Name: .+; Type: SEQUENCE SET; Schema: |'
                             r"SELECT pg_catalog\.setval\('")

class Matcher(object):
    def __init__(self) -> None:
        self._match: Optional[Match[str]] = None

    def match(self, pattern: Pattern[str], data: str) -> Optional[Match[str]]:
        self._match = pattern.match(data)
        return self._match

    def group(self, group1: str) -> str:
        if not self._match:
            raise ValueError('Pattern did not match')
        return self._match.group(group1)


def split_sql_file(sql_filepath: str) -> None:

    directory = os.path.dirname(sql_filepath)

    output: Optional[IO[str]] = None
    buf: List[str] = []

    def flush() -> None:
        cast(IO[str], output).writelines(buf)
        buf[:] = []

    def new_output(filename: str) -> IO[str]:
        if output:
            output.close()
        return open(os.path.join(directory, filename), 'w')

    copy_lines: Optional[List[str]] = None
    counter = 0
    output = new_output('0000_prologue.sql')
    matcher = Matcher()

    for line in open(sql_filepath):
        if copy_lines is None:
            if line in ('\n', '--\n'):
                buf.append(line)
            elif line.startswith('SET search_path = '):
                flush()
                buf.append(line)
            else:
                if matcher.match(DATA_COMMENT_RE, line):
                    counter += 1
                    output = new_output(
                        '{counter:04}_{schema}.{table}.sql'.format(
                            counter=counter,
                            schema=matcher.group('schema'),
                            table=matcher.group('table')))
                elif COPY_RE.match(line):
                    copy_lines = []
                elif SEQUENCE_SET_RE.match(line):
                    pass
                elif 1 <= counter < 9999:
                    counter = 9999
                    output = new_output('%04d_epilogue.sql' % counter)
                buf.append(line)
                flush()
        else:
            if line == '\\.\n':
                copy_lines.sort(key=functools.cmp_to_key(linecomp))
                buf.extend(copy_lines)
                buf.append(line)
                flush()
                copy_lines = None
            else:
                copy_lines.append(line)
    flush()


def main() -> None:
    split_sql_file(sys.argv[1])


if __name__ == '__main__':
    main()