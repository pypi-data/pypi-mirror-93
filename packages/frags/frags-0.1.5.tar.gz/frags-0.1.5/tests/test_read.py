"""Tests for read.py"""
from frags import read
from .context import frags

def test_read():
    """ Test class 'Read(header, sequence)' and basic functions"""
    a_r = read.Read("head", "ACGTACGT")
    b_read = read.Read("head", "ACGTACGT")
    c_read = read.Read("heade", "ACGTACGT")
    not_read = "bla"
    assert a_r == b_read
    # Test __eq__
    assert a_r != c_read
    assert a_r != not_read
    # Test __repr__
    assert repr(a_r) == "('head', 'ACGTACGT', [], [], -1, 0, [])"

def test_get_strand():
    """ Test function 'get_strand()'"""
    a_header = "head"
    a_r = read.Read(a_header, "ACGTACGTAAACGTTTTGTCGTATGTGTGATGATGCTACTGATCAC")
    assert a_r.get_strand() == -1

    a_r.all_strand.append(0)
    assert a_r.get_strand() == 0

    a_r.all_strand.append(1)
    a_r.all_strand.append(1)
    a_r.all_strand.append(1)
    assert a_r.get_strand() == 2

    a_r.all_strand.remove(0)
    assert a_r.get_strand() == 1

def test_get_ref():
    """ Test function 'get_ref()'"""
    a_header = "head"
    a_r = read.Read(a_header, "ACGTACGTAAACGTTTTGTCGTATGTGTGATGATGCTACTGATCAC")
    assert a_r.get_ref() == 0

    a_r.all_ref.append(1)
    assert a_r.get_ref() == 1

    a_r.all_ref.append(2)
    a_r.all_ref.append(2)
    a_r.all_ref.append(2)
    assert a_r.get_ref() == 3

    a_r.all_ref.remove(1)
    assert a_r.get_ref() == 2

def test_output():
    """ Test function 'output(sep)'"""
    a_header = "head"
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
    a_r.add_a_match(a_match)
    # Output this read
    assert a_r.output([":", "|", "\t"]) == "{0}\t{1}\t0\tNone\t(+)({2}){3}:{4"\
                                           "}\t({2}){5}:{4}\t{4}\t{6}\tNone"\
                                           "\n".format(a_header,
                                                       a_strand,
                                                       a_ref,
                                                       a_beg_pos_read,
                                                       a_size,
                                                       a_beg_pos_ref,
                                                       0)

    # Add it another match
    b_beg_pos_read = 20
    b_beg_pos_ref = 33
    b_size = 12
    b_insert = 1
    b_match = read.Match(b_beg_pos_read, b_beg_pos_ref, a_strand, a_ref,
                         b_size, [b_insert], read_size)
    a_r.matches.append(b_match)
    # Add it a breakpoint
    beg_bp = 10
    size_bp = 10
    a_bp = read.Breakpoint(beg_bp, size_bp)
    a_r.breakpoints.append(a_bp)
    # Output this read
    assert a_r.output([":", "|", "\t"]) == "{0}\t{1}\t1\t{2}:{3}\t(+)({4}){5}"\
                                           ":{6}|(+)({4}){7}:{8}\t({4}){9}:"\
                                           "{6}|({4}){10}:{8}\t{6}|{8}\t"\
                                           "0|{11}\tNone\n".format(a_header,
                                                           a_strand,
                                                           beg_bp,
                                                           size_bp,
                                                           a_ref,
                                                           a_beg_pos_read,
                                                           a_size,
                                                           b_beg_pos_read,
                                                           b_size,
                                                           a_beg_pos_ref,
                                                           b_beg_pos_ref,
                                                           b_insert)

    # Add it third match
    c_beg_pos_read = 50
    c_beg_pos_ref = 60
    c_size = 8
    c_insert = 2
    c_match = read.Match(c_beg_pos_read, c_beg_pos_ref, a_strand, a_ref,
                         c_size, [c_insert], read_size)
    a_r.matches.append(c_match)
    # Add it a second breakpoint
    b_beg_bp = 32
    b_size_bp = 18
    b_bp = read.Breakpoint(b_beg_bp, b_size_bp)
    a_r.breakpoints.append(b_bp)
    # These breakpoints were Blasted
    id_first_bp_blasted = 0
    a_r.bp_blasted.append(id_first_bp_blasted)
    id_second_bp_blasted = 1
    a_r.bp_blasted.append(id_second_bp_blasted)
    # Output this read
    assert a_r.output([":", "|", "\t"]) == "{0}\t{1}\t2\t{2}:{3}|{4}:{5}\t(+)"\
                                           "({6}){7}:{8}|(+)({6}){9}:{10}|(+)"\
                                           "({6}){11}:{12}\t({6}){13}:{8}|"\
                                           "({6}){14}:{10}|({6}){15}:{12}\t"\
                                           "{8}|{10}|{12}\t0|{16}|{17}\t{18}|"\
                                           "{19}"\
                                           "\n".format(a_header,
                                                       a_strand,
                                                       beg_bp,
                                                       size_bp,
                                                       b_beg_bp,
                                                       b_size_bp,
                                                       a_ref,
                                                       a_beg_pos_read,
                                                       a_size,
                                                       b_beg_pos_read,
                                                       b_size,
                                                       c_beg_pos_read,
                                                       c_size,
                                                       a_beg_pos_ref,
                                                       b_beg_pos_ref,
                                                       c_beg_pos_ref,
                                                       b_insert,
                                                       c_insert,
                                                       id_first_bp_blasted,
                                                       id_second_bp_blasted)

