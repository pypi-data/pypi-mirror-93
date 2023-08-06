"""Tests for core.py"""
import gzip
import pytest
from frags import core
from frags import read
from .context import frags

def test_write_header(tmpdir):
    """ Test function 'write_header(output_file, sep)'"""
    csv_file = tmpdir.join("test.csv")
    sep = "\t"
    # Tab by default
    core.write_header(csv_file)
    assert csv_file.read() == "Read_header{0}"\
                      "Reverse_complement{0}"\
                      "Number_of_breakpoints{0}"\
                      "Breakpoints_positions{0}"\
                      "Matches_read_positions{0}"\
                      "Matches_ref_positions{0}"\
                      "Matches_size{0}"\
                      "Insertions{0}"\
                      "Blast_results_breakpoints\n".format(sep)
    # User-define separator
    sep = "PwEt"
    core.write_header(csv_file, sep)
    assert csv_file.read() == "Read_header{0}"\
                      "Reverse_complement{0}"\
                      "Number_of_breakpoints{0}"\
                      "Breakpoints_positions{0}"\
                      "Matches_read_positions{0}"\
                      "Matches_ref_positions{0}"\
                      "Matches_size{0}"\
                      "Insertions{0}"\
                      "Blast_results_breakpoints\n".format(sep)

def test_get_reference(capsys, tmpdir):
    """ Test function 'get_reference(file)'"""
    # Test fasta (multi-line) file with more than one sequence
    fasta_file = tmpdir.join("test.fasta")
    fasta_file.write(">Fake1\nACGTTATATGCTA\nTGTG\n>Fake2\nCAGTACTAGCA")
    res = core.get_reference(fasta_file)
    assert res == "ACGTTATATGCTATGTG"

    # Test gzipped fasta file
    data = b">Fake1\nACGTTATATGCTATGTG\n"
    fastagz_file = tmpdir.join("test.fasta.gz")
    with gzip.open(fastagz_file, "wb") as fil:
        fil.write(data)
    res = core.get_reference(fastagz_file)
    assert res == "ACGTTATATGCTATGTG"

    # Test fastq file
    fastq_file = tmpdir.join("test.fastq")
    fastq_file.write("@Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!")
    res = core.get_reference(fastq_file)
    assert res == "ACGTTATATGCTATGTG"

    # Test gzipped fastq file
    data = b"@Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!\n"
    fastqgz_file = tmpdir.join("test.fastq.gz")
    with gzip.open(fastqgz_file, "wb") as fil:
        fil.write(data)
    res = core.get_reference(fastqgz_file)
    assert res == "ACGTTATATGCTATGTG"

    # Test wrong gzipped fastq file
    data = b"+Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!\n"
    fastqgz_file = tmpdir.join("test.fastq.gz")
    with gzip.open(fastqgz_file, "wb") as fil:
        fil.write(data)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        res = core.get_reference(fastqgz_file)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    captured = capsys.readouterr()
    assert "File error: enable to understand type of file {} "\
           "(+)".format(fastqgz_file) in captured.out

