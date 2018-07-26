from __future__ import print_function
from os import path
import sys
import pytest

sys.path.insert(0, path.dirname(sys.path[0]))

from sam_alignment_reconstructor.pairwise import pairwise_alignment

alignments = [("ATAGCTCTCAGC", "6M14N1I5M", "11", "ATAGCT..............-TCAGC", "||||||               |||||", "ATAGCT..............CTCAGC"),
              ("CTTATATTGGCCTT", "3=1X4=2X4=", "3C4AT4", "CTTCTATTATCCTT", "|||:||||::||||", "CTTATATTGGCCTT")
    ]

@pytest.mark.parametrize("alignment_data", alignments)
def test_command_line_success(alignment_data):

    ref, matches, seq = pairwise_alignment(alignment_data[0], alignment_data[1], alignment_data[2])

    assert ref == alignment_data[3]
    assert matches == alignment_data[4]
    assert seq == alignment_data[5]
