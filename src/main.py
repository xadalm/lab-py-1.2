import os
from src.commands import ls, cd, cat, cp, mv, rm
from src import logging

def main():
    print("Мини-оболочка. Введите 'exit' для выхода.")
    while True:
        try:
            user_input = input(f"{os.getcwd()} $ ").strip()
            if not user_input:
                continue
            if user_input == "exit":
                break
            
            user_input = user_input.split()
            command = user_input[0]
            args = user_input[1:]

            if command == "ls":
                ls.ls(args)
            elif command == "cd":
                cd.cd(args)
            elif command == "cat":
                cat.cat(args)
            elif command == "cp":
                cp.cp(args)
            elif command == "mv":
                mv.mv(args)
            elif command == "rm":
                rm.rm(args)
            else:
                print(f"{command}: команда не найдена")
                logging.log(' '.join(user_input), ok=False, error="команда не найдена")
        except KeyboardInterrupt:
            print('\nВведите "exit" для выхода')
        except Exception:
            break

if __name__ == "__main__":
    main()