def test_next_read(capsys, tmpdir):
    """ Test function 'next_read(files)'"""
    # Test fasta (multi-line) file with two sequences
    fasta_file = tmpdir.join("test.fasta")
    fasta_file.write(">Fake1\nACGTTATATGCTA\nTGTG\n>Fake2\nCAGTACTAGCA")
    # Only a portion of the file (from 0 to 3)
    res = core.next_read(fasta_file, 0, 3)
    # First read
    a_read = next(res, None)
    assert a_read == (">Fake1", "ACGTTATATGCTATGTG")
    # No second read
    a_read = next(res, None)
    assert a_read is None
    # Full file
    res = core.next_read(fasta_file, 0, 35)
    # First read
    a_read = next(res, None)
    assert a_read == (">Fake1", "ACGTTATATGCTATGTG")
    # No second read
    a_read = next(res, None)
    assert a_read == (">Fake2", "CAGTACTAGCA")

    # Test gzipped fasta file
    data = b">Fake1\nACGTTATATGCTATGT\n"
    fastagz_file = tmpdir.join("test.fasta.gz")
    with gzip.open(fastagz_file, "wb") as fil:
        fil.write(data)
    res = core.next_read(fastagz_file, 0, 35)
    # First read
    a_read = next(res)
    assert a_read == (">Fake1", "ACGTTATATGCTATGT")

    # Test fastq file with two sequence
    fastq_file = tmpdir.join("test.fastq")
    fastq_file.write("@Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!\n"\
                     "@Fake2\nATGCATGCTG\n+Fake1\n8173*8173!")
    # First sequence only (from 0 to 3)
    res = core.next_read(fastq_file, 0, 3)
    # First read
    a_read = next(res, None)
    assert a_read == ("@Fake1", "ACGTTATATGCTATGTG")
    # No second read
    a_read = next(res, None)
    assert a_read is None
    # Full file
    res = core.next_read(fastq_file, 0, 1000)
    # First read
    a_read = next(res, None)
    assert a_read == ("@Fake1", "ACGTTATATGCTATGTG")
    # Second read
    a_read = next(res, None)
    assert a_read == ("@Fake2", "ATGCATGCTG")

    # Test gzipped fastq file
    data = b"@Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!\n"
    fastqgz_file = tmpdir.join("test.fastq.gz")
    with gzip.open(fastqgz_file, "wb") as fil:
        fil.write(data)
    res = core.next_read(fastqgz_file, 0, 35)
    # First read
    a_read = next(res)
    assert a_read == ("@Fake1", "ACGTTATATGCTATGTG")

    # Test wrong gzipped fastq file
    data = b"+Fake1\nACGTTATATGCTATGTG\n+Fake1\n5Q8D8=64DS-+DZ84!\n"
    fastqgz_file = tmpdir.join("test.fastq.gz")
    with gzip.open(fastqgz_file, "wb") as fil:
        fil.write(data)
    with pytest.raises(ValueError) as pytest_wrapped_e:
        res = core.next_read(fastqgz_file, 0, 35)
        a_read = next(res)
    assert pytest_wrapped_e.type == ValueError
    assert str(pytest_wrapped_e.value) == "File error: enable to understand "\
                                          "type of file {} "\
                                          "(+)".format(fastqgz_file)

def test_build_graph(capsys):
    """ Test function 'build_graph(ref, k)'"""
    # The ref to index. Each k-mers will be indexed, except the first AAAC
    ref = "AAACGTCGATTAGCTGAAAC"
    # K-mer size
    k = 4
    graph = core.build_graph(ref, k)
    # What from ACGTTTAAAC is in the index?
    res = []
    for res_tmp in graph.iter("ACGTTTAAAC"):
        res.append(res_tmp[1])
    # AAAC is at index 0 in the index
    assert res[0] == (2, "ACGT")
    # ACGT is at index 2 in the index
    assert res[0] == (2, "ACGT")
    # Warning output
    captured = capsys.readouterr()
    assert "Warning: kmer AAAC at position 16 is present more than one time i"\
           "n reference, only the last one will be used" in captured.out

def test_find_hits(capsys):
    """ Test function 'find_hits(graph, read)'"""
    # start_pos_read: start_pos_ref
    # The ref to index. Each k-mers will be indexed, except the last AAAC
    ref = "AAACGTCGATTAGCTGAAAC"
    # K-mer size
    k = 4
    graph = core.build_graph(ref, k)
    # Read to test
    a_read = "ACGTTTAAAC"
    res = core.find_hits(graph, a_read)
    # On warning to check
    captured = capsys.readouterr()
    assert "kmer AAAC at position 16 is present more than one time in "\
           "reference, only the last one will be used" in  captured.out
    # tmp results
    tmp_res = {}
    # ACGT in 0 (read) match in ref at 2
    tmp_res[0] = 2
    # AAAC in 6 (read) match in ref at 16
    tmp_res[6] = 16
    assert res == tmp_res

def test_reverse_complement(capsys):
    """ Test function 'reverse_complement(seq)'"""
    seq = "ACGT"
    assert core.reverse_complement(seq) == "ACGT"
    seq = "ACZGT"
    assert core.reverse_complement(seq) == "ACGT"
    # Warning output
    captured = capsys.readouterr()
    assert "Ignoring character 'Z' founded in ACZGT" in captured.out

