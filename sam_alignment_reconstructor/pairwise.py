"""
Copyright [2016-2018] EMBL-European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Reconstruct a pairwaise alignment from a "read", the cigar string
and md:z tag from a SAM file line.

"""

import re
from itertools import groupby, islice

# Globals for parsing the CIGAR string

# https://github.com/samtools/hts-specs/blob/da805be01e2ceaaa69fdde9f33c5377bf9ee6369/SAMv1.tex#L383
# operations that consume the reference
_cigar_ref = set(('M', 'D', 'N', '=', 'X', 'EQ'))
# operations that consume the query
_cigar_query = set(('M', 'I', 'S', '=', 'X', 'EQ'))
# operations that do not represent an alignment
_cigar_no_align = set(('H', 'P'))
_valid_cigar = _cigar_ref | _cigar_query | _cigar_no_align
# operations that can be represented as aligned to the reference
_cigar_align = _cigar_ref & _cigar_query
# operations that only consume the reference
_cigar_ref_only = _cigar_ref - _cigar_align
# operations that only consume the query
_cigar_query_only = _cigar_query - _cigar_align

def pairwise_alignment(read, cigar, mdz):
    """
    Return the original pairwise alignment for a
    read given a sequence, cigar string and md:z tag

    Parameters:
    read - The sequence for the read
    cigar - A cigarplus string
    mdz - An MD:Z tag string
    """

    seq_pos = 0
    mdz_pos = 0
    reads = list(read)
    expanded_cigar = cigar_expand(cigar)
    expanded_mdz = mdz_expand(mdz)

    ref = []
    seq = []
    match_str = []

    for _, op in enumerate(expanded_cigar):

        if op == 'H':
            # For hard masking, we skip over that
            continue

        elif op == 'M':

            if expanded_mdz[mdz_pos]:
                ref.append(expanded_mdz[mdz_pos])
                match_str.append(':')
            else:
                ref.append(reads[seq_pos])
                match_str.append('|')
            seq.append(reads[seq_pos])
            seq_pos += 1
            mdz_pos += 1

        elif op == 'I':

            ref.append('-')
            seq.append(reads[seq_pos])
            match_str.append(' ')
            seq_pos += 1

        elif op == 'D':

            ref.append(expanded_mdz[mdz_pos])
            seq.append('-')
            match_str.append(' ')
            mdz_pos += 1

        elif op == 'X':

            ref.append(expanded_mdz[mdz_pos])
            seq.append(reads[seq_pos])
            match_str.append(':')
            seq_pos += 1
            mdz_pos += 1

        elif op == '=':

            ref.append(reads[seq_pos])
            seq.append(reads[seq_pos])
            match_str.append('|')
            seq_pos += 1
            mdz_pos += 1

        elif op == 'N':

            ref.append('.')
            seq.append('.')
            match_str.append(' ')

        elif op == 'S':

            ref.append('.')
            seq.append(reads[seq_pos].lower())
            match_str.append(' ')
            seq_pos += 1

        elif op == 'P':

            ref.append('*')
            seq.append('*')
            match_str.append(' ')

    return ''.join(ref), ''.join(match_str), ''.join(seq)

def cigar_expand(cigar):
    """
    Expand the CIGAR string in to a character map of the
    alignment.

    eg. 6M3I2M

    MMMMMMIIIMM

    """
    mapping = []

    for c, op in cigar_split(cigar):
        mapping.extend([op] * c)

    return mapping

def cigar_split(cigar):
    """
    Split the CIGAR string in to (num, op) tuples

    """
    # https://github.com/brentp/bwa-meth
    if cigar == "*":
        yield (0, None)
        return
    cig_iter = groupby(cigar, lambda c: c.isdigit())
    for _, n in cig_iter:
        op = int("".join(n)), "".join(next(cig_iter)[1])
        if op[1] in _valid_cigar:
            yield op
        else:
            raise ValueError("CIGAR operation %s in record %s is invalid." % (op[1], cigar))

def mdz_expand(mdz):
    """
    Expands the MD:Z tag in to a character map of the base changes
    """
    pairs = mdz_split(mdz)

    expanded_mdz = []

    for p in pairs:
        expanded_mdz.extend([None] * p[0])
        expanded_mdz.extend(list(p[1]))

    return expanded_mdz


def mdz_split(mdz):
    """
    Splits the MD:Z string in to (num, op) tuples
    """
#    md_match = re.findall(r"([0-9]+)(\^?[A-Z]+)?", mdz)
    md_match = re.findall(r"([0-9]+)\^?([A-Z]+)?", mdz)

    pairs = [(int(i), b) for i, b in md_match]

    return pairs

def split_every(n, iterable):
    """
    Splits an iterable every n objects

    eg. split a string every 50 characters

    Returns a list of the iterable object pieces
    """
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield ''.join(piece)
        piece = list(islice(i, n))
