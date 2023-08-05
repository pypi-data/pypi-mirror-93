# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for igwn-accounting tests
"""

import json

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"


def history_from_jsonl(file, outf):
    with open(file, 'r') as fp:
        for i, line in enumerate(fp):
            data = json.loads(line)
            for key, val in data.items():
                if isinstance(val, str):
                    print("{} = \"{}\"".format(key, val), file=outf)
                else:
                    print("{} = {}".format(key, val), file=outf)
            print("ClusterId = {}".format(i), file=outf)
            print("JobStatus = 4", file=outf)
            print("JobUniverse = 5", file=outf)
            print("EnteredCurrentStatus = 1609500000.0", file=outf)
            print(
                "*** Offset = 0 ClusterId = {} Owner = {}".format(
                    i,
                    data["Owner"],
                ),
                file=outf,
            )