def test_get_recombinations(tmpdir):
    """ Test function 'get_recombinations(offset_start, offset_end,
                                              file, k, gap, graph1,
                                              graph2=None)'"""
    # Fake input file
    file = tmpdir.join("test.fasta")
    file.write(">Fake1\nACGTTATATGTTGATTAGCTGA\nTGTG\n>Fake2\nCAGTACTAGCAGGTA"\
               "TGCTAGA")
    # Fake ref
    ref = "AAACGACGTTATATGTCGATTAGCTGAAAC"
    # Fake second ref
    ref2 = "TTTTGCTAGTACTGTTT"
    # Gap size
    gap = 1
    # Kmer size
    k = 10
    # Read the whole file
    offset_start = 0
    offset_end = 1000
    # Build graphs
    graph1 = core.build_graph(ref, k)
    graph2 = core.build_graph(ref2, k)
    # Get the queries
    all_queries = core.get_recombinations(offset_start, offset_end, file, k,
                                          gap, graph1, graph2)
    # We have 2 res, one for each ref
    assert len(all_queries) == 2
    assert len(all_queries[0].matches) == 1
    assert len(all_queries[1].matches) == 1
    # Full read result for first read
    assert all_queries[0].__repr__() == "('>Fake1', 'ACGTTATATGTTGATTAGCTGATG"\
                                        "TG', [(0, 0, 22, 5, 27, 22, [1], 1)]"\
                                        ", [], 0, 1, [])"
    # Match res for second read
    assert all_queries[1].matches[0].__repr__() == "(1, 0, 11, 3, 14, 11, [0]"\
                                                   ", 2)"

    """ Test function 'get_recombinations(offset_start, offset_end,
                                              file, k, gap, graph1,
                                              graph2=None)'"""
    # Fake false input file
    file = tmpdir.join("test.fasta")
    file.write("?Fake1\nACGTTATATGTTGATTAGCTGA\nTGTG\n>Fake2\nCAGTACTAGCAGGTA"\
               "TGCTAGA")
    # Fake ref
    ref = "AAACGACGTTATATGTCGATTAGCTGAAAC"
    # Fake second ref
    ref2 = "TTTTGCTAGTACTGTTT"
    # Gap size
    gap = 1
    # Kmer size
    k = 10
    # Read the whole file
    offset_start = 0
    offset_end = 1000
    # Build graphs
    graph1 = core.build_graph(ref, k)
    graph2 = core.build_graph(ref2, k)
    # Get the queries
    with pytest.raises(ValueError) as pytest_wrapped_e:
        all_queries = core.get_recombinations(offset_start, offset_end, file,
                                              k, gap, graph1, graph2)
    # We have a ValueError
    assert pytest_wrapped_e.type == ValueError
    assert str(pytest_wrapped_e.value) == "File error: enable to understand "\
                                          "type of file {} "\
                                          "(?)".format(file)

def test_get_all_queries(tmpdir):
    """ Test function 'get_all_queries(file, nb_proc, k, gap, graph1,
                                      graph2=None)'"""
    # Fake input file
    file = tmpdir.join("test.fasta")
    file.write(">Fake1\nACGTTATATGTTGATTAGCTGA\nTGTG\n>Fake2\nCAGTACTAGCAGGTA"\
               "TGCTAGA")
    # Fake ref
    ref = "AAACGACGTTATATGTCGATTAGCTGAAAC"
    # Fake second ref
    ref2 = "TTTTGCTAGTACTGTTT"
    # Gap size
    gap = 1
    # Kmer size
    k = 10
    # Build graphs
    graph1 = core.build_graph(ref, k)
    graph2 = core.build_graph(ref2, k)
    # Call the function in two process
    all_queries = core.get_all_queries(file, 2, k, gap, graph1, graph2)
    # We have 2 res, one for each ref
    assert len(all_queries) == 2
    assert len(all_queries[0].matches) == 1
    assert len(all_queries[1].matches) == 1
    # Full read result for first read
    assert all_queries[0].__repr__() == "('>Fake1', 'ACGTTATATGTTGATTAGCTGATG"\
                                        "TG', [(0, 0, 22, 5, 27, 22, [1], 1)]"\
                                        ", [], 0, 1, [])"
    # Match res for second read
    assert all_queries[1].matches[0].__repr__() == "(1, 0, 11, 3, 14, 11, [0]"\
                                                   ", 2)"

