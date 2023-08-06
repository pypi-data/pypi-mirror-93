# -*- coding: utf-8 -*-

"""Contains class and functions related to read definition and use"""
from operator import attrgetter

class Read:
    """Define a read.

    :param header: header of the read
    :param sequence: sequence of the read
    :type header: str
    :type sequence: str
    """
    def __init__(self, header, sequence):
        self.header = header
        self.sequence = sequence
        self.matches = []
        self.breakpoints = []
        self.all_strand = []
        self.all_ref = []
        self.bp_blasted = [] # Breakpoints that have Blast hit

    # Equality between two Read
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    # self representation for print
    def __repr__(self):
        return repr((self.header, self.sequence, self.matches,
             self.breakpoints, self.get_strand(), self.get_ref(),
             self.bp_blasted))

    def get_strand(self):
        """ Compute the strand of this Read
            (-1=nothing / 0=normal / 1=revcomp / 2=normal AND revcomp)
        """
        # Nothing
        strand = -1
        # If it has matches
        if self.all_strand:
            # Get all uniq strand
            all_strand_uniq = set(self.all_strand)
            # A single strand
            if len(all_strand_uniq) == 1:
                strand = self.all_strand[0]
            # Two strand
            else:
                strand = 2
        return strand

    def get_ref(self):
        """ Compute the ref of this Read
            (0=nothing / 1=ref1 / 2=ref2 / 3=ref1 AND ref2) """
        # Nothing
        ref = 0
        # If it has matches
        if self.all_ref:
            # Get all uniq ref
            all_ref_uniq = set(self.all_ref)
            # A single ref
            if len(all_ref_uniq) == 1:
                ref = self.all_ref[0]
            # Two ref
            else:
                ref = 3
        return ref

    def output(self, sep):
        """ Proper output of a line of the result file

        :param sep: Separator to use in CSV
        :type sep: list(char)
        """
        # Output the first info
        ret = self.header + sep[2] + str(self.get_strand()) + sep[2] + \
              str(len(self.breakpoints)) + sep[2]

        # Output all breakpoints
        if len(self.breakpoints) > 0:
            ret += sep[1].join([x.output(sep) for x in self.breakpoints])
        # No breakpoint
        else:
            ret += "None"
        # Tab before next column
        ret += sep[2]

        # Sort matches by position on the read
        matches = sorted(self.matches, key=attrgetter('beg_pos_read'))

        read_info = []
        ref_info = []
        sizes = []
        inserts = []
        # For each matches in position order
        for i in matches:
            read_info.append(i.output_read(sep[0]))
            ref_info.append(i.output_ref(sep[0]))
            sizes.append(i.size)
            inserts.append(sep[0].join(map(str, i.inserts)))

        # Clean output for matches read
        ret += sep[1].join(read_info) + sep[2]
        # Clean output for matches ref
        ret += sep[1].join(ref_info) + sep[2]
        # Clean output for sizes
        ret += sep[1].join(map(str, sizes)) + sep[2]
        # Clean output for insertions
        ret += sep[1].join(map(str, inserts)) + sep[2]
        # Output ids of all breakpoints that get successfully Blasted
        if len(self.bp_blasted) > 0:
            ret += sep[1].join(map(str, self.bp_blasted))
        # Nothing blasted
        else:
            ret += "None"
        # New line
        ret += "\n"

        return ret

    def add_a_match(self, match):
        """ Test if this match should be added or not.
            It must be added if it is not a subpart of an already added
            other match. In some case, some already added matches are
            subparts of the match to add. If so, they are removed.

        :param match: the match to add
        :type match: :py:class:`Match`
        """
        # Is this match a subpart of a match already added?
        to_add = True
        for i in self.matches:
            if match.is_include_in(i):
                to_add = False
                break
        # If we need to add this match
        if to_add:
            # Matches to be removed
            matches_to_remove = []
            # Is some matches included in the tested one?
            for i in self.matches:
                if i.is_include_in(match):
                    # Add it to be removed
                    matches_to_remove.append(i)
            # Remove them
            for i in matches_to_remove:
                # Remove it
                self.matches.remove(i)
                # Remove the corresponding ref/strand
                self.all_ref.remove(i.ref)
                self.all_strand.remove(i.strand)
            # Add the match
            self.matches.append(match)
            # Add ref/strand
            self.all_ref.append(match.ref)
            self.all_strand.append(match.strand)

    def get_matches(self, hits, gap, k, strand, ref):
        """ Populate matches list from all hits, for one strand

        :param hits: matching position on read and ref
        :param gap: maximum authorized gap size for continuous hits
        :param k: k-mer size
        :param strand: the strand of this hit
        :param ref: the reference index of this hit
        :type hits: dict
        :type gap: int
        :type k: int
        :type strand: int
        :type ref: int
        """
        # If there is some hits
        if hits:
            insert = []
            beg_pos_read = sorted(hits.keys())[0]
            beg_pos_ref = hits[beg_pos_read]
            prev_pos_read = beg_pos_read
            prev_pos_ref = beg_pos_ref

            for i in sorted(hits.keys()):
                # Is the read or ref NOT continuous (modulo gap)?
                if i >= prev_pos_read+gap+k+1 or \
                   hits[i] >= prev_pos_ref+gap+k+1 or \
                   hits[i] < prev_pos_ref:
                    # Add the previous good and complete match
                    size = prev_pos_read - beg_pos_read + k
                    match = Match(beg_pos_read, beg_pos_ref, strand, ref, size,
                                  insert, len(self.sequence))
                    # Add the match
                    self.add_a_match(match)
                    # Reinit insertions
                    insert = []
                    # New match
                    beg_pos_read = i
                    beg_pos_ref = hits[i]
                # Not completely contiguous
                else:
                    # Compute the size of insertion
                    insert_tmp = max(i - (prev_pos_read + k),
                                     hits[i] - (prev_pos_ref + k))
                    if insert_tmp > 0:
                        # Add this insert for this hit
                        insert.append(insert_tmp)
                # Set both prev_pos to current_pos
                prev_pos_read = i
                prev_pos_ref = hits[i]
            # Add the last one
            size = prev_pos_read - beg_pos_read + k
            match = Match(beg_pos_read, beg_pos_ref, strand, ref, size, insert,
                          len(self.sequence))
            # Add the match
            self.add_a_match(match)

    def get_breakpoints(self):
        """ Populate breakpoints list using all hits, for both strands """
        # Sort matches by position on the read
        matches = sorted(self.matches, key=attrgetter('beg_pos_read'))
        # If there is more than one match on this read
        if len(matches) > 1:
            # breakpoints are everything between two matches
            for i in range(1, len(matches)):
                # Starting  pos of bp is the ending pos of previous match
                # Warning, end_pos_read can be greater than beg_pos of
                # current match (overlapping reads). Breakpoint is then
                # of negative size.
                #start_bp = min(matches[i-1].end_pos_read,
                #               matches[i].beg_pos_read)
                start_bp = matches[i-1].end_pos_read
                # Size of bp is position of current match minus
                # ending pos of previous match
                # Warning, it can be negative (overlapping reads)
                size_bp = matches[i].beg_pos_read - matches[i-1].end_pos_read
                # Create the breakpoint
                break_point = Breakpoint(start_bp, size_bp)
                # Add it to breakpoint list for this read
                if break_point not in self.breakpoints:
                    self.breakpoints.append(break_point)


