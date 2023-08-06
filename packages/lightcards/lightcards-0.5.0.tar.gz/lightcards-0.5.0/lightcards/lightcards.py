# Markdown flashcard utility
# Armaan Bhojwani 2021

import argparse
from curses import wrapper
import os
from random import shuffle
import sys

from . import parse, progress
from .display import Display
from .deck import Status


def parse_args():
    parser = argparse.ArgumentParser(
        description="Terminal flashcards from Markdown")
    parser.add_argument("inp",
                        metavar="input file",
                        type=str,
                        nargs=1)
    parser.add_argument("-a", "--alphabetize",
                        action='store_true',
                        help="alphabetize card order")
    parser.add_argument("-f", "--flip",
                        action='store_true',
                        help="show second column first")
    parser.add_argument("-p", "--purge",
                        action='store_true',
                        help="don't check cached info before starting")
    # TODO: don't require input file when using  -P
    parser.add_argument("-P", "--purge-all",
                        action='store_true',
                        help="don't check cached info before starting")
    parser.add_argument("-r", "--reverse",
                        action='store_true',
                        help="reverse card order")
    parser.add_argument("-s", "--shuffle",
                        action='store_true',
                        help="shuffle card order")
    parser.add_argument("-v", "--version",
                        action='version',
                        version="lightcards 0.5.0")
    return parser.parse_args()


def show(args, stack, headers):
    """
    Get objects from cache, manipulate deck according to passed arguments, and
    send it to the display functions
    """
    # Purge caches if asked
    if args.purge:
        progress.purge(stack)
    if args.purge_all:
        progress.purge_all()

    # Check for caches
    idx = Status()
    cache = progress.dive(get_orig())
    if cache:
        (stack) = cache

    # Manipulate deck
    if args.shuffle:
        shuffle(stack)
    if args.alphabetize:
        stack.sort()
    if args.reverse:
        stack.reverse()
    if args.flip:
        for x in stack:
            x[0], x[1] = x[1], x[0]
        headers[0], headers[1] = headers[1], headers[0]

    # Send to display
    win = Display(stack, headers, idx)
    wrapper(win.run)


def reparse():
    """Parse arguments and input file again"""
    args = parse_args()
    os.system(f"$EDITOR {args.inp[0]}"),
    return parse.parse_html(parse.md2html(args.inp[0]))


def get_orig():
    """Return original header and stack"""
    return((headers, stack))


def main(args=sys.argv):
    args = parse_args()
    global headers, stack
    (headers, stack) = parse.parse_html(parse.md2html(args.inp[0]))
    show(args, stack, headers)


if __name__ == "__main__":
    main()
