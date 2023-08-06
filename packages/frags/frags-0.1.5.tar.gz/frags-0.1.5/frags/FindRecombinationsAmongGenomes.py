# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6

"""
Main file of FRAG software, handle input/output and launch
necessary functions
"""

import argparse
import os
import sys
import time
import subprocess
#from context import frags
from frags import core


__version_info__ = ('0', '1', '5')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2020-12-17"
__author__ = "Nicolas Maillet"

def create_parser():
    """ Handling arguments at startup """
    parser = argparse.ArgumentParser(description="FRAG software (Find Recombi"\
                                                 "nations Among Genomes) "\
                                                 "analyses results of "\
                                                 "sequencing data about "\
                                                 "recombination. It takes "\
                                                 "several fasta/fastq files "\
                                                 "compressed or not "\
                                                 "(-i option) and one or two "\
                                                 "reference genomes "\
                                                 "(-r option). It then "\
                                                 "identifies chimeric reads "\
                                                 "(reads composed of "\
                                                 "non-adjacent fragments, "\
                                                 "coming either from on one "\
                                                 "or the two references "\
                                                 "genomes) and potential "\
                                                 "breakpoints (inserts "\
                                                 "between fragments). "\
                                                 "Optionally, breakpoints can"\
                                                 " then be Blasted again the "\
                                                 "host genome, if provided.")

    parser.add_argument("-i", "--inputfiles", type=str, nargs='+',
                        metavar="file", required=True,
                        help="Input reads files")
    parser.add_argument("-r", "--reffiles", type=str, nargs='+',
                        metavar="file", required=True,
                        help="Input references genomes (maximum two)")
    parser.add_argument("-o", "--outputfolder", type=str, metavar="folder",
                        required=True, help="Output folder for results")
    parser.add_argument("-k", "--kmer", type=int, metavar="", default=30,
                        help="K-mer length of the search (default: 30)")
    parser.add_argument("-g", "--gap", type=int, metavar="", default=10,
                        help="Gap length to consider not contiguous hits as c"\
                             "ontiguous (default: 10)")
    parser.add_argument("-p", "--processes", type=int, metavar="", default=1,
                       help="Number of parallel processes to use (default: 1)")

    group_blast = parser.add_argument_group("Blast options")
    group_blast.add_argument("-b", "--blast", action='store_true',
                             help="Use Blast to analyze breakpoints greater "\
                             "than -m/--minsizeblast argument")
    group_blast.add_argument("-t", "--host", type=str, metavar="file",
                             help="Host genome file. Required if -b/--blast "\
                             "argument is used. Note: a Blast database will "\
                             "be created at this location")
    group_blast.add_argument("-m", "--minsizeblast", type=int, metavar="",
                             default=20, help="Minimum size of breakpoint to "\
                             "Blast (default: 20)")

    group_sep = parser.add_argument_group("CSV separators options")
    group_sep.add_argument("-s", "--posizesep", type=str, metavar="",
                           default=":", help="Separator between position and "\
                           "size (default: :)")
    group_sep.add_argument("-f", "--fieldsep", type=str, metavar="",
                           default="|", help="Field separator inside columns "\
                           "(default: |)")
    group_sep.add_argument("-c", "--csvsep", type=str, metavar="",
                           default="\t", choices=['\t', ','], help="Column "\
                           "separator (default: \\t)")

    group_verbose = parser.add_mutually_exclusive_group()
    group_verbose.add_argument("-q", "--quiet", action="store_true",
                               help="No standard output, only error(s)")
    group_verbose.add_argument("-v", "--verbose", action="count", default=0,
                               help="Verbose mode")

    parser.add_argument("--version", action="version",
                        version="%(prog)s " + __version__ + " from " +
                        __revision_date__)

    return parser

