#!/usr/bin/env python3

import argparse
import os
import errno
import sys

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="each locus in a .loci file from pyRAD is output to a separate Phylip file")

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
    ind_count = 0
    
    for line in fin:
        line = line.rstrip().strip()
        lines = line.split()
        
        if line.startswith(">"):
            locus[lines[0]] = lines[1]
            ind_count += 1
            seq_len = len(lines[1])
            
        elif line.startswith("//"):
            locus_count += 1
            yield locus, locus_count, ind_count, seq_len
            ind_count = 0
            locus = dict()
            
def writePhylip(alignment, fout, indcount, seqlen):

    fout.write(str(indcount) + " " + str(seqlen) + "\n")
    
    for k, v in alignment.items():
        k = k[1:]
        fout.write(k.ljust(15) + "\t" + str(v) + "\n")

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
        for aln, lcount, icount, slen in locusGenerator(fin, locus_num):
        
            # makes outfile names for each locus
            OF = ("locus" + str(lcount) + ".phy")
            
            # Writes each locus as a separate Phylip file into ./loci/*.phy
            with open(os.path.join(dir, OF), "w") as fout:
                writePhylip(aln, fout, icount, slen)
