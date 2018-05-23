#!/usr/bin/env python3

import argparse

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="Converts Phylip file to FASTA format")

    parser.add_argument("-p", "--phylip", type=str, required=True, help="PHYLIP input filename")
    parser.add_argument("-n", "--nexus", type=str, required=False,
                        help="NEXUS output filename; Default = out.nex", nargs="?", default="out.nex")
    
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
    
def write_nexus(dict, ofile, dimensions):

    line1 = "#NEXUS"
    line2 = "BEGIN DATA;"
    line3 = "DIMENSIONS NTAX=" + dimensions[0] + " NCHAR=" + dimensions[1] + ";"
    line4 = "FORMAT DATATYPE=DNA MISSING=N GAP=- INTERLEAVE=YES;"
    line5 = "MATRIX"
    colon = ";"
    end = "END"
    
    ofile.write("{}\n{}\n{}\n{}\n{}\n".format(line1, line2, line3, line4, line5))
    
    for k, v in dict.items():
        ofile.write("{}\t{:>15}\n".format(str(k), str(v)))
    
    ofile.write("{}\n{}\n".format(colon, end))
        
    
        
##########################################################################################################################################
##############################################################MAIN########################################################################
##########################################################################################################################################
    
arguments = Get_Arguments()

check_if_exists(arguments.phylip)

samples = dict()

with open(arguments.phylip, "r") as fin:
    with open(arguments.nexus, "w") as fout:
    
        header = fin.readline()
        
        dimensions = header.split()
        
        samples = read_phylip(fin)
        
        write_nexus(samples, fout, dimensions)