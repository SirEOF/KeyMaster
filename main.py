#!/usr/bin/env python3

from cmdloop import CmdRunner

def main():
    canceled = False

    while not canceled:
        try:
            CmdRunner().cmdloop()
            canceled = True
        except KeyboardInterrupt:
            print('')
            
    print('')

if __name__ == '__main__':
    main()

