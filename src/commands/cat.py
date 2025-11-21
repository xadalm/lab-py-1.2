from src import logging
import os

def cat(args):
    if not args:
        print("cat: не указан файл")
        logging.log("cat", ok=False, error="не указан файл")
        return None
    path = args[0]
    if os.path.isdir(path):
        print(f"cat: {path}: это каталог, а не файл")
        logging.log(f"cat {path}", ok=False, error="это каталог, а не файл")
        return None
    try:
        with open(path, 'r') as f:
            print(f.read(), end='')
        logging.log(f"cat {path}")
    except Exception as e:
        print(f"cat: {path}: {e}")
        logging.log(f"cat {path}", ok=False, error=str(e))