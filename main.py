import sys
import os
import argparse

sys.path.append(os.path.abspath('.') + './pys')

import version

def version():
    version.version('./release_note.txt')
    sys.exit(-1)

def main():
    parser = argparse.ArgumentParser('multi-chain usage')
    parser.add_argument('--config', type=str, dest='config',
                        help="input config file which in ini format")
    parser.add_argument("-V", "--version", action="store_true",
                        help="version of multi-chain")
    args = parser.parse_args()
    print(args)
    for arg in args.__dict__:
        if arg == 'version' and args.version:
            version()
        elif arg == 'config' and args.config is not None:
            config_file = args.config
            print(config_file)


if __name__ == '__main__':
    main()
