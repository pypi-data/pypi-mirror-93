# -*- coding: utf-8 -*-


"""
heatdesert
"""
import argparse

from .core import ioliudownload

parser = argparse.ArgumentParser(prog='bingwp', add_help=False, description='download bing wallpaper')
parser.add_argument('-o', '--output', type=str, help='file output path')
parser.add_argument('-p', '--pack', action='store_true', help='pack file')

args = parser.parse_args()


def main():
    print('开始执行')
    """

    """
    path = None
    whether_pack = False

    if args.output is not None:
        path = args.output
    else:
        raise Exception('output is None')

    if args.pack is True:
        whether_pack = True

    ioliudownload(path, whether_pack)
    print('执行完毕')


if __name__ == '__main__':
    main()
