import os
import sys
from datetime import datetime
import stat
from src import logging

def ls(args):
    detailed = '-l' in args        
    path = [n for n in args if n != '-l'] or ['.']
    for p in path:
        if not os.path.isdir(p):
            name = os.path.basename(p)
            if detailed:
                try:
                    size = os.path.getsize(p)
                    time = datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")
                    perms = stat.filemode(os.stat(p).st_mode)
                    print(f'{size:10} {time} {perms} {name}')
                except OSError:
                    print(name, file=os.sys.stderr)
            else:
                print(name)
            continue
        try:
            for name in sorted(os.listdir(p)):
                full_path = os.path.join(p, name)
                if detailed:
                    try:
                        size = os.path.getsize(full_path)
                        time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M")
                        perms = stat.filemode(os.stat(full_path).st_mode)
                        print(f'{size:10} {time} {perms} {name}')
                    except OSError:
                        print(name, file=os.sys.stderr)
                else:
                    print(name)
        except PermissionError:
            print(f"ls: не получается открыть директорию '{p}': Запрос отклонен", file=os.sys.stderr)
    logging.log(f"ls {' '.join(args)}")        