def test_prepare_blast_file(tmpdir):
    """ Test function 'prepare_blast_file(breakpoint_file, all_queries,
                                          minsizeblast)'"""
    breakpoint_file = tmpdir.join("breakpoints.fasta")

    all_queries = []
    # Add 2 matches on a read
    a_header = ">head1"
    a_r = read.Read(a_header, "ACGTACGTAAACGTTTTGTCGTATGTGTGATGATGCTACTGATCAC"\
                              "GTGTACTGGTCGTACTGATGCTGACTGATCTGTAC")
    read_size = len(a_r.sequence)
    # Normal strand
    a_strand = 0
    a_r.strand = a_strand
    a_ref = 1
    a_size = 10
    # Matches
    a_beg_pos_read = 0
    a_beg_pos_ref = 3
    a_match = read.Match(a_beg_pos_read, a_beg_pos_ref, a_strand, a_ref,
                         a_size, [], read_size)
    a_r.matches.append(a_match)
    a_r.all_ref.append(a_match.ref)
    a_r.all_strand.append(a_match.strand)
    # Add it another match
    b_beg_pos_read = 20
    b_beg_pos_ref = 33
    b_size = 12
    b_insert = 1
    b_match = read.Match(b_beg_pos_read, b_beg_pos_ref, a_strand, a_ref,
                         b_size, [b_insert], read_size)
    a_r.matches.append(b_match)
    a_r.all_ref.append(b_match.ref)
    a_r.all_strand.append(b_match.strand)

    # Get the breakpoint
    a_r.get_breakpoints()

    all_queries.append(a_r)


    # Add 2 overlapping matches on a read, negative size of a breakpoint
    b_header = ">head2"
    b_r = read.Read(b_header, "ACGTACGTAAACGTTTTGTCGTATGTGTGATGATGCTACTGATCAC"\
                              "GTGTACTGGTCGTACTGATGCTGACTGATCTGTAC")
    read_size = len(b_r.sequence)
    # Normal strand
    c_strand = 0
    b_r.strand = c_strand
    c_ref = 1
    c_size = 10
    # Matches
    c_beg_pos_read = 0
    c_beg_pos_ref = 3
    c_match = read.Match(c_beg_pos_read, c_beg_pos_ref, c_strand, c_ref,
                         c_size, [], read_size)
    b_r.matches.append(c_match)
    b_r.all_ref.append(c_match.ref)
    b_r.all_strand.append(c_match.strand)
    # Add it another match
    d_beg_pos_read = 6
    d_beg_pos_ref = 28
    d_size = 12
    d_insert = 1
    d_match = read.Match(d_beg_pos_read, d_beg_pos_ref, c_strand, c_ref,
                         d_size, [d_insert], read_size)
    b_r.matches.append(d_match)
    b_r.all_ref.append(d_match.ref)
    b_r.all_strand.append(d_match.strand)

    # Get the breakpoint
    b_r.get_breakpoints()

    all_queries.append(b_r)

    minsizeblast = 4
    res = core.prepare_blast_file(breakpoint_file, all_queries, minsizeblast)
    assert res == {'head1_1': 0, 'head2_1': 1}
    assert breakpoint_file.read() == ">head1_1\nACGTTTTGTC\n"\
                                                ">head2_1\nGTAA\n"

    minsizeblast = 5
    res = core.prepare_blast_file(breakpoint_file, all_queries, minsizeblast)
    assert res == {'head1_1': 0}
    assert breakpoint_file.read() == ">head1_1\nACGTTTTGTC\n"