class Match:
    """Define a match.

    :param beg_pos_read: starting position in the read of this match
    :param beg_pos_ref: starting position in the ref of this match
    :param strand: strand of this match
    :param ref: the ref index for this match
    :param size: size of the match
    :param inserts: size of potential insertions (possible to have several insertions in ONE match)
    :param seq_l: size of the read (needed for rev comp computation)
    :type beg_pos_read: int
    :type beg_pos_ref: int
    :type strand: int
    :type ref: int
    :type size: int
    :type inserts: list(int)
    :type seq_l: int
    """
    def __init__(self, beg_pos_read, beg_pos_ref, strand, ref, size, inserts, \
                 seq_l):
        self.ref = ref
        self.strand = strand # 0 -> normal / 1 -> rc
        # Compute ending position on the read (not that useful anymore)
        # Normal strand, direct
        if self.strand == 0:
            self.beg_pos_read = beg_pos_read
            self.end_pos_read = beg_pos_read + size
        # Reverse complement: use total length of the read
        else:
            self.beg_pos_read = seq_l - size - beg_pos_read
            self.end_pos_read = seq_l - beg_pos_read
        # Positions on the ref
        self.beg_pos_ref = beg_pos_ref
        self.end_pos_ref = beg_pos_ref + size
        # Size of the match
        self.size = size
        # Potential insertions
        if not inserts:
            # No insertion
            self.inserts = [0]
        else:
            self.inserts = inserts

    # self representation for print
    def __repr__(self):
        return repr((self.strand, self.beg_pos_read, self.end_pos_read,
                     self.beg_pos_ref, self.end_pos_ref, self.size,
                     self.inserts, self.ref))

    # Equality between two Matches
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def is_include_in(self, other):
        """ Check if this match is included in another match

        :param other: the match to compare with
        :type other: :py:class:`Match`
        """
        ret = False
        if self.beg_pos_read >= other.beg_pos_read and\
           self.end_pos_read <= other.end_pos_read:
            ret = True
        return ret

    def output_read(self, sep):
        """ Correct output of read infos

        :param sep: Separator to use in CSV
        :type sep: list(char)
        """
        # Reverse complement
        if self.strand:
            # Add ref
            ret = "(-)"
        else:
            ret = "(+)"
        # Match info
        ret += "({}){}{}{}".format(self.ref, self.beg_pos_read,
                                   sep[0], self.size)
        return ret

    def output_ref(self, sep):
        """ Correct output of ref infos

        :param sep: Separator to use in CSV
        :type sep: list(char)
        """
        return "({}){}{}{}".format(self.ref, self.beg_pos_ref,
                                   sep[0], self.size)


class Breakpoint:
    """Define a breakpoint.

    :param beg_pos_read: starting position in the read of this match
    :param size: size of the match
    :type beg_pos_read: int
    :type beg_pos_ref: int
    :type size: int
    """
    def __init__(self, beg_pos_read, size):
        self.beg_pos_read = beg_pos_read
        # Size of the match
        self.size = size

    # self representation for print
    def __repr__(self):
        return repr((self.beg_pos_read, self.size))

    # Equality between two Matches
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def output(self, sep):
        """ Proper output of a line in the result file

        :param sep: Separator to use in CSV
        :type sep: list(char)
        """
        return str(self.beg_pos_read) + sep[0] + str(self.size)
