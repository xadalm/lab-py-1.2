from src import logging
import os

def cd(args):
    if not args:
        print("cd: неправильно указан путь")
        logging.log("cd", ok=False, error="неправильно указан путь")
        return None
    path = args[0]
    path = os.path.expanduser(path)
    try:
        os.chdir(path.strip('"'))
        logging.log(f"cd {path}")
    except Exception as e:
        print(f"cd: {e}")
        logging.log(f"cd {path}", ok=False, error=str(e))