import argparse
import sys

from FacebookInspector import FacebookInspector

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Give information from FB.')
    parser.add_argument('--uid', default=None)
    parser.add_argument('--user', default=None)

    args = parser.parse_args()

    fbi = FacebookInspector()

    if args.uid:
        fbi.find_by_uid(args.uid)
    elif args.user:
        fbi.find_by_name(args.user)

    res = fbi.columns(['username', 'pic_big'])[1:3]

    print(res)

