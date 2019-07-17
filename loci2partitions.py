#!/usr/bin/env python3

import argparse
import sys

<<<<<<< HEAD
def main():

=======

def main():
>>>>>>> 0b5b1ca206309a823ef3ea043d06c2ae6977d166

    arguments = Get_Arguments()

    check_if_exists(arguments.loci)

    locus_num = 0
<<<<<<< HEAD
    site_pos = 1
    length_part = set()
=======
    ind_count = 0
    site_pos = 1
    length_part = set()
    length_list = list()
    ind_count_list = list()
    loc_list = list()
>>>>>>> 0b5b1ca206309a823ef3ea043d06c2ae6977d166

    nexus = str(arguments.out) + ".nex"
    partitions = str(arguments.out) + ".partitions"

    with open(arguments.loci, "r") as fin:
        with open(nexus, "w") as nex:
            nex.write("#nexus\n")
            nex.write("begin sets;\n")

            with open(partitions, "w") as part:

            # Call generator function on input .loci file
            # Output is a NEXUS and RAxML-style partition input file.
<<<<<<< HEAD
                for lcount, slen, total_len in locusGenerator(fin, locus_num):
                    upper_bound = write_nexpartition(nex, lcount, slen, site_pos)
                    write_partitions(part, lcount, slen, site_pos, upper_bound)
                    site_pos += slen
                print(sum(total_len))
                nex.write("end;\n")

=======
                for locus, lcount, slen, ind_count in locusGenerator(fin, locus_num, length_part, ind_count):

                    loc_list.append(locus)
                    upper_bound = write_nexpartition(nex, lcount, slen, site_pos)
                    write_partitions(part, lcount, slen, site_pos, upper_bound)
                    length_list.append(slen)
                    site_pos += slen

            nex.write("end;\n")

                # Get all keys in list of dictionaries.
    all_keys = set().union(*(d.keys() for d in loc_list))
    #print(all_keys)

    concatenate_alignments(all_keys, loc_list, length_list)
    #print(length_list)


    return 0
>>>>>>> 0b5b1ca206309a823ef3ea043d06c2ae6977d166

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

def locusGenerator(file, locus_count, length_part, ind_count):

    locus = dict()

<<<<<<< HEAD
    length_set = set()
    length_list = list()
    total_length = 0
=======
>>>>>>> 0b5b1ca206309a823ef3ea043d06c2ae6977d166
    for line in file:
        line = line.strip()
        lines = line.split()

        if line.startswith("//"):
            temp_locus = locus.copy()
            locus.clear()

            locus_count += 1
<<<<<<< HEAD
            if len(length_set) > 1:
                print("Unequal lengths: " + str(length_set))
                length_set.clear()
                length_list.append(seq_len)
                yield locus_count, seq_len, length_list
            else:
                length_set.clear()
                length_list.append(seq_len)
                yield locus_count, seq_len, length_list
=======

            if len(length_part) > 1:
                print("Warning: Unequal sequence lengths at locus " + \
                str(locus_count) + "\n")

            length_part.clear()

            yield temp_locus, locus_count, seq_len, ind_count
>>>>>>> 0b5b1ca206309a823ef3ea043d06c2ae6977d166

        elif line and \
        (line[0].isalpha() or \
        line[0].isdigit() or \
        line[0].startswith(">")):
            locus[lines[0]] = lines[1]
            ind_count += 1
            seq_len = len(lines[1])
<<<<<<< HEAD
            length_set.add(seq_len)
=======
            length_part.add(seq_len)

>>>>>>> 0b5b1ca206309a823ef3ea043d06c2ae6977d166

def write_nexpartition(fout, loc_count, seqlen, site_pos):

    upper_site_bound = (site_pos + seqlen - 1)
    fout.write("\tcharset part" + str(loc_count) + " = " + str(site_pos) + "-" + \
                str(upper_site_bound) + ";\n")

    return upper_site_bound

def write_partitions(fout, loc_count, seqlen, site_pos, upper_site_bound):

    fout.write("DNA, part" + str(loc_count) + " = " + str(site_pos) + "-" + \
                str(upper_site_bound) + ";\n")

def concatenate_alignments(all_keys, list_of_dicts, slen):

<<<<<<< HEAD
if __name__ == "__main__":

=======

    sorted_keys = sorted(all_keys)
    #print(len(all_keys))
    for k in sorted_keys:
        merged = "".join(d.get(k, "N" * len( for d in list_of_dicts)

        print(k + "\t" + str(merged))

    for d in range(len(list_of_dicts)):
        concat = dict()
        for k in sorted_keys:
            #print(slen[d])
            missing = "N"
            missing_len = missing * slen[d]
            seqs = list_of_dicts[d].get(k, missing_len)
            concat[k] = seqs
            #$print(k + "\t")

            "".join(concat[k])
        #for k in concat.keys():
            #print(concat[k])
            #print(k, concat[k])
            #print(joined)
    #for k in sorted_keys:
        #joined = "".join(str(concat[x]) for x in sorted(list_of_dicts[d]))

        #print(joined)
    #print(test)
            #d.get(k, default)

    #for i in sorted_keys:
    #for d in list_of_dicts:
        #if

##########################################################################################################################################
##############################################################MAIN########################################################################

if __name__ == "__main__":

>>>>>>> 0b5b1ca206309a823ef3ea043d06c2ae6977d166
    rtrn_code = main()
    print("Program finished with exit status " + str(rtrn_code) + "\n")
    sys.exit(rtrn_code)
