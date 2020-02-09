#!/usr/bin/env python

# Script written by Bradley T. Martin, PhD Candidate, University of Arkansas.
# Please report any issues or bugs to btm002@email.uark.edu

import argparse # parse command-line arguments.
import os # needed for listing directory of fasta files.
import sys # used for exiting if conditions not met.

from Bio import AlignIO # to read fasta files.

def main():

    args = Get_Arguments() # uses argparse.
    popmap = read_popmap(args.popmap)
    indcount = len(popmap)

    with open(args.outfile, "w") as fout:
        fout.write("\n\n") # Write two empty lines at beginning of file.

    for filename in os.listdir(args.dir):
        fas = read_fasta(filename, args.dir) # Uses biopython AlignIO
        alnLen = fas.get_alignment_length() # Gets max length of each alignment
        ninds = len(fas) # Gets number of sequences
        header = "{} {}".format(indcount, alnLen) # Make header for each locus.
        indlist = list()
        with open(args.outfile, "a") as fout:
            fout.write(header + "\n")

            # If present in popmap: get list of individuals
            new_popmap = {k.id: popmap[k.id] for k in fas if k.id in popmap}
            ind_id_list = [record.id for record in fas]

            # For finding individual missing from alignment
            missing_inds = dict()
            for k, v in popmap.items():
                if k not in ind_id_list:
                    missing_inds[k] = v
            indlist = list(("{}^{}".format(key, value) for key, value in new_popmap.items()))

            missing_ind_list = list(("{}^{}".format(key, value) for key, value in missing_inds.items()))

            # Makes new dictionary in format of ind1^pop1
            new_fasta_dict = dict()
            for ind in indlist:
                first = ind.split("^")
                for record in fas:
                    if first[0] == record.id:
                        new_fasta_dict[ind] = str(record.seq)

            # Write all dashes for missing indivuals. length = alnLen
            missing_seq = repeat_to_length("-", alnLen)
            missing_dict = {k: missing_seq for k in missing_ind_list}

            # Add individuals with all missing data to dictionary
            new_fasta_dict.update(missing_dict)

            for key in sorted(new_fasta_dict):
                fout.write("{}\t{}\n".format(key, new_fasta_dict[key]))
            fout.write("\n\n")


def repeat_to_length(string_to_expand, length):
   return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def read_popmap(filename):
    """
    Function to read a two-column tab-separated file and save the first column as dictionary keys and second as values.
    Input: filename
    Returns: dictionary[col1] = col2.
    """
    mydict = dict()
    with open(filename, "r") as fin:
        for line in fin: # Read file line by line.
            line = line.strip()
            if not line:
                continue
            cols = line.split()
            mydict[cols[0]] = cols[1] # Make dictionary from popmap.
    return mydict

def read_fasta(filename, mydir):
    """
    Reads fasta file using biopython's AlignIO.
        Used in generator with directory of fasta files.
        Inputs: filename, directory of input files.
        Returns: file contents.
    """
    # Remove forward slash if present.
    if mydir.endswith("/"):
        mydir = mydir[:-1]
    mypath = str(mydir) + "/" + str(filename)
    file = AlignIO.read(open(mypath), 'fasta') # from biopython
    return file

def Get_Arguments():
    """
    Parse command-line arguments. Imported with argparse.
    Returns: object of command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Converts directory of FASTA files to input file for CLADES for species delimitation", add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    ## Required Arguments
    required_args.add_argument("-d", "--dir",
                                type=str,
                                required=True,
                                help="Specify directory containing only input FASTA files.")
    required_args.add_argument("-o", "--outfile",
                                type=str,
                                required=True,
                                help="String; Specify output CLADES filename")
    required_args.add_argument("-p", "--popmap",
                                type=str,
                                required=True,
                                help="String; Specify two-column tab-delimited popmap file: IndID\tPopID; no header line.")


    optional_args.add_argument("-h", "--help",
                                action="help",
                                help="Displays this help menu")

    # If no arguments specified print help and die.
    if len(sys.argv)==1:
        print("\nExiting because no command-line options were called.\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
