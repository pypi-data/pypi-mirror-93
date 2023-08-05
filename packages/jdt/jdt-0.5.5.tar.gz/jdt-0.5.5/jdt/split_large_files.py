#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

import argparse
from itertools import zip_longest


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def split_large_files(filename, number_of_lines_per_file):
    with open(filename) as f:
        for i, g in enumerate(grouper(number_of_lines_per_file, f, fillvalue=''), 1):
            small_filename = '%s_%s' % (filename, format(i * number_of_lines_per_file))
            with open(small_filename, 'w') as fout:
                fout.writelines(g)


if __name__ == "__main__":

    # Parse args
    parser = argparse.ArgumentParser(
        description='Split a large file into many based on a specified number of lines.')
    parser.add_argument(
        dest='input_file',
        action='store',
        help='Input file to be split')
    parser.add_argument(
        dest='number_of_lines_per_file',
        action='store',
        help="Enter the numbert of lines per file.")

    args = parser.parse_args()
    split_large_files(args.input_file, int(args.number_of_lines_per_file))
