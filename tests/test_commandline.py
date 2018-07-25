from __future__ import print_function
from os import path
import sys
import click
from click.testing import CliRunner
import pytest

sys.path.insert(0, path.dirname(sys.path[0]))

from sam_alignment_reconstructor.cli import main
 
test_path = path.dirname(path.realpath(__file__))
package_path = path.dirname(test_path)
script_path = path.join(package_path, 'bin', 'reconstruct_alignment.py')

successful_sam_files = [('test_DS.sam', 'test_DS.out'),
                        ('test_Hend.sam', 'test_Hend.out'),
                        ('test_Hstart.sam', 'test_Hstart.out'),
                        ('test_MD0end.sam', 'test_MD0end.out'),
                        ('test_N.sam', 'test_N.out'),
                        ('test_SI.sam', 'test_SI.out'),
                        ('test_SPI.sam', 'test_SPI.out'),
                        ('test_X=.sam', 'test_X=.out'),
    ]

failure_sam_files = ['test_charstartCIGAR.sam', 'test_D_noMD.sam']

@pytest.mark.parametrize("sam_file", successful_sam_files)
def test_command_line_success(sam_file):
    in_file = open(path.join(test_path, 'sam_files', sam_file[0]), 'r')
    out_file = open(path.join(test_path, 'sam_files', sam_file[1]), 'r+')
    output = out_file.read()
    
    runner = CliRunner()
    result = runner.invoke(main, input=in_file)
    assert not result.exception
    assert result.output == output

@pytest.mark.parametrize("sam_file", failure_sam_files)
def test_command_line_failure(sam_file):
    in_file = open(path.join(test_path, 'sam_files', sam_file), 'r')
    
    runner = CliRunner()
    result = runner.invoke(main, input=in_file)
    assert result.exception
