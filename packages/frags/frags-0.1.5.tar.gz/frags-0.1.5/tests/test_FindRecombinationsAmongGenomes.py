"""Tests for FindRecombinationsAmongGenomes.py"""
import unittest.mock
import os
import pytest
from .context import frags
from frags import FindRecombinationsAmongGenomes
from frags import core
from frags import read

def test_parser():
    """ Test function 'create_parser()'"""
    parser = FindRecombinationsAmongGenomes.create_parser()
    args = parser.parse_args(["-i", "small_good.fa", "-r", "../../fq_files/CV"\
                              "B4_5-Nluc-2C-3.fasta", "-o", "res", "--kmer",
                              "10", "--gap", "2", "-vv", "-p", "4"])
    assert args.inputfiles == ["small_good.fa"]
    assert args.reffiles == ["../../fq_files/CVB4_5-Nluc-2C-3.fasta"]
    assert args.outputfolder == "res"
    assert args.kmer == 10
    assert args.gap == 2
    assert args.processes == 4
    assert args.verbose == 2
    assert not args.quiet

    args = parser.parse_args(["-i", "g.fa", "-r", "3.fa", "-o", "res", "-b",
                              "-t", "host.fa", "-m", "5"])
    assert args.blast
    assert args.host == "host.fa"
    assert args.minsizeblast == 5

    args = parser.parse_args(["-i", "g.fa", "-r", "3.fa", "-o", "res",
                              "-s", "%", "-f", "/", "-c", ","])
    assert args.posizesep == "%"
    assert args.fieldsep == "/"
    assert args.csvsep == ","

    args = parser.parse_args(["-i", "g.fa", "-r", "3.fa", "-o", "res", "-q"])
    assert args.quiet
    assert not args.verbose


