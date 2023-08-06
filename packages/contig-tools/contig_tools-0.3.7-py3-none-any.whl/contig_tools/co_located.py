from Bio.Blast.Applications import NcbimakeblastdbCommandline
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast import NCBIXML
import tempfile
import os
import csv
import parmap


def calculate_chunk_size(num_tasks, num_parallel_processes, update_timeline_num = 4):
    """
    calculate the size of the number of tasks to pass in each 'chunk' to each parallele process
    """
    num_chunks, extra = divmod(num_tasks, num_parallel_processes * update_timeline_num)
    if extra:
        num_chunks += 1
    return int(num_chunks)


def parse_genome_file(genome_filepath, query_file, percent_id_threshold):
    """
    This function executes the series of steps necessary to query a genome with the query sequences and
    report matches, co-located or not

    Args:
        genome_filepath (str): Path to a single genome file
        query_file (str): Path to a multi fasta file containing two or more loci that could be co-located
        percent_id_threshold(float): threshold below which hits will not be reported

    Returns:
        tuple: first item is genome file prefix, second item are the parsed genome result metrics
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        blast_database_path = make_blast_database(genome_filepath, f'{tmpdirname}/blast_database')
        blast_result_path = blast_search(query_file, blast_database_path, tmpdirname)
        parsed_blast_result = parse_blast(blast_result_path, percent_id_threshold)
        genome_prefix = os.path.splitext(os.path.basename(genome_filepath))[0]
        return (genome_prefix, parsed_blast_result)


def find_co_located(query_file, output_file, percent_id_threshold, genome_file=None, genome_file_list=None, num_parallel_processes=1, write_only_co_located=False):
    """
    Function to find co located loci on one or more genomes

    Args:
        query_file (str): Path to a multi fasta file containing two or more loci that could be co-located
        output_file(str): path to file where the results will be written
        percent_id_threshold(float): threshold below which hits will not be reported
        genome_file (str): Path to a single genome file
        genome_file_list (str): Path to a text file with one or more genome filepaths. 1 / line
        num_parallel_processes (int): number of parallel processes to run
        write_only_co_located (boolean): whether to write to the output file just those genomes where the queries are colocated
    """
    if genome_file:
        genome_files = [genome_file]
    else:
        with open(genome_file_list) as f:
            genome_files = [line.strip() for line in f.readlines()]
    
    chunksize = calculate_chunk_size(len(genome_files), num_parallel_processes)

    parsed_blast_results = parmap.map(parse_genome_file,
                                      genome_files,
                                      query_file,
                                      percent_id_threshold,
                                      pm_processes=num_parallel_processes,
                                      pm_chunksize=chunksize,
                                      pm_pbar=True)
    parsed_blast_results_dict = { genome:result for (genome,result) in parsed_blast_results }

    write_result_table(parsed_blast_results_dict, output_file, write_only_co_located)



def make_blast_database(genome_file, outdir):
    """
    function to make blast database
    Args:
        genome_file (str): Path to a genome file from which the database will be made
        outdir (str): Path to where the blast database will be created including the database prefix
    
    Returns:
        str: path to the blast database, including prefix
    """
    cmd = NcbimakeblastdbCommandline(dbtype="nucl",
                                     input_file=genome_file,
                                     title='genome',
                                     out=outdir )
    cmd()
    return(outdir)
    
def blast_search(query_seq, blast_database, outdir, evalue=0.001):
    """
    Perform a blast search. The result will be written to an xml file in blast 5 format
    Args:
        query_seq (str): path to a query sequence
        blast_database (str): path to the blast database including prefix
        outdir (str): path to directory where the blast_result.xml file will be written
        evalue (float): the expect value (e) use for setting a threshold of which hits to report
    
    Return:
        str path to the blast result file
    """
    cmd = NcbiblastnCommandline(query=query_seq,
                                db=blast_database,
                                evalue=0.001,
                                out=f'{outdir}/blast_result.xml',
                                dust='no',
                                soft_masking='false',
                                outfmt=5)
    cmd()
    return(f'{outdir}/blast_result.xml')
    
def parse_blast(blast_output, percent_id_threshold = 95):
    """
    Parses a blast result with one or more records and reports metrics on hots that have a percent
    identity match equal to or greater than the percent_id_threshold
    Args:
        blast_output (str): path to a blast result file in blast 5 XML format
        percent_id_threshold(float): threshold below which hits will not be reported
    
    Returns:
        list: A list of blast metrics (one per record corresponding to each query) where the items are dicts with keys
        query, subject, subject_start, subject_end, percent_id
    """ 
    metrics = []
    with open(blast_output) as result_handle:
        blast_records = NCBIXML.parse(result_handle)
        for blast_record in blast_records:
            result_metrics = {'query': blast_record.query}
            if len(blast_record.alignments) > 0:
                alignment_metrics = get_alignment_metrics(blast_record.alignments[0])
                # test percent_id threshold
                alignment_length = alignment_metrics['subject_end'] - alignment_metrics['subject_start'] + 1
                percent_id = alignment_metrics['identities']/alignment_length*100
                if percent_id >= percent_id_threshold:
                    alignment_metrics['percent_id'] = round(percent_id,1)
                    del alignment_metrics['identities']
                    result_metrics.update(alignment_metrics)
            else:
                result_metrics.update({
                    'subject': 'NA',
                    'subject_start': 'NA',
                    'subject_end': 'NA',
                    'percent_id': 'NA',
                })

            metrics.append(result_metrics)
    return(metrics)


def get_alignment_metrics(alignment):
    """
    method to return alignment metrics
    Args:
    alignment (Bio.Blast.Record.Alignment): An alignment object

    Returns:
        dict: Dictionary of metrics with keys subject, identities, subject_start, subject_end
    """
    title = alignment.title.split(" ")[1]
    identities = sum([hsp.identities for hsp in alignment.hsps])
    subject_starts = [hsp.sbjct_start for hsp in alignment.hsps]
    subject_ends = [hsp.sbjct_end for hsp in alignment.hsps]
    
    subject_positions = subject_starts
    subject_positions.extend(subject_ends)
    subject_start = min(subject_positions)
    subject_end = max(subject_positions)
    return({"subject": title,
            "identities": identities,
            "subject_start": subject_start,
            "subject_end": subject_end})

    
def write_result_table(genome_results, output_file, write_only_co_located = False):
    """
    method to write genome_results data to table
    Args:
        genome_results (list): A list of genome results. Each item contains a lits of dicts with blast metrics for each query
        output_file (str): path to file where the results will be written
        write_only_co_located (bolean): whether to write to the output file just those genomes where the queries are colocated
    """
    with open(output_file, 'w') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        # make field names based on the first item
        first_genome = list(genome_results.keys())[0]
        fieldnames = ['genome', 'co-located']
        fieldnames.extend([f'{key}_{index+1}' for index, result in enumerate(genome_results[first_genome]) for key in result.keys()])
        csv_writer.writerow(fieldnames)
        # write each result out
        for genome, genome_result in genome_results.items():

            values = [value for result in genome_result for value in result.values()]
            hit_subjects = [result['subject'] for result in genome_result]
            # add co-location result
            if len(set(hit_subjects)) == 1 and set(hit_subjects) != set(['NA']):
                row_items = [genome, 'Y'] # co-located
                row_items.extend(values)
                csv_writer.writerow(row_items)
            elif not write_only_co_located:
                row_items = [genome, 'N'] # not co-located
                row_items.extend(values)
                csv_writer.writerow(row_items)
    