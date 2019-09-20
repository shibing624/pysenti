# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import sys
r = set()
for line in sys.stdin:
    line = line.strip().split()
    if len(line) > 1:
        pass
    r.add(line[0])

for i in r:
    print(i)