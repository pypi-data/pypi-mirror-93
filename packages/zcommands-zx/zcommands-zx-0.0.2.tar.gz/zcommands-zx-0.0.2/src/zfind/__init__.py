#! /usr/bin/env python3
# coding=utf-8
import os, sys


def show_help():
    help_txt = """
使用 zfind -h 来获取帮助
使用 zfind 关键字 在当前目录查询含有`关键字`的md文档
使用 zfind 关键字 -d 路径 在指定目录查询含有`关键字`的md文档
使用 zfind 关键字 -d 路径 -s 文件后缀 在指定目录查询含有`关键字`的指定后缀文档
使用 zfind 关键字 -d 路径 -s 文件后缀 -t 查找类型(d:文件夹, f: 文件) 在指定目录查询含有`关键字`的指定后缀文档
使用 zfind 关键字 -e 排除路径 排除路径中含有你不想搜索的路径

技巧:
    如果想同时查找多个后缀,可以使用`+`进行连接,中间不得有空格

    例如: zfind ok -s html+htm+md 会生成三条命令:
        (1)find  -L . -iname "*ok*.html" -type f
        (2)find  -L . -iname "*ok*.htm" -type f
        (3)find  -L . -iname "*ok*.md" -type f

问题:
    暂时无法检测失效软链接的问题
    """
    print(help_txt)


######################## 准备变量
search_dir = ''
keyword = ''
suffix = ''
type = ''
exclude = ''

args = sys.argv
if len(args) == 1:
    show_help()
    exit(0)
if len(args) > 1 and args[1] == '-h':
    show_help()
    exit(0)
if len(args) >= 2:
    keyword = sys.argv[1]

# 捕捉多余可选参数
opt_args = args[2:]
for i in range(len(opt_args)):
    if (opt_args[i] == '-s'):
        suffix = opt_args[i + 1]
    if (opt_args[i] == '-d'):
        search_dir = opt_args[i + 1]
    if (opt_args[i] == '-t'):
        type = opt_args[i + 1]
    if (opt_args[i] == '-e'):
        exclude = opt_args[i + 1]

######### 执行命令
search_dir = search_dir or '.'
suffix = suffix or 'md'
type = type or 'f'

if type == 'd':
    suffix = ''
else:
    if '+' in suffix:
        suffixes = suffix.split('+')
        # suffix = '.'+ suffix
        suffixes = list(set(suffixes))  # 去重
        suffixes = ['.' + item for item in suffixes]
        suffix = suffixes


def islist(a):
    from typing import List
    return isinstance(a, List)


def make_command(keyword, search_dir, suffix, type, exclude):
    command = []
    if islist(suffix):
        for suffix_part in suffix:
            command_part = 'find  -L {} -iname "*{}*.{}" -type {} -print '.format(search_dir, keyword, suffix_part, type)
            if exclude:
                command_part += ' -o -path "*{}*" -prune'.format(exclude)
            command.append(command_part)
    else:
        command = 'find  -L {} -iname "*{}*.{}" -type {} -print '.format(search_dir, keyword, suffix, type)
        if exclude:
            command += ' -o -path "*{}*" -prune'.format(exclude)
    # 兼容查询软链接命令, 兼容大小写
    # example as: find . -iname "*@make*.md"
    return command


def exec_command(command):
    if islist(command):
        ret = []
        for command_part in command:
            print("the command is: ", command_part)
            ret_part = os.popen(command_part).readlines()
            ret.extend(ret_part)
    else:
        print("the command is: ", command)
        ret = os.popen(command).readlines()
    return ret


command = make_command(keyword, search_dir, suffix, type, exclude)
ret = exec_command(command)
for line in ret:
    print(line, end='')






