# -*- coding: utf-8 -*-

"""Contains generic functions used by FRAG"""
import gzip
from multiprocessing import Pool
from functools import partial
from collections import defaultdict
import os
import sys
import ahocorasick
from frags import read

def write_header(output_file, sep="\t"):
    """ Write header of CSV output files

    :param output_file: CSV file to write in
    :type output_file: str
    :param sep: Separator to use between CSV columns
    :type sep: char
     """
    output_file.write("Read_header{0}"\
                      "Reverse_complement{0}"\
                      "Number_of_breakpoints{0}"\
                      "Breakpoints_positions{0}"\
                      "Matches_read_positions{0}"\
                      "Matches_ref_positions{0}"\
                      "Matches_size{0}"\
                      "Insertions{0}"\
                      "Blast_results_breakpoints\n".format(sep))

def get_reference(input_file):
    """ Get the reference genome in one-string.
        Only take the first sequence of the file.
        Can be fasta or fastq, gzipped or not.

    :param input_file: fasta/fastq file to use as reference
    :type input_file: str
    """
    # The reference that will be returned
    ref = ""
    # Is it a GZIP file?
    test_file = open(input_file, "rb")
    # Get the first values
    magic = test_file.read(2)
    # Close the file
    test_file.close()
    # Open the file, GZIP or not
    with (gzip.open(input_file, "rt") if magic == b"\x1f\x8b"
          else open(input_file)) as in_file:
        # Get the first char to determine the type of file
        first_char = in_file.read(1)
        # Ignore header
        next(in_file)
        # Fasta file, can be multi-line
        if first_char == ">":
            # First line
            tmp_line = in_file.readline().strip()
            while tmp_line and not tmp_line.startswith(">"):
                ref += tmp_line
                tmp_line = in_file.readline().strip()
        # Fastq file
        elif first_char == "@":
            # Get the second line only
            ref = in_file.readline().strip()
        else:
            print("File error: enable to understand type of file {} "\
                  "({})".format(input_file, first_char))
            sys.exit(1)

    # Return the ref as a single string
    return ref

def next_read(file, offset_start, offset_end):
    """ Return each sequence between offsets range of a file
        as a tuple (header, seq) using a generator.
        Can be fasta or fastq, gzipped or not.
        WARNING: spaces in headers are replaced by _

    :param file: fasta/fastq file to read
    :param offset_start: offset in the file from where to read
    :param offset_end: offset in the file until where to read
    :type file: str
    :type offset_start: int
    :type offset_end: int
    """
    # Is it a GZIP file?
    test_file = open(file, "rb")
    # Get the first values
    magic = test_file.read(2)
    # Close the file
    test_file.close()

    # Open the file, GZIP or not
    with (gzip.open(file, "rb") if magic == b"\x1f\x8b"
          else open(file, "rb")) as in_file:
        first_line = in_file.readline().decode('utf-8')
        # FASTQ file
        if first_line.startswith("@"):
            # Go to starting offset
            in_file.seek(offset_start)
            # Set current offset
            beg_line_offset = offset_start
            # Read each line from this point
            for line in in_file:
                # Consider this line as a header
                header = line.decode('utf-8').strip()
                # It is a proper fastq header
                if header.startswith("@"):
                    # The beginning of header is in the offset range
                    if beg_line_offset < offset_end:
                        # Get the sequence
                        sequence = in_file.readline().decode('utf-8').strip()
                        # Skip the two next lines
                        in_file.readline()
                        in_file.readline()
                        # Return header and sequence and wait for the next one
                        # WARNING: replace spaces in header by _
                        yield (header.replace(" ", "_"), sequence.upper())
                    # Out of offset, stop this loop
                    else:
                        break
                # Current offset
                beg_line_offset = in_file.tell()

        # (multi?)FASTA file
        elif first_line.startswith(">"):
            # Go to starting offset
            in_file.seek(offset_start)
            # Set current offset
            beg_line_offset = offset_start
            # Read each line from this point
            for line in in_file:
                # Consider this line as a header
                header = line.decode('utf-8').strip()
                # It is a proper fasta header
                if header.startswith(">"):
                    # The beginning of header is in the offset range
                    if beg_line_offset < offset_end:
                        # Get the sequence
                        sequence = in_file.readline().decode('utf-8').strip()
                        # Get current offset
                        current_offset = in_file.tell()
                        # Get next line
                        next_l = in_file.readline().decode('utf-8').strip()
                        # While this next line is not a fasta header...
                        while next_l and not next_l.startswith(">"):
                            # Add this to the Sequence
                            sequence += next_l
                            # Get current offset
                            current_offset = in_file.tell()
                            # Get next line
                            next_l = in_file.readline().decode('utf-8').strip()
                        # Next line is a fasta header, go back to its beginning
                        in_file.seek(current_offset)
                        # Return header and sequence and wait for the next one
                        # WARNING: replace spaces in header by _
                        yield (header.replace(" ", "_"), sequence.upper())
                    # Out of offset, stop this loop
                    else:
                        break
                # Current offset
                beg_line_offset = in_file.tell()
        # Not a valid file
        else:
            # Stop the generator with the error to show
            raise ValueError("File error: enable to understand type of file "\
                             "{} ({})".format(file, first_line[0]))