def test_process_blast_res(tmpdir):
    """ Test function 'process_blast_res(compressed_file,res_blast_file,
                                         sep, all_breakpoints)'"""
    # Fake input file
    # head1_3 got 3 hits, 2 with same highest eval/bitscore
    # head1_7 and head 2_7 have each one hit
    file = tmpdir.join("res_blast.csv")
    file.write("head1_3\tlcl|NC_000012.12_cds_NP_000215.1_70801~[gene=KRT18]~"\
        "[db_xref=CCDS:CCDS31809.1,Ensembl:ENSP00000373487.3,GeneID:3875]~[pr"\
        "otein=keratin,~type~I~cytoskeletal~18]~[protein_id=NP_000215.1]~[loc"\
        "ation=join(52949174..52949590,52950328..52950410,52950750..52950906,"\
        "52951481..52951645,52951731..52951856,52952119..52952342,52952722..5"\
        "2952842)]~[gbkey=CDS]\t5.77e-19\t97.1\nhead1_3\tlcl|NC_000012.12_cds"\
        "_NP_000215.1_70801~[gene=KRT18]~[db_xref=CCDS:CCDS31809.1,Ensembl:EN"\
        "SP00000373487.3,GeneID:3875]~[protein=keratin,~type~I~cytoskeletal~1"\
        "8]~[protein_id=NP_000215.1]~[location=join(52949174..52949590,529503"\
        "28..52950410,52950750..52950906,52951481..52951645,52951731..5295185"\
        "6,52952119..52952342,52952722..52952842)]~[gbkey=CDS]\t1.25e-15\t86."\
        "1\nhead1_3\tlcl|NC_000012.12_cds_NP_954657.1_70800~[gene=KRT18]~[db_"\
        "xref=CCDS:CCDS31809.1,GeneID:3875]~[protein=keratin,~type~I~cytoskel"\
        "etal~18]~[protein_id=NP_954657.1]~[location=join(52949174..52949590,"\
        "52950328..52950410,52950750..52950906,52951481..52951645,52951731..5"\
        "2951856,52952119..52952342,52952722..52952842)]~[gbkey=CDS]\t5.77e-1"\
        "9\t97.1\nhead1_7\tlcl|NC_000012.12_cds_NP_954657.1_70800~[gene=KRT18"\
        "]~[db_xref=CCDS:CCDS31809.1,GeneID:3875]~[protein=keratin,~type~I~cy"\
        "toskeletal~18]~[protein_id=NP_954657.1]~[location=join(52949174..529"\
        "49590,52950328..52950410,52950750..52950906,52951481..52951645,52951"\
        "731..52951856,52952119..52952342,52952722..52952842)]~[gbkey=CDS]\t5"\
        ".77e-19\t97.1\nhead2_7\tlcl|NC_000012.12_cds_NP_954657.1_70800~[gene"\
        "=KRT18]~[db_xref=CCDS:CCDS31809.1,GeneID:3875]~[protein=keratin,~typ"\
        "e~I~cytoskeletal~18]~[protein_id=NP_954657.1]~[location=join(5294917"\
        "4..52949590,52950328..52950410,52950750..52950906,52951481..52951645"\
        ",52951731..52951856,52952119..52952342,52952722..52952842)]~[gbkey=C"\
        "DS]\t1.25e-15\t86.1\n")

    # Breakpoints
    all_breakpoints = {'head1_1': 0, 'head1_3': 1, 'head1_4': 2, 'head1_7': 3,
                       'head2_1': 4, 'head2_7': 5}
    # Separators
    sep = [":", "|", "\t"]

    # Result file
    compressed_file = tmpdir.join("compressed.fasta")
    res = core.process_blast_res(compressed_file, file, sep,
                            all_breakpoints)
    assert res == {1: ['3'], 3: ['7'], 5: ['7']}

    # Verify output file
    res = []
    for line in compressed_file.readlines():
        res.append(set(line.strip().split("\t")))
    truth = []
    truth.append(set(">head1_3|5.77e-19|97.1\n".strip().split("\t")))
    truth.append(set("lcl|NC_000012.12_cds_NP_000215.1_70801~[gene=KRT18]~[db"\
                     "_xref=CCDS:CCDS31809.1,Ensembl:ENSP00000373487.3,GeneID"\
                     ":3875]~[protein=keratin,~type~I~cytoskeletal~18]~[prote"\
                     "in_id=NP_000215.1]\tlcl|NC_000012.12_cds_NP_954657.1_70"\
                     "800~[gene=KRT18]~[db_xref=CCDS:CCDS31809.1,GeneID:3875]"\
                     "~[protein=keratin,~type~I~cytoskeletal~18]~[protein_id="\
                     "NP_954657.1]\n".strip().split("\t")))
    truth.append(set(">head1_7|5.77e-19|97.1\n".strip().split("\t")))
    truth.append(set("lcl|NC_000012.12_cds_NP_954657.1_70800~[gene=KRT18]~[db"\
                     "_xref=CCDS:CCDS31809.1,GeneID:3875]~[protein=keratin,~t"\
                     "ype~I~cytoskeletal~18]~"\
                     "[protein_id=NP_954657.1]\n".strip().split("\t")))
    truth.append(set(">head2_7|1.25e-15|86.1\n".strip().split("\t")))
    truth.append(set("lcl|NC_000012.12_cds_NP_954657.1_70800~[gene=KRT18]~[db"\
                     "_xref=CCDS:CCDS31809.1,GeneID:3875]~[protein=keratin,~t"\
                     "ype~I~cytoskeletal~18]~"\
                     "[protein_id=NP_954657.1]\n".strip().split("\t")))
    assert res == truth
