# file_converters
File conversion scripts for DNA sequence data  

All the scripts require Python 3  

Help Menus:  
`./<script> -h`  

```
loci2fasta - converts a .loci file from pyRAD to a separate FASTA file for each locus  
loci2phylip - does the same, except it creates a PHYLIP file for each locus  
phylip2fasta - converts a PHYLIP file to a single FASTA file  
phylip2svdq - converts PHYLIP file to NEXUS format with a taxpartition for use with SVDquartets  
multifasta2clades - converts directory of FASTA files to CLADES format  
phylip2onehotsnps - converts PHYLIP file to one-hot SNP format for input to VAE machine learning species delimitation.
vcf2bgc - converts ipyrad VCF file to BGC (Bayesian Genomic Cline) genotype uncertainty format. Currently only works with 3 populations. Also writes locinames to $prefix_loci.txt
```

