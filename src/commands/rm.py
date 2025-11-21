from src import logging
import os
import shutil

def rm(args):
    if not args:
        print("rm: не указан путь")
        logging.log("rm", ok=False, error="не указан путь")
        return
    
    r = '-r' in args
    clean = [a for a in args if a != '-r']
    if not clean:
        print("rm: не указан путь")
        logging.log("rm", ok=False, error="не указан путь")
        return
    
    path = clean[0]
    if path in ["/", ".."]:
        print("rm: запрещено удаление системного пути")
        logging.log(f"rm {path}", ok=False, error="запрещено удаление системного пути")
        return
    try:
        if os.path.isdir(path):
            if not r:
                print(f"rm: невозможно удалить '{path}': Это каталог.")
                logging.log(f"rm {' '.join(args)}", ok=False, error="невозможно удалить каталог без -r")
                return 
            confirm = input(f"rm: удалить каталог '{path}'? (y/n): ")
            if confirm.lower() == 'y':
                shutil.rmtree(path)
                logging.log(f"rm {path}")
            else:
                print("rm: операция отменена")
                logging.log(f"rm {path}", ok=False, error="операция отменена")
        else:
            os.remove(path)
            logging.log(f"rm {path}")
    except Exception as e:
        print(f"rm: {e}")
        logging.log(f"rm {path}", ok=False, error=str(e))