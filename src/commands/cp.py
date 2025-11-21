import os
from src import logging
import shutil

def cp(args):
    if len(args) < 2:
        print("cp: нужно указать источник и назначение")
        logging.log("cp", ok=False, error="нужно указать источник и назначение")
        return None
    
    r = '-r' in args
    clean = [a for a in args if a != '-r']
    if len(clean) < 2:
        print("cp: нужно указать источник и назначение")
        logging.log("cp", ok=False, error='нужно указать источник и назначение')
    
    src, dst = clean[0], clean[1]
    try:
        if os.path.isdir(src):
            if not r:
                print(f"cp: -r не указан; пропущен каталог '{src}'")
                logging.log(f"cp {' '.join(args)}", ok=False, error='опция -r не указана для каталога')
                return
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        logging.log(f"cp {' '.join(args)}")
    except Exception as e:
        print(f"cp: {e}")
        logging.log(f"cp {' '.join(args)}", ok=False, error=str(e))