def build_graph(ref, k):
    """ Index each k-mers of a genome
        Aho-Corasick implementation, requires pypi package pyahocorasick

    :param ref: the reference to index
    :param k: k-mer size
    :type ref: str
    :type k: int
    """
    # Create the automaton
    graph = ahocorasick.Automaton()
    # Add each kmers of ref in the automaton
    for i, _ in enumerate(ref[0:len(ref)-k+1]):
        # The current kmer
        pattern = ref[i:i+k].upper()
        # Add the kmer
        added = graph.add_word(pattern, (i, pattern))
        # If this kmer was already added
        if not added:
            # Print a warning
            print("Warning: kmer {} at position {} is present more "\
                   "than one time in reference, only the last one will "\
                   "be used".format(pattern, i))
    # Construct the graph
    graph.make_automaton()
    # Return the graph
    return graph

def find_hits(graph, a_read):
    """ Find all kmers of ref present in a read
        All hits are on the form:
        start_pos_read: start_pos_ref

    :param graph: the graph to parse
    :param a_read: the read to search in the index
    :type graph: :py:class:`pyahocorasick`
    :type a_read: str
    """
    # Results
    hits = {}
    # Search the hits
    for item in graph.iter(a_read):
        # Add in the dict the results
        hits[item[0]-len(item[1][1])+1] = item[1][0]
    # Return the hits
    return hits

def reverse_complement(seq):
    """ Take an input sequence and return its revcomp

    :param seq: the seq to compute
    :type seq: str
    """
    # Empty return sequence
    ret = ""
    # Hash of correspondence
    rc_val = {"A": "T", "T": "A", "C": "G", "G": "C", "N": "N"}
    # For each nucleotides
    for nucl in seq[::-1]:
        try:
            # Add its rc to ret
            ret += rc_val[nucl.upper()]
        except KeyError:
            print("Ignoring character '{}' founded in {}".format(nucl, seq))
    # Return ret
    return ret

