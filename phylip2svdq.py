#!/usr/bin/env python3

import argparse

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
        
def get_unique_identifiers(pattern, hit, number, sample_number, end):

    if not hit:
        hit[pattern] = number
    
    if pattern not in hit:
        number += 1
        hit[pattern] = number
        end = sample_number-1
        return end, sample_number
    else:
        return end, sample_number
    
def write_taxblock(pattern, outfile, tpl):

    outfile.write("\t\t{}\t:  {}-{},\n".format(pattern, tpl[0], tpl[1]))
   
    
##########################################################################################################################################
##############################################################MAIN########################################################################
##########################################################################################################################################
    
arguments = Get_Arguments()

check_if_exists(arguments.phylip)

samples = dict()
unique_ids = dict()

popnum = 1

sample_number = 1

ranges = ()
range_begin = 1




with open(arguments.phylip, "r") as fin:
    with open(arguments.nexus, "w") as fout:
        
        header = fin.readline()
        
        dimensions = header.split()
        
        samples = read_phylip(fin)
                     
        write_nexus(samples, fout, dimensions)

        line1 = "\nbegin sets;"
        line2 = "\ttaxpartition popmap ="
        fout.write("{}\n{}\n".format(line1, line2))
        
        previous_patt = list(sorted(samples.keys()))[0][arguments.start-1:arguments.end]
        
        final_patt = list(sorted(samples.keys()))[-1][arguments.start-1:arguments.end]
        
        for k in sorted(samples.keys()):
            range_end = 0
            
            
            patt = k[arguments.start-1:arguments.end]
                    
            range_end, sample_number = get_unique_identifiers(patt, unique_ids, popnum, sample_number, range_end)  # Returns popID and adds 1 for each unique ID
            
            sample_number += 1
            
            if range_end > 0:
                ranges = (range_begin, range_end)
                range_begin = range_end+1
                write_taxblock(previous_patt, fout, ranges)
                previous_patt = patt
        
        
        fout.write("\t\t{}\t:  {}-{};\n".format(final_patt, range_begin, sample_number-1))
        fout.write("end;\n")
        
                        
                    
        