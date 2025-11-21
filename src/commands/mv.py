import shutil
from src import logging

def mv(args):
    if len(args) < 2:
        print("mv: нужно указать источник и назначение")
        logging.log("mv", ok=False, error="нужно указать источник и назначение")
        return None
    src, dst = args[0], args[1]
    try:
        shutil.move(src, dst)
        logging.log(f"mv {' '.join(args)}")
    except Exception as e:
        print(f"mv: {e}")
        logging.log(f"mv {' '.join(args)}", ok=False, error=str(e))