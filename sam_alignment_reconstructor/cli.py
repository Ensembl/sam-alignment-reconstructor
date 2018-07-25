#!/usr/bin/env python

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

"""

from __future__ import print_function
import sys, os
import click

sys.path.insert(0, os.path.dirname(sys.path[0]))
from sam_alignment_reconstructor.pairwise import pairwise_alignment, split_every
from simplesam import Reader

@click.command()
def main():

    try:
        stdin_text = click.get_text_stream('stdin')
        in_sam = Reader(stdin_text)

        for sam in in_sam:
            ref, matches, seq = pairwise_alignment(sam.seq, sam.cigar, sam['MD'])

            ref_split = list(split_every(50, ref))
            matches_split = list(split_every(50, matches))
            seq_split = list(split_every(50, seq))

            print(sam.qname)
            for idx, val in enumerate(matches_split):
                print(seq_split[idx])
                print(val)
                print(ref_split[idx])
                print("")
    except Exception:
        print("Error, SAM file seems to be invalid")
        sys.exit(-1)

if __name__ == "__main__":
    main()
