# Contig Tools
## Installation
```
pip3 install contig-tools
```

source code: https://gitlab.com/antunderwood/contig_tools

## Usage
```
usage: contig-tools [-h] [-v] {filter,metrics,check_metrics} ...

A package to maniuplate and assess contigs arising from de novo assemblies


positional arguments:
  {filter,metrics,check_metrics}
                        The following commands are available. Type
                        contig_tools <COMMAND> -h for more help on a specific
                        commands
    filter              Filter contigs based on either length and/or coverage
    metrics             Print contig metrics
    check_metrics       check contig metrics

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         display the version number
```

## Examples
### filter contigs

```
contig-tools filter -l 500 -c 3 -f contigs.fasta
```

### print contig metrics

```
contig-tools metrics -f contig_tools/tests/test_data/contigs_for_checks.fas
contig-tools metrics -f contig_tools/tests/test_data/contigs_for_checks.fas -o json
```
### check if contigs meet conditions based on conditions enoded in a yaml file

example yaml file
```
N50 score:
  condition_type: gt
  condition_value: 10
Largest contig:
  condition_type: gt
  condition_value: 15
Total length:
  condition_type: lt_gt
  condition_value:
    - 100
    - 50
```
example command
```
contig-tools check_metrics -f contigs.fasta -y conditions.yml
```
metrics that can be checked are
 - Number of contigs
 - Number of contigs > 500bp
 - Total length
 - %GC
 - Largest contig
 - N50 score

 conditions that can be used are 
 - gt => greater than
 - lt => less than
 - lt_gt => less than and greater than

### check if a two or more loci are co-located

Make a fasta query file with the 2 or more loci you want to see if they are co-located e.g
```
>gene1
GCAGCTAGCGACTGCGAC.....
>gene2
CTACGTAGGACACGACTA....
```

There are two options

1. Search a single genome file for the co-location of loci

    ```
    contig-tools co_located -q queries.fas -f /path/to/single/genome/contigs.fas
    ```
or

2. Search a list of genomes for the co-location of loci
  Make a text file with paths to genomes e.g
  
    ```
    /path/to/single/genome1.fas
    /path/to/single/genome1.fas
    ....
    ```

    and then run the command
    ```
    contig-tools co_located -q queries.fas -l /path/to/single/genome_list_file.txt
    ```

    If you have muliple cores on the computer you are running this on you can process the search in parallel using the `-n <NUMBER PARALLEL PROCESSES>`.

    If you only want to write out genomes where the queries are co-located use the `-y` options
## code
Code can be found [here](https://gitlab.com/antunderwood/contig_tools)