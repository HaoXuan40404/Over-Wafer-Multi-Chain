import sys
import os
import argparse

sys.path.append(os.path.abspath('.') + './pytools')

import version

def main():
    parser = argparse.ArgumentParser('multi-chain usage')
    parser.add_argument('-C', '--config', type=str, dest='config',
                        help="input config file which in ini format")
    parser.add_argument("-V", "--version", action="store_true",
                        help="version of multi-chain")
    parser.add_argument("--new_account", help="generate a new account")
    args = parser.parse_args()

    for arg in args.__dict__.keys():
        print(args.__dict__)
        print(arg)
        if args.__dict__['version']:
            version.version('./release_note.txt')
            sys.exit(-1)
        elif arg == 'config':
            print(args.__dict__[arg])


if __name__ == '__main__':
    main()