def main():
    """ The main of FRAG """

    ##################
    # ARGUMENTS PART #
    ##################
    # Create the parse for command line arguments
    parser = create_parser()
    # Parse the arguments
    args = parser.parse_args()

    # Global time
    if not args.quiet:
        total_start = time.time()

    # Separators (3 separators, posizesep, fieldsep, csvsep)
    sep = (args.posizesep, args.fieldsep, args.csvsep)

    # Test if blastn command-line in available, if needed
    if args.blast:
        try:
            subprocess.run(["blastn", "-version"], check=True,
                           capture_output=True)
        except FileNotFoundError:
            print("'blastn' command line not found.\n"\
                  "Either Blast is not installed or "\
                  "not accessible through your path.\n"\
                  "Blast will not be performed.")
            # Swith --blast argument to not use it
            args.blast = False

    # Test if makeblastdb command-line in available, if needed
    if args.blast:
        if not args.host:
            parser.error("argument -b/--blast: argument -t/--host is required")
        else:
            # Valid input host file?
            if not os.path.isfile(args.host):
                print("Error, host file {} not found".format(args.host))
                sys.exit(1)
            # Is a database already there?
            if not os.path.isfile(args.host + ".ndb") or\
               not os.path.isfile(args.host + ".nhr") or\
               not os.path.isfile(args.host + ".nin") or\
               not os.path.isfile(args.host + ".not") or\
               not os.path.isfile(args.host + ".nsq") or\
               not os.path.isfile(args.host + ".ntf") or\
               not os.path.isfile(args.host + ".nto"):
                # Test if makeblastdb is accessible
                try:
                    subprocess.run(["makeblastdb", "-help"], check=True,
                                   capture_output=True)
                except FileNotFoundError:
                    print("'makeblastdb' command line not found.\n"\
                          "Either Blast is not fully installed or "\
                          "not accessible through your path.\n"\
                          "Blast will not be performed.")
                    # Swith --blast argument to not use it
                    args.blast = False

    # Input reads files
    files = []
    for file in args.inputfiles:
        # If it seems to be a file
        if os.path.isfile(file):
            files.append(file)
        else:
            print("Error, file {} not found".format(file))
            sys.exit(1)

    # Input reference genomes
    ref_files = []
    for file in args.reffiles:
        # If it seems to be a file
        if os.path.isfile(file):
            # If there is not already 2 files
            if len(ref_files) < 2:
                # Add this file
                ref_files.append(file)
            else:
                print("You can only input 2 references, file {} will be ignor"\
                      "ed".format(file))
        else:
            print("Error, file {} not found".format(file))
            sys.exit(1)

    # Output folder
    output_folder = args.outputfolder
    # Make sure the output path is with leading slash
    if output_folder[-1] != "/":
        output_folder += "/"
    # Create this folder if necessary
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        # Quiet mode
        if not args.quiet:
            print("Folder {} created".format(output_folder))

    # Be sure to have at least 1 process
    if args.processes <= 0:
        parser.error("argument -p/--processes should be greater than 0")

    # Ref names for output files
    ref1 = os.path.splitext(os.path.basename(ref_files[0]))[0]
    # Second ref if it exists
    ref2 = None
    if len(ref_files) > 1:
        ref2 = os.path.splitext(os.path.basename(ref_files[1]))[0]


    ################
    # QUERING PART #
    ################
    # Verbose mode
    if args.verbose:
        # Start timer
        start = time.time()

    # Construct the graph from the ref1
    graph1 = core.build_graph(core.get_reference(ref_files[0]), args.kmer)
    # Construct graph from ref2
    if ref2:
        graph2 = core.build_graph(core.get_reference(ref_files[1]), args.kmer)
    else:
        graph2 = None

    # This will contains the main result
    all_queries = []
    # For each file
    for file in files:
        # Get all queries for this file in parallel
        all_queries += core.get_all_queries(file, args.processes, args.kmer,
                                            args.gap, graph1, graph2)
    # Verbose mode
    if args.verbose:
        # Print exec time
        print("Query time: {:.2f}s".format(time.time() - start))


    ##############
    # BLAST PART #
    ##############

    # Even if Blast is not required
    # Path of breakpoints file
    bp_file = output_folder + "breakpoints.fasta"
    # Verbose mode
    if args.verbose:
        # Start timer
        start = time.time()
    # Prepare the file to be blasted
    # Return a dict with headers associated to index in all_queries
    all_bp_and_pos = core.prepare_blast_file(bp_file, all_queries,
                                             args.minsizeblast)
    # Verbose mode
    if args.verbose:
        # Print exec time
        print("Write file to be Blasted: {:.2f}s".
                  format(time.time() - start))

    # If Blast is required
    if args.blast:
        # Is a Blast database already there?
        if not os.path.isfile(args.host + ".ndb") or\
           not os.path.isfile(args.host + ".nhr") or\
           not os.path.isfile(args.host + ".nin") or\
           not os.path.isfile(args.host + ".not") or\
           not os.path.isfile(args.host + ".nsq") or\
           not os.path.isfile(args.host + ".ntf") or\
           not os.path.isfile(args.host + ".nto"):
            try:
                # Verbose mode
                if args.verbose:
                    # Start timer
                    start = time.time()
                # Build Blast database
                subprocess.run(["makeblastdb", "-in", args.host, "-dbtype",
                                "nucl"], check=True, capture_output=True)
                # Verbose mode
                if args.verbose:
                    # Print exec time
                    print("Blast database construction: {:.2f}s".
                              format(time.time() - start))
            except:
                print("Error: 'makeblastdb' command for creating Blast "\
                      "database failed. Disabling Blast step.")
                args.blast = False   
    # If Blast is still required
    if args.blast:
        # If there is something to blast
        if os.stat(bp_file).st_size > 0:
            # Path of output Blast file
            blast_res = output_folder + "res_blast.csv"
            try:
                # Verbose mode
                if args.verbose:
                    # Start timer
                    start = time.time()
                # Launch Blast
                subprocess.run(["blastn",
                                "-query", bp_file,
                                "-db", args.host,
                                "-outfmt", "6 qseqid sseqid evalue bitscore",
                                "-out", blast_res,
                                "-num_threads", str(args.processes)],
                               check=True)
                # Verbose mode
                if args.verbose:
                    # Print exec time
                    print("Blast time: {:.2f}s".format(time.time() - start))
            # If Blast failed for any reason...
            except:
                print("Blast failed, removing Blast result file.")
                # It is safer to remove result file
                if os.path.exists(blast_res):
                    os.remove(blast_res)

            # If there is some Blast results
            if os.path.exists(blast_res) and os.stat(blast_res).st_size > 0:
                # Verbose mode
                if args.verbose:
                    # Start timer
                    start = time.time()
                # Write compressed output
                # Return which queries have Blast results
                bp_matched = core.process_blast_res(output_folder + \
                                                        "compressed.fasta",
                                                    blast_res,
                                                    sep, all_bp_and_pos)
                # Fill queries info about Blast
                for idq, bps in bp_matched.items():
                    all_queries[idq].bp_blasted = bps

                # Verbose mode
                if args.verbose:
                    # Print exec time
                    print("Write compressed Blast results: {:.2f}s".
                              format(time.time() - start))


    #################
    # WRITING FILES #
    #################
    # Verbose mode
    if args.verbose:
        # Start timer
        start = time.time()

    # Open output files
    # Unmatched
    res_unmatched = open(output_folder + "unmatched.csv", "w")
    # Only ref1
    res_matched1 = open(output_folder + ref1 + ".csv", "w")
    # Write header for ref1 results
    core.write_header(res_matched1, sep[2])
    # There is two ref files
    if ref2:
        # Only ref2
        res_matched2 = open(output_folder + ref2 + ".csv", "w")
        # Write header for ref2 results
        core.write_header(res_matched2, sep[2])
        # Ref1 and ref2
        res_matched1_2 = open(output_folder + ref1 + "_and_" + ref2 + ".csv",
                              "w")
        # Write header for ref1 and ref2 results
        core.write_header(res_matched1_2, sep[2])

    # For each query
    for query in all_queries:
        # Get the ref of this query
        ref = query.get_ref()
        # If there is no match
        if ref == 0:
            # Output it in unmatched file
            res_unmatched.write(query.header + "\n")
        # Match only on ref1
        elif ref == 1:
            # Output it in matched file
            res_matched1.write(query.output(sep))
        # Match only on ref2
        elif ref == 2:
            # Output it in matched file
            res_matched2.write(query.output(sep))
        # Match only on both ref1 and ref2
        elif ref == 3:
            # Output it in matched file
            res_matched1_2.write(query.output(sep))

    # Close files
    res_unmatched.close()
    res_matched1.close()
    if ref2:
        res_matched2.close()
        res_matched1_2.close()

    # Verbose mode
    if args.verbose:
        # Print exec time
        print("Write results files: {:.2f}s".format(time.time() - start))


    #########
    # STATS #
    #########
    '''
    # Stats rajouter une stat sur les parties les plus blastées ?
    stats = collections.defaultdict(int)
    for i in all_breakpoints:
        stats[len(i)] += 1
    ods = collections.OrderedDict(sorted(stats.items()))
    #print("Non unique")
    #print(ods)
    # Set version
    stats = collections.defaultdict(int)
    for i in set(all_breakpoints):
        stats[len(i)] += 1
    ods = collections.OrderedDict(sorted(stats.items()))
    #print("Unique")
    #print(ods)
    '''

    # Global time
    if not args.quiet:
        print("Total time: {:.2f}s".format(time.time() - total_start))

### Let'z go ###
def init():
    """ Launch the main """
    if __name__ == '__main__':
        main()
        # The end
        sys.exit(0)
# GOGOGO
init()
