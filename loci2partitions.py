#!/usr/bin/env python3

import argparse
import sys

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="Script to make NEXUS and "
                                                 " RAxML-style partitions files "
                                                 "from pyRAD/ipyrad .loci file ")

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument("-l", "--loci", type=str,
                                        required=True,
                                        help=".loci input filename")
    parser.add_argument("-o", "--out", type=str,
                                        required=False,
                                        nargs="?",
                                        default="out",
                                        help="Prefix for output files")
    args = parser.parse_args()

    return args

def check_if_exists(filename):

    try:
        file = open(filename, "r")
    except IOError:
        print("\nError: The file " + filename + " does not exist.\n")
        sys.exit(1)

def locusGenerator(file, locus_count):

    for line in fin:
        line = line.strip()
        lines = line.split()

        if line.startswith("//"):
            locus_count += 1
            yield locus_count, seq_len

        elif line and \
        (line[0].isalpha() or \
        line[0].isdigit() or \
        line[0].startswith(">")):
            seq_len = len(lines[1])

def write_nexpartition(fout, loc_count, seqlen, site_pos):

    upper_site_bound = (site_pos + seqlen - 1)
    fout.write("\tcharset part" + str(loc_count) + " = " + str(site_pos) + "-" + \
                str(upper_site_bound) + ";\n")

    return upper_site_bound

def write_partitions(fout, loc_count, seqlen, site_pos, upper_site_bound):

    fout.write("DNA, part" + str(loc_count) + " = " + str(site_pos) + "-" + \
                str(upper_site_bound) + ";\n")

##########################################################################################################################################
##############################################################MAIN########################################################################

arguments = Get_Arguments()

check_if_exists(arguments.loci)

locus_num = 0
site_pos = 1
length_part = set()

nexus = str(arguments.out) + ".nex"
partitions = str(arguments.out) + ".partitions"

with open(arguments.loci, "r") as fin:
    with open(nexus, "w") as nex:
        nex.write("#nexus\n")
        nex.write("begin sets;\n")

        with open(partitions, "w") as part:

        # Call generator function on input .loci file
        # Output is a NEXUS and RAxML-style partition input file.
            for lcount, slen in locusGenerator(fin, locus_num):
                upper_bound = write_nexpartition(nex, lcount, slen, site_pos)
                write_partitions(part, lcount, slen, site_pos, upper_bound)
                site_pos += slen

            nex.write("end;\n")
