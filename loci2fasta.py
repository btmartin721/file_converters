#!/usr/bin/env python3

import argparse
import os
import errno
import sys

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="each locus in a .loci file from pyRAD is output to a separate FASTA file")

    parser.add_argument("-L", "--loci", type=str, required=True, help=".loci input filename")
    
    args = parser.parse_args()

    return args

def check_if_exists(filename):

    try:
        file = open(filename, "r")
    except IOError:
        print("\nError: The file " + filename + " does not exist.\n")
        sys.exit(1)

def locusGenerator(file, locus_count):

    locus = dict()
    
    for line in fin:
        line = line.rstrip().strip()
        lines = line.split()
        
        if line.startswith(">"):
            locus[lines[0]] = lines[1]
            
        elif line.startswith("//"):
            locus_count += 1
            yield locus, locus_count
            locus = dict()
            
def writeFasta(alignment, fout):

    for k, v in alignment.items():
        fout.write(str(k) + "\n" + str(v) + "\n")

# Makes subdirectory for outfiles
def makeLociDir(directory):
    
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
##########################################################################################################################################
##############################################################MAIN########################################################################

arguments = Get_Arguments()

check_if_exists(arguments.loci)

locus_num = 0
dir = "loci"

# Makes subdirectory called loci
makeLociDir(dir)

with open(arguments.loci, "r") as fin:

        # Call generator function on input .loci file
        # Output is a dictionary (sampleID: sequence) that is cleared and replaced for each locus
        for aln, lcount in locusGenerator(fin, locus_num):
        
            # makes outfile names for each locus
            OF = ("locus" + str(lcount) + ".fasta")
            
            # Writes each locus as a separate FASTA file into ./loci/*.fasta
            with open(os.path.join(dir, OF), "w") as fout:
                writeFasta(aln, fout)
