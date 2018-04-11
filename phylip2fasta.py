#!/usr/bin/env python3

import argparse
import os
import errno
import sys

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="Converts Phylip file to FASTA format")

    parser.add_argument("-p", "--phylip", type=str, required=True, help=".phy input filename")
    parser.add_argument("-f", "--fasta", type=str, required=False,
                        help="Output filename; Default = out.fas", nargs="?", default="out.fas")
    
    args = parser.parse_args()

    return args

def check_if_exists(filename):

    try:
        file = open(filename, "r")
    except IOError:
        print("\nError: The file " + filename + " does not exist.\n")
        sys.exit(1)

def read_phylip(file):
    
    loci = dict()
    for line in file:
        line = line.rstrip()
        id_seq = line.strip().split()
        loci[id_seq[0]] = id_seq[1]

    return loci
       
def writeFasta(dict, ofile):
    
   for k, v in dict.items():
        ofile.write(">" + str(k) + "\n" + str(v) + "\n")
    
##########################################################################################################################################
##############################################################MAIN########################################################################

arguments = Get_Arguments()

check_if_exists(arguments.phylip)

samples = dict()

with open(arguments.phylip, "r") as fin:
    with open(arguments.fasta, "w") as fout:
    
        header = fin.readline()
        
        samples = read_phylip(fin)
        
        writeFasta(samples, fout)
