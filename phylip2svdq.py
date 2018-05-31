#!/usr/bin/env python3

import argparse
import operator

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="Converts PHYLIP file to NEXUS format and writes taxpartition block for SVDquartets")

    parser.add_argument("-p", "--phylip", type=str, required=True, help="PHYLIP input filename")
    parser.add_argument("-n", "--nexus", type=str, required=False,
                        help="NEXUS output filename; Default = out.nex", nargs="?", default="out.nex")
    parser.add_argument("-s", "--start", type=int, required=False, nargs="?", default="1",
                        help="Specify first character of sample ID to be used as pattern for taxpart population ID; default=1")
    parser.add_argument("-e", "--end", type=int, required=False, nargs="?", default="4",
                        help="Specify last character of sample ID to be used as pattern for taxpart population ID; default=4")
    
   
    
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
    
def write_first_block(ofile, dimensions):

    line1 = "#NEXUS"
    line2 = "BEGIN DATA;"
    line3 = "DIMENSIONS NTAX=" + dimensions[0] + " NCHAR=" + dimensions[1] + ";"
    line4 = "FORMAT DATATYPE=DNA MISSING=N GAP=- INTERLEAVE=YES;"
    line5 = "MATRIX"
    
    ofile.write("{}\n{}\n{}\n{}\n{}\n".format(line1, line2, line3, line4, line5))
    
        
def get_unique_identifiers(pattern, hit, number, sample_number):

    if not hit and sample_number == 1:
        hit[pattern] = sample_number
        end = 1
        return end, sample_number, hit
    
    if hit and pattern not in hit:
        hit[pattern] = sample_number
        end = sample_number
        return end, sample_number, hit
        
    elif sample_number == last_sample+1:
        end = sample_number-1
        
    else:
        end = 0
        return end, sample_number, hit
    
def write_taxpart(pattern, outfile, range_tupl):
    
    outfile.write("\t\t{}\t:    {}-{},\n".format(str(pattern), str(range_tupl[0]), str(range_tupl[1])))
    
def write_sorted_matrix(samples):

    for k, v in sorted(samples.items(), key=lambda p: p[0][arguments.start-1:arguments.end]):
        fout.write("{}\t{:>15}\n".format(str(k), str(v)))
        
    fout.write(";\nEND;\n\n") 
    
    partline1 = "\nbegin sets;"
    partline2 = "\ttaxpartition popmap ="
    fout.write("{}\n{}\n".format(partline1, partline2))

##########################################################################################################################################
##############################################################MAIN########################################################################
##########################################################################################################################################
    
arguments = Get_Arguments()

check_if_exists(arguments.phylip)

samples = dict()
unique_ids = dict()

popnum = 1
sample_number = 1
range_begin = 1

with open(arguments.phylip, "r") as fin:
    with open(arguments.nexus, "w") as fout:
        
        header = fin.readline()
        
        dimensions = header.split()
        last_sample = int(dimensions[0])

        samples = read_phylip(fin)
                     
        write_first_block(fout, dimensions)
        write_sorted_matrix(samples)
        
        previous_patt = list(sorted(samples.keys()))[0][arguments.start-1:arguments.end]
        final_patt = list(sorted(samples.keys()))[-1][arguments.start-1:arguments.end]        
        
        #Sorts dictionary by pattern specified by -s and -e options
        for k, v in sorted(samples.items(), key=lambda p: p[0][arguments.start-1:arguments.end]):
            
            # Current pattern iteration
            patt = k[arguments.start-1:arguments.end]
            
            # Returns popID dictionary and adds 1 for each unique ID
            # Also returns number of last entry of each popID: 0 if 
            range_end, sample_number, unique_ids = get_unique_identifiers(patt, unique_ids, popnum, sample_number)
            
            sample_number += 1
            
            # If new unique pattern is found, get sample ranges for previous pattern:
            if range_end > 1 and range_end < last_sample+1:
                patt_range = (range_begin, range_end-1)
                range_begin = range_end
                write_taxpart(previous_patt, fout, patt_range)

                previous_patt = patt
            
            # If last pattern:
            if sample_number == last_sample+1:
                patt_range = (range_begin, last_sample)
                fout.write("\t\t{}\t:    {}-{};\n".format(str(patt), str(patt_range[0]), str(patt_range[1])))

        fout.write("end;\n")