def get_recombinations(offset_start, offset_end, file, k, gap, graph1, graph2=None):
    """ Main parallelized function that retrieve each read
        of a offset range and find matches and breakpoint of them.

    :param offset_start: where to start taking sequences in the file
    :param offset_end: where to stop taking sequences in the file
    :param file: the filename of the file where to take sequences from
    :param k: size of kmers
    :param gap: maximum authorized gap size for continuous hits
    :param graph1: the graph to parse for genome1
    :param graph2: the graph to parse for genome2
    :type offset_start: int
    :type offset_end: int
    :type file: string
    :type k: int
    :type gap: int
    :type graph1: :type graph: :py:class:`pyahocorasick`
    :type graph2: :type graph: :py:class:`pyahocorasick` or None
    """
    # Resulting Reads of current offset range
    all_queries = []
    try:
        # Query each read, one by one, in the offset range
        for header, sequence in next_read(file, offset_start, offset_end):
            # Construct the Read
            query = read.Read(header, sequence)

            # Find hits for this query
            hits = find_hits(graph1, query.sequence)
            # Transforms hits to matches
            query.get_matches(hits, gap, k, 0, 1)
            # Find hits for this query (Rev comp)
            hits_rc = find_hits(graph1, reverse_complement(query.sequence))
            # Transforms hits to matches
            query.get_matches(hits_rc, gap, k, 1, 1)

            # Two ref files
            if graph2:
                # Find hits for this query
                hits = find_hits(graph2, query.sequence)
                # Transforms hits to matches
                query.get_matches(hits, gap, k, 0, 2)
                # Find hits for this query (Rev comp)
                hits_rc = find_hits(graph2,reverse_complement(query.sequence))
                # Transforms hits to matches
                query.get_matches(hits_rc, gap, k, 1, 2)

            # Create the breakpoints
            query.get_breakpoints()

            # Add this query to the result
            all_queries.append(query)
    except ValueError as exc:
        raise exc

    # Add the global result into the queue
    return all_queries

def get_all_queries(file, nb_proc, k, gap, graph1, graph2=None):
    """ Launch all parallel process to get all queries from a file

    :param file: the filename of the file where to take sequences from
    :param nb_proc: number of precess to run in parallel
    :param k: size of kmers
    :param gap: maximum authorized gap size for continuous hits
    :param graph1: the graph to parse for genome1
    :param graph2: the graph to parse for genome2
    :type file: string
    :type nb_proc: int
    :type k: int
    :type gap: int
    :type graph1: :type graph: :py:class:`pyahocorasick`
    :type graph2: :type graph: :py:class:`pyahocorasick` or None
    """
    # Get the size of the file
    total_size = os.path.getsize(file)
    # Size of what to read
    chunk_size = total_size // nb_proc
    # Starting offset
    offset_start = 0
    try:
        # Create the pool of process
        pool = Pool()
        # Partial function to fix all but firsts arguments
        prod_recomb=partial(get_recombinations, file=file, k=k, gap=gap,
                            graph1=graph1, graph2=graph2)
        # All tuples of offset_start, offset_end
        all_offsets = []
        # For each thread/chunk
        for _ in range(nb_proc - 1):
            # Compute the ending offset for this chunk
            offset_end = offset_start + chunk_size
            # Add this couple of start/end
            all_offsets.append((offset_start, offset_end))
            # Next start is where it stops
            offset_start = offset_start + chunk_size
        # Add the last chunk
        all_offsets.append((offset_start, total_size))

        # Launch all process (Results is a list of list)
        results = pool.starmap(prod_recomb, all_offsets)
    except ValueError as exc:
        print(exc)
        pool.terminate()
        sys.exit(1)
    pool.terminate()

    # Get a flatten list
    all_queries = []
    for i in results:
        all_queries += i

    # Return all queries
    return all_queries

def prepare_blast_file(breakpoint_file, all_queries, minsizeblast):
    """ Prepare a fasta file to be Blasted containing all breakpoints
        of at least minsizeblast nucleotides.
        WARNING: this wrote a FASTA file, regardless of the format of
        the original file
        WARNING: headers of original files are modified to add the
        information of which breakpoint(s) of a specific read are
        Blasted: original_header_#bp

    :param breakpoint_file: the filename of the file to be written
    :param all_queries: all queries that may contain breakpoints
    :param minsizeblast: minimal size of breakpoint accepted
    :type breakpoint_file: string
    :type all_queries: list(:py:class:`Read`)
    :type minsizeblast: int
    """

    # This dict will contain headers (minus the first '>') of
    # breakpoints to blast as they are written, associated to there
    # index in all_queries.
    all_breakpoints = {}
    # Open the file to be Blasted
    with open(breakpoint_file, "w") as out_brp:
        # Parse each query and extract potential breakpoints
        for index, query in enumerate(all_queries):
            # Only the matched ones
            if query.get_ref() != 0:
                # Get all breakpoints and there id
                for nb_brp, brp in enumerate(query.breakpoints):
                    # Minimal size to Blast (could be negative)
                    if abs(brp.size) >= minsizeblast:
                        # Forge un header pour dico et pour ecrire,
                        # le +1 car les bp sont de 1 à n
                        # Forge the header: originalheader_idBreakpoint
                        # breakpoint count starts at 1
                        header = "{}_{}".format(query.header[1:], nb_brp+1)
                        # Associate it with its id in all_queries
                        all_breakpoints[header] = index
                        # Compute start/stop pos (size could be negative)
                        beg = min(brp.beg_pos_read, brp.beg_pos_read+brp.size)
                        end = max(brp.beg_pos_read, brp.beg_pos_read+brp.size)
                        # Write it to the file
                        out_brp.write(">{}\n{}\n".\
                            format(header, query.sequence[beg:end]))
    # Return the main dict of Breakpoints/index
    return all_breakpoints