def test_add_a_match():
    """ Test function 'add_a_match(match)'"""
    a_header = "head"
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
    a_r.add_a_match(a_match)

    # Match smaller than the one already in the read, different ref
    b_match = read.Match(a_beg_pos_read+2, a_beg_pos_ref, a_strand, 2,
                         a_size-4, [], read_size)
    # Backup matches status
    tmp_matches = a_r.matches.copy()
    # Try to add it
    a_r.add_a_match(b_match)
    # It was not added
    assert tmp_matches == a_r.matches

    # Different match of same size
    b_match = read.Match(a_beg_pos_read+2, a_beg_pos_ref, a_strand, 2,
                         a_size, [], read_size)
    # Backup matches status
    tmp_matches.append(b_match)
    # Try to add it
    a_r.add_a_match(b_match)
    # It was not added
    assert tmp_matches == a_r.matches

    # Match bigger, same ref
    d_match = read.Match(a_beg_pos_read, a_beg_pos_ref, a_strand, a_ref,
                         a_size+4, [], read_size)
    # Try to add it
    a_r.add_a_match(d_match)
    # If it is added...
    tmp_matches.append(d_match)
    # a_match should be removed
    tmp_matches.remove(a_match)
    # b_match should be removed
    tmp_matches.remove(b_match)
    # It was added
    assert tmp_matches == a_r.matches

    # Match bigger, different ref
    e_match = read.Match(a_beg_pos_read, a_beg_pos_ref, a_strand, 2,
                         a_size+4, [], read_size)
    # Try to add it
    a_r.add_a_match(e_match)
    # It was not added
    assert tmp_matches == a_r.matches

