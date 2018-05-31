# file_converters
File conversion scripts for DNA sequence data

loci2fasta converts a .loci file from pyRAD to a separate FASTA file for each locus

loci2phylip does the same, except it creates a PHYLIP file for each locus

phylip2fasta converts a PHYLIP file to a single FASTA file

phylip2svdq converts PHYLIP file to NEXUS format with a taxpartition for use with SVDquartets  
phylip2svdq also uses a regex pattern to generate the population IDs  
To set the characters for the popID, use the -s and -e options

Help Menus: ./<script> -h
