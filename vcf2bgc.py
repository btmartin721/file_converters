#!/usr/bin/env python

"""
Script to convert VCF files to BGC (Bayesian Genomic Cline) format, using the genotype uncertainties.

Uses the read depth for each allele and each individual
which is output in the ipyrad VCF file.

BGC format looks like this:

Parental population files:

locus_1
22 4
1 21
4 55
33 0
locus_2
33 5
22 3
0 1
0 0

Admixed population files:
locus_1
pop_0
0 0
0 43
33 5
0 33
locus_2
pop_0
22 3
33 5
33 0
0 0


So: the loci contain 4 individuals, and each column represents the read depth
for each allele. Must be bi-allelic data. The admixed file requires a population ID line.

The ipyrad VCF output file contains a column that includes:
GT (Genotype):DP (total reads):CATG (# reads per allele) delimited by a colon.

Dependencies:
    PyVCF (I used version 0.6.8)
"""

# Load necessary modules.
import argparse
import sys
import vcf # PyVCF module


def main():

    # Parse command-line arguments.
    args = Get_Arguments()

    # Read popmap into dictionary. {'indID': 'popID'}
    popmap = read_popmap(args.popmap)
    popsamples = get_samples_by_pop(popmap, args.admixed, args.p1, args.p2)

    # Read VCF using PyVCF module.
    vcf_reader = vcf.Reader(open(args.vcf), "r")

    admix_file = "{}_admixedin.txt".format(args.outprefix)
    p1_file = "{}_p0in.txt".format(args.outprefix)
    p2_file = "{}_p1in.txt".format(args.outprefix)

    # Open file handles.
    admix = open(admix_file, "w")
    p1 = open(p1_file, "w")
    p2 = open(p2_file, "w")

    # For each locus:
    for record in vcf_reader:

        # Get ref and alt alleles.
        ref = record.REF
        alt = record.ALT
        locus = "{}_{}".format(record.CHROM, record.POS)

        # Make sure all sites are bi-allelic. Required for BGC.
        if len(alt) > 1:
            raise ValueError("All SNPs must be bi-allelic. >2 alleles detected for locus {} ...Terminating execution.\n".format(record.CHROM))

        # Get alternate allele. pyvcf has it as a list.
        alt = str(alt[0])

        write_output(record, popsamples, ref, alt, locus, args.outprefix, admix, p1, p2)

    admix.close()
    p1.close()
    p2.close()

def get_allele_depth(record, pop, ref, alt, sampledict):
    """
    Get read depths for each allele of each sample. Should be within for loop.
    Input:
        record: pyvcf reader object.
        pop: Population ID that is dictionary key in sampledict.
        ref: reference allele
        alt: alternate allele.
        sampledict: dict(list) {popID: [inds]}
    """
    possible = ["C", "A", "T", "G"]

    # For each sample:
    result = list()
    for call in record.samples:

        # CallData from PyVCF has depth counts as comma-delimited.
        alleles = call.data[2].split(",")

        # cast depth counts to integers.
        alleles = [int(x) for x in alleles]

        # Make into dict object: {'C': DepthCount, 'A': DC, 'T': DC, 'G': DC}
        allele_depth = dict(zip(possible, alleles))

        try:
            idx = sampledict[pop].index(call.sample)
            result.append("{} {}".format(allele_depth[ref], allele_depth[alt]))
        except:
            continue

    return result


def write_output(record, sampledict, ref, alt, locus, prefix, admix, p1, p2):
    """
    Write to the three output files: admixed, p1, and p2. This function should be within a for loop.
    Input:
        record: pyvcf reader object.
        sampledict: dict(list) {population: [inds]}
        ref: reference allele (string)
        alt: alternate allele (string)
        locus: locus name (string)
        prefix: prefix for output files. Specified by user at command-line
        admix: admixed file handle.
        p1: p1 file handle.
        p2: p2 file handle.
    Returns:
        Writes to three output files.

    """
    # Get possible alleles in order of CATG.
    #print(sampledict["P2"])
    # For each sample: get depth counts.
    admix_output = get_allele_depth(record, "Admixed", ref, alt, sampledict)
    p1_output = get_allele_depth(record, "P1", ref, alt, sampledict)
    p2_output = get_allele_depth(record, "P2", ref, alt, sampledict)

    admix.write("{}\npop0\n".format(locus))
    p1.write("{}\n".format(locus))
    p2.write("{}\n".format(locus))
    #print("{} {}\n".format(allele_depth[ref], allele_depth[alt]))
    for ind in admix_output:
        admix.write("{}\n".format(ind))

    for ind in p1_output:
        p1.write("{}\n".format(ind))

    for ind in p2_output:
        p2.write("{}\n".format(ind))

def get_samples_by_pop(d, admix, p1, p2):
    """
    Finds samples associated with each of the three user-specified populations:
    Input:
        d: popmap dictionary {indids: popids}.
        admix: admixed population string specified by user at command-line.
        p1: p1 population string specified by user at command-line.
        p2: p2 population string specified by user at command-line.
    Returns:
        popdict: dictionary {'Admixed': [inds], 'P1': [inds], 'P2': [inds]}
    """
    popdict = dict()
    admix_inds = list()
    p1_inds = list()
    p2_inds = list()
    for k,v in d.items():
        if str(v) == str(admix):
            admix_inds.append(k)
        elif str(v) == str(p1):
            p1_inds.append(k)
        elif str(v) == str(p2):
            p2_inds.append(k)
    popdict["Admixed"] = admix_inds
    popdict["P1"] = p1_inds
    popdict["P2"] = p2_inds
    return popdict

def read_popmap(filename):
    """
    Read a population map file.
    Input:
        filename: file should be two-columns, tab-separated. IndIDs\tPopIDs. No header.
    Returns:
        results: dict of {indIDs: popIDs}
    """
    results = dict()
    with open(filename, "r") as popfile:
        for line in popfile:
            line = line.strip()
            inds, pops = line.split()
            results[inds] = pops
    return results

def Get_Arguments():
    """
    Parse command-line arguments. Imported with argparse.
    Returns: object of command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Convert VCF file to BGC format (with genotype uncertainties). Currently only handles three populations maximum (P1, P2, and Admixed).", add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    ## Required Arguments
    required_args.add_argument("-v", "--vcf",
                                type=str,
                                required=True,
                                help="Input VCF file")
    required_args.add_argument("-m", "--popmap",
                                type=str,
                                required=True,
                                help="Two-column tab-separated population map file: inds\tpops. No header line.")
    required_args.add_argument("--p1",
                                type=str,
                                required=True,
                                help="Parental population 1")
    required_args.add_argument("--p2",
                                type=str,
                                required=True,
                                help="Parental population 2")
    required_args.add_argument("--admixed",
                                type=str,
                                required=True,
                                help="Admixed population (limit=1 population)")
    optional_args.add_argument("-o", "--outprefix",
                                type=str,
                                required=False,
                                default="bgc",
                                help="Specify output prefix for BGC files.")
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