def test_get_matches():
    """ Test function 'get_matches(hits, gap, k, strand, ref)'"""
    a_r = read.Read("head", "ACGTACGTAAACGTTTTGTCGTA")
    hits = {}
    hits[0] = 2
    hits[8] = 15
    gap = 1
    k = 4
    strand = 0
    ref = 1
    assert a_r.get_strand() == -1
    assert a_r.get_ref() == 0
    a_r.get_matches(hits, gap, k, strand, ref)
    assert a_r.get_strand() == strand
    assert a_r.get_ref() == ref
    assert a_r.matches[0].__repr__() == "(0, 0, 4, 2, 6, 4, [0], 1)"
    assert a_r.matches[1].__repr__() == "(0, 8, 12, 15, 19, 4, [0], 1)"
    # Test the repr function of Read without insertion
    assert a_r.__repr__() == "('head', 'ACGTACGTAAACGTTTTGTCGTA', [(0, 0, 4, "\
                             "2, 6, 4, [0], 1), (0, 8, 12, 15, 19, 4, [0], 1)"\
                             "], [], 0, 1, [])"

    # Other strand and gap activated
    hits = {}
    hits[0] = 2
    hits[5] = 7
    gap = 2
    k = 4
    strand = 1
    ref = 2
    a_r.get_matches(hits, gap, k, strand, ref)
    assert a_r.matches[2].__repr__() == "(1, 14, 23, 2, 11, 9, [1], 2)"
    assert a_r.get_strand() == 2
    assert a_r.get_ref() == 3

    # Other way around for strand
    a_r = read.Read("head", "ACGTACGTAAACGTTTTGTCGTA")
    hits = {}
    hits[0] = 2
    hits[8] = 15
    gap = 1
    k = 4
    strand = 1
    ref = 1
    a_r.get_matches(hits, gap, k, strand, ref)
    assert a_r.matches[0].__repr__() == "(1, 19, 23, 2, 6, 4, [0], 1)"
    assert a_r.matches[1].__repr__() == "(1, 11, 15, 15, 19, 4, [0], 1)"

    # Other strand and gap activated
    hits = {}
    hits[0] = 2
    hits[5] = 7
    gap = 2
    k = 4
    strand = 0
    ref = 1
    a_r.get_matches(hits, gap, k, strand, ref)
    assert a_r.matches[2].__repr__() == "(0, 0, 9, 2, 11, 9, [1], 1)"

    # Test the repr function of Read
    assert a_r.__repr__() == "('head', 'ACGTACGTAAACGTTTTGTCGTA', [(1, 19, 23"\
                             ", 2, 6, 4, [0], 1), (1, 11, 15, 15, 19, 4, [0],"\
                             " 1), (0, 0, 9, 2, 11, 9, [1], 1)], [], 2, 1, [])"

    # More hits to test insertions
    a_r = read.Read("head", "ACGTACGTAAACGTTTTGTCGTATGTGTGATGATGCTACTGATCACGT"\
                            "GTACTGGTCGTACTGATGCTGACTGATCTGTAC")
    hits = {}
    hits[0] = 2
    hits[5] = 7
    hits[9] = 12
    hits[17] = 60
    gap = 2
    k = 4
    strand = 0
    ref = 1
    a_r.get_matches(hits, gap, k, strand, ref)

    # Test the repr function of Read
    assert a_r.__repr__() == "('head', 'ACGTACGTAAACGTTTTGTCGTATGTGTGATGATGCT"\
                             "ACTGATCACGTGTACTGGTCGTACTGATGCTGACTGATCTGTAC', "\
                             "[(0, 0, 13, 2, 15, 13, [1, 1], 1), (0, 17, 21, "\
                             "60, 64, 4, [0], 1)], [], 0, 1, [])"

    # More hits to test insertions
    #'''
    hits = {}
    hits[24] = 50
    gap = 2
    k = 4
    strand = 1
    ref = 1
    a_r.get_matches(hits, gap, k, strand, ref)

    # Test the repr function of Read
    assert a_r.__repr__() == "('head', 'ACGTACGTAAACGTTTTGTCGTATGTGTGATGATGCT"\
                             "ACTGATCACGTGTACTGGTCGTACTGATGCTGACTGATCTGTAC', "\
                             "[(0, 0, 13, 2, 15, 13, [1, 1], 1), (0, 17, 21, "\
                             "60, 64, 4, [0], 1), (1, 53, 57, 50, 54, 4, [0],"\
                             " 1)], [], 2, 1, [])"

def test_get_breakpoints():
    """ Test function 'get_breakpoints()'"""
    # Add 2 matches on a read
    a_header = "head"
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
    # Add it another match
    b_beg_pos_read = 20
    b_beg_pos_ref = 33
    b_size = 12
    b_insert = 1
    b_match = read.Match(b_beg_pos_read, b_beg_pos_ref, a_strand, a_ref,
                         b_size, [b_insert], read_size)
    a_r.matches.append(b_match)

    # Get the breakpoint
    a_r.get_breakpoints()

    # Create a breakpoint
    beg_bp = 10
    size_bp = 10
    a_bp = read.Breakpoint(beg_bp, size_bp)

    assert len(a_r.breakpoints) == 1
    assert a_r.breakpoints[0] == a_bp

    # Add 2 matches on a read and add a breakpoint before calling
    a_header = "head"
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
    # Add it another match
    b_beg_pos_read = 20
    b_beg_pos_ref = 33
    b_size = 12
    b_insert = 1
    b_match = read.Match(b_beg_pos_read, b_beg_pos_ref, a_strand, a_ref,
                         b_size, [b_insert], read_size)
    a_r.matches.append(b_match)

    # Create a breakpoint
    beg_bp = 10
    size_bp = 10
    a_bp = read.Breakpoint(beg_bp, size_bp)

    a_r.breakpoints.append(a_bp)

    # Get the breakpoint
    a_r.get_breakpoints()

    # The function does not add the breakpoint as it is already in,
    # so same res as befor
    assert len(a_r.breakpoints) == 1
    assert a_r.breakpoints[0] == a_bp

    # Add 2 overlapping matches on a read, negative size of a breakpoint
    a_header = "head"
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
    # Add it another match
    b_beg_pos_read = 5
    b_beg_pos_ref = 28
    b_size = 12
    b_insert = 1
    b_match = read.Match(b_beg_pos_read, b_beg_pos_ref, a_strand, a_ref,
                         b_size, [b_insert], read_size)
    a_r.matches.append(b_match)

    # Get the breakpoint
    a_r.get_breakpoints()

    # Create a breakpoint
    beg_bp = 10
    size_bp = -5
    a_bp = read.Breakpoint(beg_bp, size_bp)

    assert len(a_r.breakpoints) == 1
    assert a_r.breakpoints[0] == a_bp