def process_blast_res(compressed_file, res_blast_file, sep, all_breakpoints):
    """ Compress Blast result to only show the bests hits and output
        result in a fasta-like file. Header is the original header
        with breakpoint id, e-value and bit-score.
        WARNING: this wrote a FASTA file, regardless of the format of
        the original file

    :param compressed_file: the filename of the file to be written
    :param res_blast_file: Blast result file
    :param sep: separator to use in the result file
    :param all_breakpoints: dict of Breakpoints/index created before the Blast
    :type compressed_file: string
    :type res_blast_file: string
    :type sep: list(char)
    :type all_breakpoints: dict
    """
    # Dict that will contain index in all_queries associated with
    # the list of breakpoints that have a Blast result
    all_bp_query = defaultdict(list)
    # Open output file where to write
    with open(compressed_file, "w") as compressed:
        # Open Blast result file
        with open(res_blast_file) as blast_out:
            # Get the 4 info for the first line
            cur_header, cur_matches, cur_evalue, cur_bitscore = blast_out.\
                                                                readline().\
                                                                split()
            # key is index in all_queries and Blasted bp is added
            all_bp_query[all_breakpoints[cur_header]].append(cur_header.\
                                                             split("_")[-1])
            # Forge the header for this first line
            fasta_header = ">{0}{1}{2}{1}{3}\n".format(cur_header, sep[1],
                                                       cur_evalue,
                                                       cur_bitscore)
            # Remove some blast info
            small_match = cur_matches.split("location")[0][:-2]
            # Set of matches for this header
            fasta_line = {small_match}
            # For each other line in the blast result file
            for line in blast_out:
                # Info from this line
                header, matches, evalue, bitscore = line.split()
                # Same header than before?
                if header == cur_header:
                    # Same bit-score/e-value?
                    if evalue == cur_evalue and bitscore == cur_bitscore:
                        # Remove some blast info
                        small_match = matches.split("location")[0][:-2]
                        # Add this blast result
                        fasta_line.add(small_match)
                # New header
                else:
                    # Write the previous header
                    compressed.write(fasta_header)
                    # Write the corresponding results
                    compressed.write(sep[2].join(fasta_line) + "\n")
                    # Get new header
                    cur_header = header
                    # Get new match
                    cur_matches = matches
                    # Get new e-value
                    cur_evalue = evalue
                    # Get new bit-score
                    cur_bitscore = bitscore
                    # Associate the current breakpoint to its index
                    # in all_queries
                    all_bp_query[all_breakpoints[cur_header]].\
                                 append(cur_header.split("_")[-1])
                    # Forge the new header
                    fasta_header = ">{0}{1}{2}{1}{3}\n".format(cur_header,
                                                               sep[1],
                                                               cur_evalue,
                                                               cur_bitscore)
                    # Remove some blast info
                    small_match = cur_matches.split("location")[0][:-2]
                    # Set of matches for this header
                    fasta_line = {small_match}
        # Write the last header
        compressed.write(fasta_header)
        # Write the corresponding results
        compressed.write(sep[2].join(fasta_line) + "\n")
    # Return blasted breakpoint and associated index in all_queries
    return all_bp_query
