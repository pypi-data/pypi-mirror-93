#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2018.11.28
from __future__ import print_function
vlogs = {
    '0.0.8': 'add text search template',
    '0.0.9': 'update service template url; auto check version',
    '0.1.0': 'add go source file wathdog',
    '0.1.1': 'add api version',
    '0.1.2': 'fix page',
    '0.1.3': 'add string type or/like template, fix without manager query bug',
    '0.1.4': 'update watchgo/orm',
    '0.1.5': 'update swagger',
    '0.1.6': 'fix manager list relation',
    '0.1.7': 'fix with string like',
    '0.1.8': 'page 1 base: 注意当前版本分页功能从1开始, 应用层不需要再做pageIndex-1 操作!!!', # add change_log notify
    '0.1.9': 'add batch update',
    '0.1.10': 'fix batch update',
    '0.1.11': 'add reqRaw/respRaw api; float/array type',
    '0.1.12': 'gop v0.0.3',
    '0.1.13': 'gop v0.0.3',
    '0.1.14': 'add orm $in/$nin, nest api param',
    '0.1.15': 'fix remove pdb',
    '0.1.16': 'export orm.GetQuery, orm.Scan filter empty object',
    '0.1.17': 'add api alias',
    '0.1.18': 'update nest apimodel',
    '0.1.19': 'update swagger',
    '0.2.0': 'add api param validator',
    '0.2.9': 'openApi v3 and apiResp model',
    '0.2.10': 'go mod vendor auto',
    '0.2.11': 'update orm AllResultTo',
    '0.2.12': 'add form tag for apimodel',
    '0.3.0': 'add new struct v4',
    '0.3.1': 'auto load .env',
    '0.3.2': 'fix load .env',
    '0.3.3': 'add any router',
    '0.3.4': 'add python3 support',
    '0.3.5': 'fix swagger tags/servers',
    '0.3.6': 'add service code template',
    '0.3.7': 'add cmdmodel',
    '0.3.8': 'add wildcard router',
    '0.3.9': 'add swagger codegen',
    '0.4.0': 'add swagger security, json resp model',
    '0.4.1': 'add m2c init from git repo',
    '0.4.2': 'fix pack'
}

name = 'm2c'
version = '0.4.2'

from .conf import M2C_PATH, Color
from .helper import m2c_version

def change_log():
    curv = m2c_version()
    if not curv:
        return

    if curv == version:
        return

    print(Color.red(u'当前项目使用的m2c版本: %s' % curv))
    print(Color.red(u'使用m2c apicode 或者m2c objcode 可以更新当前版本'))
    print(Color.red(u'注意以下更新:'))
    for v, msg in vlogs.items():
        if v > curv:
            print(v, msg)


def check_version():
    import os
    import random
    from .conf import Color
    if random.randint(0, 10) % 2 == 0:
        return
    # random check for speed up
    change_log()
    text = os.popen('pip search %s' % name).read()
    need_update = False
    for line in text.splitlines():
        print(line)
        line = line.strip()
        if line.startswith('LATEST:'):
            need_update = True
    if need_update:
        print(Color.red('run: pip install -U %s, update it!' % name))