def test_main(capsys, tmpdir):
    """ Test the main of FindRecombinationsAmongGenomes """

    # Tmp fasta (multi-line) file with more than one sequence
    fasta_file = tmpdir.join("test.fasta")
    fasta_file.write(">Fake1\nAGTTGTGAACAAGGTGTGAAG\n"\
                     "CACTGGTATCACGGTACCTTTGTGCGCCTGTTTTATCCAC\n"\
                     "CCGGTATCGCGGTACCCTTGTACGCCTGTT\n"\
                     ">Fake2\nTTGTGGTGTGTTGG\n"\
                     ">Fake3\nGGTGAGGTCGTATAGACTGTTACCCACGGTT\n"\
                     ">Fake4\nAGGTGTGAAGAGCCTATTGAGCTACATGAG")

    # Tmp ref file
    ref_file = tmpdir.join("ref.fasta")
    ref_file.write(">Ref1\nAGTACACCGGTATCGCGGTACCCTTGTACGCCTGTTTTATACTCCCTTTC"\
        "CCCGTAACTTAGAAGCAATGAAACCAAGTTCAATAGAAAGGGGGTACAAACCAGTACCACCACGAACA"\
        "AGCACTTCTGTCTCCCCGGTGAGGTCGTATAGACTGTTCCCACGGTTGAAAATGACTGATCCGTTATC"\
        "CGCTCTTGTACTTCGAGA\n")

    # Tmp ref file 2
    ref_file2 = tmpdir.join("ref2.fasta")
    ref_file2.write(">Ref2\nCGCTAGTTGTGAACAAGGTGTGAAGAGCCTATTGAGCTACATGAGAG\n")

    # Tmp ref file 3
    ref_file3 = tmpdir.join("ref3.fasta")
    ref_file3.write(">Ref3|NC_000001.11_cds_NP_001005221.2_4~[gene=OR4F29]~[d"\
                    "b_xref=CCDS:CCDS72675.1,GeneID:729759]~[protein=olfactor"\
                    "y~receptor~4F3/4F16/4F29]~[protein_id=NP_001005221.2]~[l"\
                    "ocation=complement(450740..451678)]~[gbkey=CDS]\nTTAAAAC"\
                    "AGCCTGTGGGTTGTTCCCTCCCACAGGGCCCAGTGGGCGCTAGCACACTGGTATCA"\
                    "CGGTACCTTTGTGCGCCTGTTTTATCCACCCTACCCCAGAGAAACTTAGAAGCTTA"\
                    "ATCTAAACGGTCAGTAGGAAACCCAGTACACCAACTGGGTCATGACCAAGC\n")

    # Tmp ref wrong file 4
    ref_file4 = tmpdir.join("ref4.fasta")
    ref_file4.write("ZATATATATTATATTATATATATATATTTATATATATATATATTATAT\n")

    # Tmp out folder
    output_folder = tmpdir.mkdir("res")

    # Test whiteout input file
    with unittest.mock.patch("sys.argv", ["test", "-i", "pwet", "-r",
                                              str(ref_file), "-o",
                                              str(output_folder)]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            FindRecombinationsAmongGenomes.main()
            assert pytest_wrapped_e.type == SystemExit
            assert pytest_wrapped_e.value.code == 1
            captured = capsys.readouterr()
            assert "Error, file pwet not found\n" \
                   in captured.out

    # Test whiteout ref file
    with unittest.mock.patch("sys.argv", ["test", "-i", str(fasta_file),
                                              "-r", "pwet", "-o",
                                              str(output_folder)]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            FindRecombinationsAmongGenomes.main()
            assert pytest_wrapped_e.type == SystemExit
            assert pytest_wrapped_e.value.code == 1
            captured = capsys.readouterr()
            assert "Error, file pwet not found\n" \
                   in captured.out

    # Test with non existing output folder
    fake_folder = "/pwet"
    with unittest.mock.patch("sys.argv", ["test", "-i", str(fasta_file), "-r",
                                          str(ref_file), "-o",
                                          str(output_folder) + fake_folder]):
        FindRecombinationsAmongGenomes.main()
    captured = capsys.readouterr()
    assert "Folder {}/ created\n".format(str(output_folder) + fake_folder) \
           in captured.out

    # Test with Blast on but no host file
    with unittest.mock.patch("sys.argv", ["test", "-i", str(fasta_file), "-r",
                                          str(ref_file), "-b", "-o",
                                          str(output_folder)]):
        with pytest.raises(SystemExit):
            FindRecombinationsAmongGenomes.main()
            captured = capsys.readouterr()
            assert "argument -b/--blast: argument -t/--host is required" \
                in captured.out

    # Not a valid host file
    with unittest.mock.patch("sys.argv", ["test", "-i", str(fasta_file), "-r",
                                          str(ref_file), "-b", "-t",
                                          "pwet.fa", "-o",
                                          str(output_folder), "-k", "4"]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            FindRecombinationsAmongGenomes.main()
            assert pytest_wrapped_e.type == SystemExit
            assert pytest_wrapped_e.value.code == 1
            captured = capsys.readouterr()
            assert "Error, host file pwet.fa not found" \
                   in captured.out

    # Not a valid host file
    with unittest.mock.patch("sys.argv", ["test", "-i", str(fasta_file), "-r",
                                          str(ref_file), "-b", "-t",
                                          str(ref_file4), "-o",
                                          str(output_folder), "-k", "4"]):
        FindRecombinationsAmongGenomes.main()
        captured = capsys.readouterr()
        assert "Error: 'makeblastdb' command for creating Blast database "\
               "failed. Disabling Blast step." in captured.out

    # Test with negative number of proc
    fake_folder = "/pwet"
    with unittest.mock.patch("sys.argv", ["test", "-i", str(fasta_file), "-r",
                                          str(ref_file), "-p", "-2", "-o",
                                          str(output_folder) + fake_folder]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            FindRecombinationsAmongGenomes.main()
            assert pytest_wrapped_e.type == SystemExit
            assert pytest_wrapped_e.value.code == 1
            captured = capsys.readouterr()
            assert "argument -p/--processes should be greater than 0" \
                   in captured.out

    # Too much ref files
    with unittest.mock.patch("sys.argv", ["test", "-i", str(fasta_file), "-r",
                                          str(ref_file), str(ref_file2),
                                          str(ref_file3), "-o",
                                          str(output_folder), "-k", "4"]):
        FindRecombinationsAmongGenomes.main()
    captured = capsys.readouterr()
    assert "You can only input 2 references, file {} will be ignored"\
           "\n".format(str(ref_file3)) in captured.out


    # Everything is good
    with unittest.mock.patch("sys.argv", ["test", "-i", str(fasta_file), "-r",
                                          str(ref_file), str(ref_file2), "-b",
                                          "-m", "4", "-t", str(ref_file3),
                                          "-v", "-o", str(output_folder), "-k",
                                          "20"]):
        FindRecombinationsAmongGenomes.main()

    # Verify all outputed files
    # Res for ref_file
    with open(os.path.join(output_folder, "ref.csv")) as res_file:
        assert res_file.read() == "Read_header\tReverse_complement\t"\
                                  "Number_of_breakpoints\t"\
                                  "Breakpoints_positions\t"\
                                  "Matches_read_positions\t"\
                                  "Matches_ref_positions\tMatches_size\t"\
                                  "Insertions\tBlast_results_breakpoints\n"\
                                  ">Fake3\t0\t0\tNone\t(+)(1)0:21\t(1)135:21"\
                                  "\t21\t0\tNone\n"

    # Res for ref_file2
    with open(os.path.join(output_folder, "ref2.csv")) as res_file:
        assert res_file.read() == "Read_header\tReverse_complement\t"\
                                  "Number_of_breakpoints\t"\
                                  "Breakpoints_positions\t"\
                                  "Matches_read_positions\t"\
                                  "Matches_ref_positions\tMatches_size\t"\
                                  "Insertions\tBlast_results_breakpoints\n"\
                                  ">Fake4\t0\t0\tNone\t(+)(2)0:30\t(2)15:30\t"\
                                  "30\t0\tNone\n"

    # Res for both ref files
    with open(os.path.join(output_folder, "ref_and_ref2.csv")) as res_file:
        assert res_file.read() == "Read_header\tReverse_complement\t"\
                                  "Number_of_breakpoints\t"\
                                  "Breakpoints_positions\t"\
                                  "Matches_read_positions\t"\
                                  "Matches_ref_positions\tMatches_size\t"\
                                  "Insertions\tBlast_results_breakpoints\n"\
                                  ">Fake1\t0\t1\t21:40\t"\
                                  "(+)(2)0:21|(+)(1)61:30\t(2)4:21|(1)6:30\t"\
                                  "21|30\t0|0\t1\n"
    # Res for unmatched.csv
    with open(os.path.join(output_folder, "unmatched.csv")) as res_file:
        assert res_file.read() == ">Fake2\n"

    # Res for breaklpoints
    with open(os.path.join(output_folder, "breakpoints.fasta")) as res_file:
        assert res_file.read() == ">Fake1_1\nCACTGGTATCACGGTACCTTTGTGCGCCTGTT"\
                                  "TTATCCAC\n"
    # Res for compressed blast result
    with open(os.path.join(output_folder, "compressed.fasta")) as res_file:
        assert res_file.read() == ">Fake1_1|1.44e-19|75.0\nRef3|NC_000001.11_"\
                                  "cds_NP_001005221.2_4~[gene=OR4F29]~[db_xre"\
                                  "f=CCDS:CCDS72675.1,GeneID:729759]~[protein"\
                                  "=olfactory~receptor~4F3/4F16/4F29]~[protei"\
                                  "n_id=NP_001005221.2]\n"
    # Res for Blast
    with open(os.path.join(output_folder, "res_blast.csv")) as res_file:
        assert res_file.read() == "Fake1_1\tRef3|NC_000001.11_cds_NP_00100522"\
                                  "1.2_4~[gene=OR4F29]~[db_xref=CCDS:CCDS7267"\
                                  "5.1,GeneID:729759]~[protein=olfactory~rece"\
                                  "ptor~4F3/4F16/4F29]~[protein_id=NP_0010052"\
                                  "21.2]~[location=complement(450740..451678)"\
                                  "]~[gbkey=CDS]\t1.44e-19\t75.0\n"

def test_init():
    """ Test __main__ """
    with unittest.mock.patch.object(FindRecombinationsAmongGenomes, "main", return_value=0):
        with unittest.mock.patch.object(FindRecombinationsAmongGenomes, "__name__", "__main__"):
            with unittest.mock.patch.object(FindRecombinationsAmongGenomes.sys, "exit") as mock_exit:
                FindRecombinationsAmongGenomes.init()
                assert mock_exit.call_args[0][0] == 0