def test_match():
    """ Test class
    'Match(beg_pos_read, beg_pos_ref, strand, ref, size, inserts, seq_l)'
    """
    a_match = read.Match(0, 3, 1, 1, 10, 0, 20)
    b_match = read.Match(10, 3, 0, 2, 10, 0, 20)
    c_match = read.Match(10, 3, 0, 2, 10, 0, 20)
    # Test __repr__
    assert a_match.__repr__() == "(1, 10, 20, 3, 13, 10, [0], 1)"
    assert b_match.__repr__() == "(0, 10, 20, 3, 13, 10, [0], 2)"
    # __eq__
    assert a_match != b_match
    assert a_match != []
    assert b_match == c_match

def test_is_include_in():
    """Test function 'is_include_in(other)'"""
    a_match = read.Match(0, 3, 0, 1, 10, 0, 20)
    # b in a
    b_match = read.Match(2, 3, 0, 1, 8, 0, 20)
    assert b_match.is_include_in(a_match)
    # rev c in a
    c_match = read.Match(12, 3, 1, 1, 5, 0, 20)
    assert c_match.is_include_in(a_match)
    # a not in rev c
    assert not a_match.is_include_in(c_match)

def test_output_read():
    """Test function 'output_read(sep)'"""
    a_beg_pos_read = 0
    a_beg_pos_ref = 3
    a_strand = 0
    a_ref = 1
    a_size = 10
    a_insert = 0
    a_seq_l = 20
    a_match = read.Match(a_beg_pos_read, a_beg_pos_ref, a_strand, a_ref,
                         a_size, a_insert, a_seq_l)
    a_sep = ["X", 2]
    assert a_match.output_read(a_sep) == "(+)({}){}{}{}".format(a_ref,
                                                              a_beg_pos_read,
                                                              a_sep[0],
                                                              a_size)
    b_beg_pos_read = 10
    b_beg_pos_ref = 3
    b_strand = 1 # revcomp
    b_ref = 1
    b_size = 3
    b_insert = 2
    b_seq_l = 20
    b_match = read.Match(b_beg_pos_read, b_beg_pos_ref, b_strand, b_ref,
                         b_size, b_insert, b_seq_l)
    b_sep = ["Y"]
    assert b_match.output_read(b_sep) == "(-)({}){}{}{}".format(b_ref,
                                                                b_seq_l -
                                                                b_size -
                                                                b_beg_pos_read,
                                                                b_sep[0],
                                                                b_size)

def test_output_ref():
    """Test function 'output_ref(sep)'"""
    a_beg_pos_read = 0
    a_beg_pos_ref = 3
    a_strand = 0
    a_ref = 1
    a_size = 10
    a_insert = 0
    a_seq_l = 20
    a_match = read.Match(a_beg_pos_read, a_beg_pos_ref, a_strand, a_ref,
                         a_size, a_insert, a_seq_l)
    a_sep = ["|", 2]
    assert a_match.output_ref(a_sep) == "({}){}{}{}".format(a_ref,
                                                              a_beg_pos_ref,
                                                              a_sep[0],
                                                              a_size)

    b_beg_pos_read = 10
    b_beg_pos_ref = 3
    b_strand = 1 # revcomp
    b_ref = 1
    b_size = 3
    b_insert = 2
    b_seq_l = 20
    b_match = read.Match(b_beg_pos_read, b_beg_pos_ref, b_strand, b_ref,
                         b_size, b_insert, b_seq_l)
    b_sep = ["\n"]
    assert b_match.output_ref(b_sep) == "({}){}{}{}".format(b_ref,
                                                            b_beg_pos_ref,
                                                            b_sep[0],
                                                            b_size)



def test_breakpoint():
    """ Test class 'Breakpoint(beg_pos_read, size)'"""
    a_bp = read.Breakpoint(0, 3)
    b_bp = read.Breakpoint(1, 3)
    c_bp = read.Breakpoint(0, 3)
    # Test __repr__
    assert a_bp.__repr__() == "(0, 3)"
    assert b_bp.__repr__() == "(1, 3)"
    # __eq__
    assert a_bp != b_bp
    assert a_bp != (0, 3)
    assert a_bp == c_bp


def test_output_bp():
    """ Test function 'output(sep)'"""
    beg_pos = 0
    size = 5
    sep = [":", "|"]
    a_bp = read.Breakpoint(beg_pos, size)
    assert a_bp.output(sep) == "{}{}{}".format(beg_pos, sep[0], size)
