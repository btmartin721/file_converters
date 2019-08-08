#!/usr/bin/env python3

import argparse
import sys

def main():

    args = Get_Arguments()

    ind, pop, seq = read_phylip(args.input)

    my_encodings = {
		"A" : "1.0,0.0,0.0,0.0",
		"C" : "0.0,1.0,0.0,0.0",
        "G" : "0.0,0.0,1.0,0.0",
        "T" : "0.0,0.0,0.0,1.0",
        "R" : "0.5,0.0,0.5,0.0",
        "Y" : "0.0,0.5,0.0,0.5",
        "S" : "0.0,0.5,0.5,0.0",
        "W" : "0.5,0.0,0.0,0.5",
        "K" : "0.0,0.0,0.5,0.5",
        "M" : "0.5,0.5,0.0,0.0",
        "N" : "0.0,0.0,0.0,0.0",
        "-" : "0.0,0.0,0.0,0.0"
	}

    onehot_list = sub_encodings(seq, my_encodings)

    write_output(onehot_list, args.outfile, ind, pop)


def write_output(my_list, outfile, inds, pops):
    with open(outfile, "w") as fout:
        for l in range(len(my_list)):
            fout.write(str(inds[l]) + " " + str(pops[l]) + " " + my_list[l] + "\n")


def sub_encodings(seqs, codes):
    onehot = list()
    for l in seqs:
        temponehot = list()
        tmplist = list(l)
        for j in tmplist:
            if j in codes:
                temponehot.append(codes[j])
            else:
                print("Error: Unknown base '{}' could not be converted to one-hot format; terminating program.".format(j))
        onehot.append(" ".join(temponehot))

    return onehot

def read_phylip(file):
    ind_ids = list()
    pop_ids = list()
    seqs = list()
    with open(file, "r") as fin:
        next(fin)
        for line in fin:
            line = line.strip()
            cols = line.split()
            ind_ids.append(cols[0])
            pop_ids.append(cols[1])
            seqs.append(cols[2])

    return ind_ids, pop_ids, seqs



def Get_Arguments():
    """
    Parse command-line arguments. Imported with argparse.
    Returns: object of command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Converts PHYLIP to one-hot encoding for input to VAE species delimitation", add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    ## Required Arguments
    required_args.add_argument("-i", "--input",
                                type=str,
                                required=True,
                                help="String; Input PHYLIP file with popmap as column 2")
    required_args.add_argument("-o", "--outfile",
                                type=str,
                                required=True,
                                help="String; Specify output filename")


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
