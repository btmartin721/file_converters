#!/usr/bin/env python3

import argparse
import errno
import os
import sys

from itertools import chain, islice


def main():

    args = Get_Arguments()
    with open(args.outgroup) as fin:
        outgroup = [line.strip() for line in fin if line.strip()]
        print(outgroup)
    #smallfile = None
    file_large = args.tests

    commandfilename = "compDcommands.txt"
    silentremove(commandfilename) # Remove compDcommands.txt file if exists

    with open(file_large, "r") as f:

        # For line in DFOIL_picked.txt
        for count, line in enumerate(f):
            if not line.strip():
                continue

            cols = line.strip().split()
            compDbase = "compDtest.txt"
            compDtest = "{}.{}".format(count, compDbase)

            # Write tests to separate files
            with open(compDtest, "w") as o:
                cols.reverse()
                o.write("{}\n{}\n".format(" ".join(outgroup), "\n".join(cols)))

            # Write comp-D commands to file.
            with open(commandfilename, "a") as o:
                o.write("compD -i {} -t {} -b {} -l {} -PfH -o {}.out.txt\n".format(args.phylip, compDtest, args.bootstraps, args.sites, count))

    # Split compDcommands.txt into equal chunks
    compD_basefile = "compDcommands"
    with open(commandfilename, "r") as f:
        for i, lines in enumerate(split_bigfile(f, args.lines)):
            file_split = "{}.{}.split.txt".format(compD_basefile, i)
            with open(file_split, "w") as o:
                o.writelines(lines)

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def split_bigfile(iterable, n):
    """Split a large file into equal chunks"""
    iterable = iter(iterable)
    while True:
        yield chain([next(iterable)], islice(iterable, n-1))

def Get_Arguments():
    """
    Parse command-line arguments. Imported with argparse.
    Returns: object of command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Prepares DFOIL_Picker.R output for input into Comp-D", add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    ## Required Arguments
    required_args.add_argument("-t", "--tests",
                                type=str,
                                required=True,
                                help="String; Output from DFOIL_picker.R "
                                    "(space delimited)")
    required_args.add_argument("-o", "--outgroup",
                                type=str,
                                required=True,
                                help="String; Specify file containing outgroup individuals (space delimited)")
    required_args.add_argument("-p", "--phylip",
                                type=str,
                                required=True,
                                help="String; Specify PHYLIP filename")
    required_args.add_argument("-b", "--bootstraps",
                                type=int,
                                required=True,
                                help="Integer; Specify number of bootstrap replicates you're going to use")
    required_args.add_argument("-s", "--sites",
                                type=int,
                                required=True,
                                help="Integer; Specify number of sites in alignment")

    ## Optional Arguments
    ## Call help menu
    optional_args.add_argument("-l", "--lines",
                                type=int,
                                required=False,
                                default=250000,
                                nargs="?",
                                help="Integer; Specify number of lines per split file; DEFAULT=250000")
    optional_args.add_argument("-h", "--help",
                                action="help",
                                help="Displays this help menu")

    if len(sys.argv)==1:
        print("\nExiting because no command-line options were called.\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
