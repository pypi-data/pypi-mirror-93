"""Functional tests for FRAG.py"""

import os
import pytest
import unittest.mock
from collections import defaultdict
from shutil import copyfile
from frags import FindRecombinationsAmongGenomes
from .context import frags

def test_main(tmpdir, capsys):
    """ Test the functional behavior of FRAG """

    # Output folder
    output_folder = tmpdir.mkdir("res_functional_tests")

    # Genome A file
    ref_a = tmpdir.join("A.fasta")
    ref_a.write(">Genome1\nTTAAAACAGCCTGTGGGTTGTTCCCTCCCACAGGGCCCAGTGGGCGCTAG"\
                "CACACTGGTATCACGGTACCTTTGTGCGCCTGTTTTATCCACCCTACCCCAGAGAAACTT"\
                "AGAAGCTTAATCTAAACGGTCAGTAGGAAACCCAGTACACCAACTGGGTCATGACCAAGC"\
                "ACTTCTGTAACCCCGGACTGAGTATCAATAAGCTGCTCACGTGGCTGAAGGAGAAAACGT"\
                "TCGTTATCCGGCCAATTACTTCGAGAAACCTAGTACCACCATGAAAGTTGCGCAGCGTTT"\
                "CGTTCCGCACAACCCCAGTGTAGATCAGGCCGATGAGTCACCGCGTTCCCCACGGGCGAC"\
                "CGTGGCGGTGGCTGCGTTGGCGGCCTGCCCATGGGGCAACCCATGGGACGCCTCAATACT"\
                "GACATGGTGCGAAGAGTCTATTGAGCTAATTGGTAGTCCTCCGGCCCCTGAATGCGGCTA"\
                "ATCCCAACTGCGGAGCAGATACCCACATGCCAGTGGGCAGTCTGTCGTAACGGGCAACTC"\
                "TGCAGCGGAACCGACTACTTTGGGTGTCCGTGTTTCCTGTTATTCTTATACTGGCTGCTT"\
                "ATGGTGACAATTGAGAGATTGTTACCATATAGCTATTGGATTGGCCATCCGGTATCTAAC"\
                "AGGGCAATCATTTATCTGTTTGTTGGGTTTGTACCCTTGAATTTTAAAGTTCTCAAAACA"\
                "CTCAACCTTGTCTTACAATTTAATTCAGCAAAATGGTCTTCACACTCGAAGATTTCGTTG"\
                "GGGACTGGCGACAGACAGCCGGCTACAACCTGGACCAAGTCCTTGAACAGGGAGGTGTGT"\
                "CCAGTTTGTTTCAGAATCTCGGGGTGTCCGTAACTCCGATCCAAAGGATTGTCCTGAGCG"\
                "GTGAAAATGGGCTGAAGATCGACATCCATGTCATCATCCCGTATGAAGGTCTGAGCGGCG"\
                "ACCAAATGGGCCAGATCGAAAAAATTTTTAAGGTGGTGTACCCTGTGGATGATCATCACT"\
                "TTAAGGTGATCCTGCACTATGGCACACTGGTAATCGACGGGGTTACGCCGAACATGATCG"\
                "ACTATTTCGGACGGCCGTAGCGGCCTACCTGTGGCCCAAAGCCACAGGACGCTAGTTGTG"\
                "AACAAGGTGTGAAGGCATCGCCGTGTTCGACGGCAAAAAGATCACTGTAACAGGGACCCT"\
                "GTGGAACGGCAACAAAATTATCGACGAGCGCCTGATCAACCCCGACGGCTCCCTGCTGTT"\
                "CCGAGTAACCATCAACGGAGTGACCGGCTGGCGGCTGTGCGAACGCATTCTGGCGTAGAA"\
                "CAACGGCTGGCTGAAGAAGTTCACCGAAATGACCAACGCCTGCAAGGGCATGGAATGGAT"\
                "TGCCATTAAAATTCAGAAATTTATTGAATGGCTCAAGGTTAAAATCCTGCCAGAAGTGAG"\
                "AGAGAAGCATGAATTTCTTAACAGACTAAAGCAATTACCATTCCTTGAAAGCCAGATTGC"\
                "CACCATTGAACAAAGTGCGCCCTCACAAAGTGACCAGGAGCAGCTTTTTTCAAATGTCCA"\
                "GTACTTCGCCCACTACTGCAGAAAGTACGCCCCCTTGTACGCCGCTGAAGCAAAAAGAGT"\
                "GTTCTCGCTAGAAAAGAAGATGAGCAATTACATACAGTTCAAGTCCAAATGCCGTATTGA"\
                "ACCTGTATGCTTACTCCTCCATGGCAGCCCAGGAGCTGGCAAATCGGTGGCCACTAACCT"\
                "AATAGGGAGATCCCTCGCGGAGAAGCTAAATAGCTCCGTGTACTCCCTACCGCCAGATCC"\
                "AGATCACTTTGATGGGTATAAACAACAAGCGGTAGTGATTATGGATGATCTGTGCCAGAA"\
                "CCCCGATGGGAAGGACGTGTCACTGTTCTGCCAAATGGTCTCTAGCGTGGACTTTGTGCC"\
                "ACCCATGGCGGCACTAGAAGAGAAAGGAATCCTTTTCACCTCCCCATTTGTGCTAGCCTC"\
                "AACCAATGCTGGGTCTATCAATGCGCCCACAGTGTCAGACAGCAGAGCGCTTGCTAGAAG"\
                "ATTCCACTTTGACATGAATATTGAAGTCATCTCCATGTACAGCCAGAACGGGAAAATTAA"\
                "CATGCCTATGTCTGTTAAGACATGTGATGAGGAGTGTTGCCCAGCCAACTTTAAGAAGTG"\
                "CTGCCCATTGGTTTGCGGTAAGGCTATTCAATTCATTGACAGGAGAACACAGGTCAGATA"\
                "CTCACTGGACATGTTGGTTACTGAAATGTTCAGAGAGTACAATCACAGACACAGCGTAGG"\
                "CGCCACTCTTGAAGCTTTATTTCAATGAAATTAGAGCACAATTATAGAGCCACAATTGGC"\
                "TTAACCCTACCGCATTAACCGAACTTGACAAAAGTGCGGTAGGGGTAAATTCTCCGCATT"\
                "CGGTGCGGAAAAAAAAAAAAAAAAAAAAAAAAA")

    # Genome B file
    ref_b = tmpdir.join("B.fasta")
    ref_b.write(">Genome_2\nTTAAAACAGCTCTGGGGTTGTTCCCACCCCAGAGGCCCACGTGGCGGCC"\
        "AGTACACCGGTATCGCGGTACCCTTGTACGCCTGTTTTATACTCCCTTTCCCCGTAACTTAGAAGCAA"\
        "TGAAACCAAGTTCAATAGAAAGGGGGTACAAACCAGTACCACCACGAACAAGCACTTCTGTCTCCCCG"\
        "GTGAGGTCGTATAGACTGTTCCCACGGTTGAAAATGACTGATCCGTTATCCGCTCTTGTACTTCGAGA"\
        "AGCCTAGTACCACCTTGGAATCTTCGATGCGTTGCGCTCAGCACTCAACCCCGGAGTGTAGCTTGGGC"\
        "TGATGAGTCTGGACATTCCCCACCGGCGACGGTGGTCCAGGCTGCGTTGGCGGCCTACCTGTGGCCCA"\
        "AAGCCACAGGACGCTAGTTGTGAACAAGGTGTGAAGAGCCTATTGAGCTACATGAGAGTCCTCCGGCC"\
        "CCTGAATGCGGCTAATCCCAACCACGGAGCAGGCGATTGCAATCCAGCAATTAGCCTGTCGTAACGCG"\
        "TAAGTCTGTGGCGGAACCGACTACTTTGGGTGACCGTGTTTCCTTTTATTCTTACATTGGCTGCTTAT"\
        "GGTGACAATCATAGATTGTTATCATAAAGCGAGTTGGATTGGCCATCCAGTGAGAATTAGATCGATCA"\
        "TCTACCTTTTTGTTGGATTTACACCTTTAAAACCACACAGCTTGAATCTCATCAAAATTGTATTGTTG"\
        "ATACGACATTATTATCATT")

    # Host genome
    h_file = tmpdir.join("host.fasta")
    h_file.write(">lcl|NC_000001.11_cds_NP_001005484.1_1~[gene=OR4F5]~[db_xre"\
                 "f=CCDS:CCDS30547.1,GeneID:79501]~[protein=olfactory~recepto"\
                 "r~4F5]~[protein_id=NP_001005484.1]~[location=69091..70008]~"\
                 "[gbkey=CDS]\nATGGTGACTGAATTCATTTTTCTGGGTCTCTCTGATTCTCAGGAAC"\
                 "TCCAGACCTTCCTATTTATGTTGTTTTTTGTATT\nCTATGGAGGAATCGTGTTTGGAA"\
                 "ACCTTCTTATTGTCATAACAGTGGTATCTGACTCCCACCTTCACTCTCCCATGTACT\n"\
                 "TCCTGCTAGCCAACCTCTCACTCATTGATCTGTCTCTGTCTTCAGTCACAGCCCCCAAG"\
                 "ATGATTACTGACTTTTTCAGC\nCAGCGCAAAGTCATCTCTTTCAAGGGCTGCCTTGTT"\
                 "CAGATATTTCTCCTTCACTTCTTTGGTGGGAGTGAGATGGTGAT\nCCTCATAGCCATG"\
                 "GGCTTTGACAGATATATAGCAATATGCAAGCCCCTACACTACACTACAATTATGTGTGG"\
                 "CAACGCAT\nGTGTCGGCATTATGGCTGTCACATGGGGAATTGGCTTTCTCCATTCGGT"\
                 "GAGCCAGTTGGCGTTTGCCGTGCACTTACTC\nTTCTGTGGTCCCAATGAGGTCGATAG"\
                 "TTTTTATTGTGACCTTCCTAGGGTAATCAAACTTGCCTGTACAGATACCTACAG\nGCT"\
                 "AGATATTATGGTCATTGCTAACAGTGGTGTGCTCACTGTGTGTTCTTTTGTTCTTCTAA"\
                 "TCATCTCATACACTATCA\nTCCTAATGACCATCCAGCATCGCCCTTTAGATAAGTCGT"\
                 "CCAAAGCTCTGTCCACTTTGACTGCTCACATTACAGTAGTT\nCTTTTGTTCTTTGGAC"\
                 "CATGTGTCTTTATTTATGCCTGGCCATTCCCCATCAAGTCATTAGATAAATTCCTTGCT"\
                 "GTATT\nTTATTCTGTGATCACCCCTCTCTTGAACCCAATTATATACACACTGAGGAAC"\
                 "AAAGACATGAAGACGGCAATAAGACAGC\nTGAGAAAATGGGATGCACATTCTAGTGTA"\
                 "AAGTTTTAG\n>lcl|NC_000001.11_cds_XP_024307731.1_2~[gene=LOC"\
                 "112268260]~[db_xref=GeneID:112268260]~[protein=uncharacteri"\
                 "zed~protein~LOC112268260~isoform~X2]~[protein_id=XP_0243077"\
                 "31.1]~[location=complement(join(358067..358183,373144..3733"\
                 "23,379769..379870,399041..399100))]~[gbkey=CDS]\nATGGATGACC"\
                 "ATTTCAAACGATCCAGGCTAAGCCAGGAGGAGAGCTCAAAGTCTGATCTGCTCTGCTGC"\
                 "CCCCTGCCCCA\nTACACGTGATGGAGCAGAAAACGTGCTGTGTGAACCTGTGACTTCA"\
                 "GGGCCTGTTGACGTGGTCGTGCTTGCATACTCTC\nTGGACTGGACCTCACTGTGGGAA"\
                 "CAACAAGATCAACAAGAGGAGCAAGAACAACATCAAGAGTCAGGGCCCGGGGGTCCT\n"\
                 "GACGGGTACAGGACGGGTACAGACCCACACAGGAATCCCAGAGTGTGTTCCACAGCAGG"\
                 "CACGCCTGCGCTGAAAGAGT\nGGGCAGAAAGGAGCTGACCTGGACCAAACCAATGCAC"\
                 "AACTCCTACGTACTGATGGTGGTCTTACGTTTCCCTAAGTTTC\nTGCCGACTAAACTG"\
                 "TGCACACGTTCTCAGGACCTCCTGAAGCTGCGTCACAGGCGCTGA\n>lcl|NC_0000"\
                 "01.11_cds_XP_024307730.1_3~[gene=LOC112268260]~[db_xref=Gen"\
                 "eID:112268260]~[protein=uncharacterized~protein~LOC11226826"\
                 "0~isoform~X1]~[protein_id=XP_024307730.1]~[location=complem"\
                 "ent(join(358153..358183,365565..365692,373144..373323,37976"\
                 "9..379870,399041..399100))]~[gbkey=CDS]\nATGGATGACCATTTCAAA"\
                 "CGATCCAGGCTAAGCCAGGAGGAGAGCTCAAAGTCTGATCTGCTCTGCTGCCCCCTGCC"\
                 "CCA\nTACACGTGATGGAGCAGAAAACGTGCTGTGTGAACCTGTGACTTCAGGGCCTGT"\
                 "TGACGTGGTCGTGCTTGCATACTCTC\nTGGACTGGACCTCACTGTGGGAACAACAAGA"\
                 "TCAACAAGAGGAGCAAGAACAACATCAAGAGTCAGGGCCCGGGGGTCCT\nGACGGGTA"\
                 "CAGGACGGGTACAGACCCACACAGGAATCCCAGAGTGTGTTCCACAGCAGGACACGCCT"\
                 "GCGCTGAAAGAGT\nGGGCAGAAAGGAGCTGACCTGGGATTATGATCCAAACTCAGCTG"\
                 "GGCCTCCCCTCCCTGCCCCAGGATTGTGGAGTGAGA\nACGTTGCAGCAGGAGAGAACA"\
                 "ACGCAGCAAAGCACAGCAGGGGAACCGGAAATGCTCACCTTTTGACAGGACCAAACCAA"\
                 "\nTGCACAACTCCTACGTACTGA\n>lcl|NC_000001.11_cds_NP_001005221"\
                 ".2_4~[gene=OR4F29]~[db_xref=CCDS:CCDS72675.1,GeneID:729759]"\
                 "~[protein=olfactory~receptor~4F3/4F16/4F29]~[protein_id=NP_"\
                 "001005221.2]~[location=complement(450740..451678)]~[gbkey=C"\
                 "DS]\nATGGATGGAGAGAATCACTCAGTGGTATCTGAGTTTTTGTTTCTGGGACTCACT"\
                 "CATTCATGGGAGATCCAGCTCCTCCT\nCCTAGTGTTTTCCTCTGTGCTCTATGTGGCA"\
                 "AGCATTACTGGAAACATCCTCATTGTGTTTTCTGTGACCACTGACCCTC\nACTTACAC"\
                 "TCCCCCATGTACTTTCTACTGGCCAGTCTCTCCTTCATTGACTTAGGAGCCTGCTCTGT"\
                 "CACTTCTCCCAAG\nATGATTTATGACCTGTTCAGAAAGCGCAAAGTCATCTCCTTTGG"\
                 "AGGCTGCATCGCTCAAATCTTCTTCATCCACGTCGT\nTGGTGGTGTGGAGATGGTGCT"\
                 "GCTCATAGCCATGGCCTTTGACAGATATGTGGCCCTATGTAAGCCCCTCCACTATCTGA"\
                 "\nCCATTATGAGCCCAAGAATGTGCCTTTCATTTCTGGCTGTTGCCTGGACCCTTGGTG"\
                 "TCAGTCACTCCCTGTTCCAACTG\nGCATTTCTTGTTAATTTAGCCTTCTGTGGCCCTA"\
                 "ATGTGTTGGACAGCTTCTACTGTGACCTTCCTCGGCTTCTCAGACT\nAGCCTGTACCG"\
                 "ACACCTACAGATTGCAGTTCATGGTCACTGTTAACAGTGGGTTTATCTGTGTGGGTACT"\
                 "TTCTTCATAC\nTTCTAATCTCCTACGTCTTCATCCTGTTTACTGTTTGGAAACATTCC"\
                 "TCAGGTGGTTCATCCAAGGCCCTTTCCACTCTT\nTCAGCTCACAGCACAGTGGTCCTT"\
                 "TTGTTCTTTGGTCCACCCATGTTTGTGTATACACGGCCACACCCTAATTCACAGAT\nG"\
                 "GACAAGTTTCTGGCTATTTTTGATGCAGTTCTCACTCCTTTTCTGAATCCAGTTGTCTA"\
                 "TACATTCAGGAATAAGGAGA\nTGAAGGCAGCAATAAAGAGAGTATGCAAACAGCTAGT"\
                 "GATTTACAAGAGGATCTCATAA")

    # Input fastq file to analyze
    f_file = tmpdir.join("functional_tests.fastq")
    f_file.write("@10_insertions_in_contiguous_read\n"\
                 "ATGGTGCGAAGAGTCTATTGAGCTAATTGGTAGTCCTCCGGCCAAACCCTTTGCCTGAA"\
                 "TGCGGCTAATCCCAACTGCGGAGCAGATACCCACATGCCAGTGGGCAGTCT\n"\
                 "+expected_results_A.csv\n"\
                 "10_insertions_in_contiguous_read\t0\t0\tNone\t(+)(1)0:110\t"\
                 "(1)413:110\t110\t10\tNone\n"\
                 "@11_insertions_in_contiguous_read\n"\
                 "ATGGTGCGAAGAGTCTATTGAGCTAATTGGTAGTCCTCCGGCCAAACCCTTTGGCCTGA"\
                 "ATGCGGCTAATCCCAACTGCGGAGCAGATACCCACATGCCAGTGGGCAGTCT\n"\
                 "+expected_results_A.csv\n"\
                 "11_insertions_in_contiguous_read\t0\t1\t43:11\t(+)(1)0:43|"\
                 "(+)(1)54:57\t(1)413:43|(1)456:57\t43|57\t0|0\tNone\n"\
                 "@all_genome_A_with_middle_(GCGGCCTACCTGTGGCCCAAAGCCACAGGACG"\
                 "CTAGTTGTGAACAAGGTGTGAAG)_also_in_B\n"\
                 "TACGCCGAACATGATCGACTATTTCGGACGGCCGTAGCGGCCTACCTGTGGCCCAAAGC"\
                 "CACAGGACGCTAGTTGTGAACAAGGTGTGAAGGCATCGCCGTGTTCGACGGCAAAAAGA"\
                 "TCACTGTAACAGGGACCCTGTGGAACGGCAACAAAATTATCGACGAGCGCCTGATCAAC"\
                 "CCCGACGGCTCCCTGCTGTTCCGAG\n"\
                 "+expected_results_A.csv\n"\
                 "all_genome_A_with_middle_(GCGGCCTACCTGTGGCCCAAAGCCACAGGACGC"\
                 "TAGTTGTGAACAAGGTGTGAAG)_also_in_B\t0\t0\tNone\t(+)(1)0:202"\
                 "\t(1)1053:202\t202\t0\tNone\n"\
                 "@contiguous_on_ref_11_insert_on_read\n"\
                 "CCATGTCATCATCCCGTATGAAGGTCTGAGCGGCGACCAAATGGAAACCCGGGTTGCCA"\
                 "GATCGAAAAAATTTTTAAGGTGGTGTACCCTGTGGATGATCATCACTTTA\n"\
                 "+expected_results_A.csv\n"\
                 "contiguous_on_ref_11_insert_on_read\t0\t1\t44:11\t(+)(1)0:"\
                 "44|(+)(1)55:54\t(1)915:44|(1)959:54\t44|54\t0|0\tNone\n"\
                 "@contiguous_on_read_11_insert_on_ref\n"\
                 "CGCCTGCAAGGGCATGGAATGGATTGCCATTAAAATTCAGAAATTTATTGAATGGCTTC"\
                 "CTGCCAGAAGTGAGAGAGAAGCATGAATTTCTTAACAGACT\n"\
                 "+expected_results_A.csv\n"\
                 "contiguous_on_read_11_insert_on_ref\t0\t1\t57:0\t(+)(1)0:57"\
                 "|(+)(1)57:43\t(1)1346:57|(1)1414:43\t57|43\t0|0\tNone\n"\
                 "@Insert_of_9_and_10_in_same_match\n"\
                 "TCCGGCCCCTGAATGCGGCTAATCCCAACTGCGGAGCAGATACAAACCCGGGCCACATG"\
                 "CCAGTGGGCAGTCTGTCGTAACGGGCAACTCTGCAGCGGAACAAACCCGGGTCGACTAC"\
                 "TTTGGGTGTCCGTGTTTCCTGTTATTC\n"\
                 "+expected_results_A.csv\n"\
                 "Insert_of_9_and_10_in_same_match\t0\t0\tNone\t(+)(1)0:145\t"\
                 "(1)449:145\t145\t9:10\tNone\n"\
                 "@Insert_of_9_and_10_in_diff_matches\n"\
                 "TCCGGCCCCTGAATGCGGCTAATCCCAACTGCGGAGCAGATACaaacccgggCCACATG"\
                 "CCAGTGGGCAGTCTGTCGTAACGGGCAACTCTGCAGCGGAATgcgcgcgcgcgcgcgcg"\
                 "ggcGGGCAGTCTGTCGTAACGGGCAACTCTGCAGCGGAACaaacccgggtCGACTACTT"\
                 "TGGGTGTCCGTGTTTCCTGTTATTC\n"\
                 "+expected_results_A.csv\n"\
                 "Insert_of_9_and_10_in_diff_matches\t0\t1\t100:21\t"\
                 "(+)(1)0:100|(+)(1)121:81\t(1)449:100|(1)504:81\t100|81\t"\
                 "9|10\tNone\n"
                 "@Insert_of_10_and_11_in_read\n"\
                 "TCCGGCCCCTGAATGCGGCTAATCCCAACTGCGGAGCAGATACAAACCCGGGTCCACAT"\
                 "GCCAGTGGGCAGTCTGTCGTAACGGGCAACTCTGCAGCGGAACAAACCCGGGTTCGACT"\
                 "ACTTTGGGTGTCCGTGTTTCCTGTTATTC\n"\
                 "+expected_results_A.csv\n"\
                 "Insert_of_10_and_11_in_read\t0\t1\t102:11\t(+)(1)0:102|(+)"\
                 "(1)113:34\t(1)449:102|(1)541:34\t102|34\t10|0\tNone\n"\
                 "@Half_A_half_B_and_one_common_pos\n"\
                 "AATGGGCTGAAGATCGACATCCATGTCATCATCCCGTATGAAGGTTTCCTTTTATTCTT"\
                 "ACATTGGCTGCTTATGGTGACAATCATA\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "Half_A_half_B_and_one_common_pos\t0\t1\t45:-2\t(+)(1)0:45|"\
                 "(+)(2)43:44\t(1)895:45|(2)562:44\t45|44\t0|0\tNone\n"\
                 "@Half_A_half_B_plus_4_inserts\n"\
                 "AATGGGCTGAAGATCGACATCCATGTCATCATCCCGTATGAAGTTTTTGTTTCCTTTTA"\
                 "TTCTTACATTGGCTGCTTATGGTGACAATCATA\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "Half_A_half_B_plus_4_inserts\t0\t1\t43:4\t(+)(1)0:43|(+)(2)"\
                 "47:45\t(1)895:43|(2)561:45\t43|45\t0|0\tNone\n"\
                 "@Half_A_half_B_in_rc\n"\
                 "AATGGGCTGAAGATCGACATCCATGTCATCATCCCGTATGAAGTATGATTGTCACCATA"\
                 "AGCAGCCAATGTAAGAATAAAAGGAAAC\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "Half_A_half_B_in_rc\t2\t1\t43:0\t(+)(1)0:43|(-)(2)43:44\t"\
                 "(1)895:43|(2)562:44\t43|44\t0|0\tNone\n"\
                 "@Half_A_half_B_in_rc_plus_3_inserts\n"\
                 "AATGGGCTGAAGATCGACATCCATGTCATCATCCCGTATGAAGTATTATGATTGTCACC"\
                 "ATAAGCAGCCAATGTAAGAATAAAAGGAAAC\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "Half_A_half_B_in_rc_plus_3_inserts\t2\t1\t43:3\t(+)(1)0:43|"\
                 "(-)(2)46:44\t(1)895:43|(2)562:44\t43|44\t0|0\tNone\n"\
                 "@Half_A_in_rc_half_B_in_rc\n"\
                 "GCTTCAGCGGCGTACAAGGGGGCGTACTTTCTGCAGTAGTGGGCGAAGTACTGGAGTAG"\
                 "ATGATCGATCTAATTCTCACTGGATGGCCAATCCAACTC\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "Half_A_in_rc_half_B_in_rc\t1\t1\t55:0\t(-)(1)0:55|(-)(2)55:"\
                 "43\t(1)1546:55|(2)623:43\t55|43\t0|0\tNone\n"\
                 "@Half_A_in_rc_half_B_in_rc_plus_3_inserts\n"\
                 "GCTTCAGCGGCGTACAAGGGGGCGTACTTTCTGCAGTAGTGGGCGAAGTACTGGATGTG"\
                 "TAGATGATCGATCTAATTCTCACTGGATGGCCAATCCAACTC\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "Half_A_in_rc_half_B_in_rc_plus_3_inserts\t1\t1\t55:3\t"\
                 "(-)(1)0:55|(-)(2)58:43\t(1)1546:55|(2)623:43\t55|43\t0|0\t"\
                 "None\n"\
                 "@A_partially_rc\n"\
                 "GTCACTCCGTTGATGGTTACTCGGAACAGCAGGGAGCCGTCGGGGTTGATCAGGCGCTC"\
                 "GGATTGGCCATCCGGTATCTAACAGGGCAATCATTTATCTGTT\n"\
                 "+expected_results_A.csv\n"\
                 "A_partially_rc\t2\t1\t60:-1\t(-)(1)0:60|(+)(1)59:43\t(1)"\
                 "1214:60|(1)627:43\t60|43\t0|0\tNone\n"\
                 "@A_then_2_B_in_rc\n"\
                 "TGTGAACAAGGTGTGAAGGCATCGCCGTGTTCGACGGCAACCAACGCAGCCTGGACCAC"\
                 "CGTCGCCGGTGGGGAACACAGACTTACGCGTTACGACAGGCTAATTGCTGGATTGC\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "A_then_2_B_in_rc\t2\t2\t40:0|75:0\t(+)(1)0:40|(-)(2)40:35|"\
                 "(-)(2)75:40\t(1)1126:40|(2)336:35|(2)495:40\t40|35|40\t"\
                 "0|0|0\tNone\n"\
                 "@Nothing\n"\
                 "AGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGGAGAGAGAGAGAGAGAGA\n"\
                 "+expected_results_unmatched.csv\n"\
                 "Nothing\n"
                 "@A_then_Blast_then_B_then_Blast_then_B\n"\
                 "ATCACTTTGATGGGTATAAACAACAAGCGGTAGTGATTAACAAGAGGAGCAAGAACAAC"\
                 "ATCAAGAGTCAGGGCTGGAATCTTCGATGCGTTGCGCTCAGCACTCAACCCCCTTCTTA"\
                 "TTGTCATAACAGTGGTATCTGACTCCCACCTTCAATTGTTATCATAAAGCGAGTTGGAT"\
                 "TGGCCATCCAGTGAGAAT\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "A_then_Blast_then_B_then_Blast_then_B\t0\t2\t39:35|111:41\t"\
                 "(+)(1)0:39|(+)(2)74:37|(+)(2)152:43\t(1)1792:39|(2)268:37|"\
                 "(2)607:43\t39|37|43\t0|0|0\t1|2\n")

    # Input fastq file to analyze with error
    false_file = tmpdir.join("false_functional_tests.fastq")
    false_file.write("@10_insertions_in_contiguous_read\n"\
                 "ATGGTGCGAAGAGTCTATTGAGCTAATTGGTAGTCCTCCGGCCAAACCCTTTGCCTGAA"\
                 "TGCGGCTAATCCCAACTGCGGAGCAGATACCCACATGCCAGTGGGCAGTCT\n"\
                 "+expected_results_A.csv\n"\
                 "10_insertions_in_contiguous_read\t0\t0\tNone\t(+)(1)0:110\t"\
                 "(1)413:110\t110\t10\tNone\n"\
                 "?11_insertions_in_contiguous_read\n"\
                 "ATGGTGCGAAGAGTCTATTGAGCTAATTGGTAGTCCTCCGGCCAAACCCTTTGGCCTGA"\
                 "ATGCGGCTAATCCCAACTGCGGAGCAGATACCCACATGCCAGTGGGCAGTCT\n"\
                 "+expected_results_A.csv\n"\
                 "11_insertions_in_contiguous_read\t0\t1\t43:11\t(+)(1)0:43|"\
                 "(+)(1)54:57\t(1)413:43|(1)456:57\t43|57\t0|0\tNone\n"\
                 "@A_then_2_B_in_rc\n"\
                 "TGTGAACAAGGTGTGAAGGCATCGCCGTGTTCGACGGCAACCAACGCAGCCTGGACCAC"\
                 "CGTCGCCGGTGGGGAACACAGACTTACGCGTTACGACAGGCTAATTGCTGGATTGC\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "A_then_2_B_in_rc\t2\t2\t40:0|75:0\t(+)(1)0:40|(-)(2)40:35|"\
                 "(-)(2)75:40\t(1)1126:40|(2)336:35|(2)495:40\t40|35|40\t"\
                 "0|0|0\tNone\n"\
                 "@Nothing\n"\
                 "AGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGGAGAGAGAGAGAGAGAGA\n"\
                 "+expected_results_unmatched.csv\n"\
                 "Nothing\n"
                 "@A_then_Blast_then_B_then_Blast_then_B\n"\
                 "ATCACTTTGATGGGTATAAACAACAAGCGGTAGTGATTAACAAGAGGAGCAAGAACAAC"\
                 "ATCAAGAGTCAGGGCTGGAATCTTCGATGCGTTGCGCTCAGCACTCAACCCCCTTCTTA"\
                 "TTGTCATAACAGTGGTATCTGACTCCCACCTTCAATTGTTATCATAAAGCGAGTTGGAT"\
                 "TGGCCATCCAGTGAGAAT\n"\
                 "+expected_results_A_and_B.csv\n"\
                 "A_then_Blast_then_B_then_Blast_then_B\t0\t2\t39:35|111:41\t"\
                 "(+)(1)0:39|(+)(2)74:37|(+)(2)152:43\t(1)1792:39|(2)268:37|"\
                 "(2)607:43\t39|37|43\t0|0|0\t1|2\n")

    # Input fastq file to analyze with error
    false_fasta_file = tmpdir.join("false_functional_tests.fasta")
    false_fasta_file.write("?10_insertions_in_contiguous_read\n"\
                 "ATGGTGCGAAGAGTCTATTGAGCTAATTGGTAGTCCTCCGGCCAAACCCTTTGCCTGAA"\
                 "TGCGGCTAATCCCAACTGCGGAGCAGATACCCACATGCCAGTGGGCAGTCT\n"\
                 "?11_insertions_in_contiguous_read\n"\
                 "ATGGTGCGAAGAGTCTATTGAGCTAATTGGTAGTCCTCCGGCCAAACCCTTTGGCCTGA"\
                 "ATGCGGCTAATCCCAACTGCGGAGCAGATACCCACATGCCAGTGGGCAGTCT\n"\
                 ">A_then_2_B_in_rc\n"\
                 "TGTGAACAAGGTGTGAAGGCATCGCCGTGTTCGACGGCAACCAACGCAGCCTGGACCAC"\
                 "CGTCGCCGGTGGGGAACACAGACTTACGCGTTACGACAGGCTAATTGCTGGATTGC\n"\
                 ">A_then_Blast_then_B_then_Blast_then_B\n"\
                 "ATCACTTTGATGGGTATAAACAACAAGCGGTAGTGATTAACAAGAGGAGCAAGAACAAC"\
                 "ATCAAGAGTCAGGGCTGGAATCTTCGATGCGTTGCGCTCAGCACTCAACCCCCTTCTTA"\
                 "TTGTCATAACAGTGGTATCTGACTCCCACCTTCAATTGTTATCATAAAGCGAGTTGGAT"\
                 "TGGCCATCCAGTGAGAAT\n")

    # Try the full software with wrong fastq file
    with unittest.mock.patch("sys.argv", ["func_test", "-i", str(false_file),
                                          "-r", str(ref_a), str(ref_b),
                                          "-o", str(output_folder), "-k", "30",
                                          "-m", "10", "-p", "4", "-b", "-t",
                                          str(h_file)]):
        assert FindRecombinationsAmongGenomes.main() is None

    # Try the full software with wrong fasta file
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with unittest.mock.patch("sys.argv", ["func_test", "-i",
                                              str(false_fasta_file),
                                              "-r", str(ref_a), str(ref_b),
                                              "-o", str(output_folder), "-k",
                                              "30", "-m", "10", "-p", "4",
                                              "-b", "-t", str(h_file)]):
            FindRecombinationsAmongGenomes.main()
    assert pytest_wrapped_e.type == SystemExit
    # Error output
    captured = capsys.readouterr()
    assert "File error: enable to understand type of file {} "\
           "(?)".format(false_fasta_file) in captured.out

    # Try the full software
    with unittest.mock.patch("sys.argv", ["func_test", "-i", str(f_file),
                                          "-r", str(ref_a), str(ref_b),
                                          "-o", str(output_folder), "-k", "30",
                                          "-m", "10", "-p", "4", "-b", "-t",
                                          str(h_file)]):
        FindRecombinationsAmongGenomes.main()
    # Open input file that contains truth
    good_res = defaultdict(list)
    with open(f_file) as truth:
        for line in truth:
            truth.readline()
            file_name = truth.readline().strip()[18:]
            result = truth.readline().strip()
            good_res[file_name].append(result)

    # The following can't work for unmatched
    # because first line is not a header
    good_res["unmatched.csv"] = []
    # Results for unmatched.csv
    with open(os.path.join(output_folder, "unmatched.csv")) as res_file:
        assert res_file.read() == "@Nothing\n"

    # Results for A.csv, B.csv and A_and_B.csv
    for filename in good_res.keys():
        nb_line = 0
        with open(os.path.join(output_folder, filename)) as file_res:
            next(file_res)
            for line in file_res:
                nb_line += 1
                assert line.strip()[1:] in good_res[filename]
        assert nb_line == len(good_res[filename])

    # Results for breakpoint
    with open(os.path.join(output_folder, "breakpoints.fasta")) as res_file:
        assert res_file.read() == ">11_insertions_in_contiguous_read_1\n"\
                                  "AAACCCTTTGG\n"\
                                  ">contiguous_on_ref_11_insert_on_read_1\n"\
                                  "AAACCCGGGTT\n"\
                                  ">Insert_of_9_and_10_in_diff_matches_1\n"\
                                  "TGCGCGCGCGCGCGCGCGGGC\n"\
                                  ">Insert_of_10_and_11_in_read_1\n"\
                                  "AAACCCGGGTT\n"\
                                  ">A_then_Blast_then_B_then_Blast_then_B_1\n"\
                                  "ACAAGAGGAGCAAGAACAACATCAAGAGTCAGGGC\n"\
                                  ">A_then_Blast_then_B_then_Blast_then_B_2\n"\
                                  "CTTCTTATTGTCATAACAGTGGTATCTGACTCCCACCTTCA\n"

    # Res for Blast
    with open(os.path.join(output_folder, "res_blast.csv")) as res_file:
        assert res_file.read() == "A_then_Blast_then_B_then_Blast_then_B_1\t"\
                                  "lcl|NC_000001.11_cds_XP_024307730.1_3~[gen"\
                                  "e=LOC112268260]~[db_xref=GeneID:112268260]"\
                                  "~[protein=uncharacterized~protein~LOC11226"\
                                  "8260~isoform~X1]~[protein_id=XP_024307730."\
                                  "1]~[location=complement(join(358153..35818"\
                                  "3,365565..365692,373144..373323,379769..37"\
                                  "9870,399041..399100))]~[gbkey=CDS]\t"\
                                  "1.12e-15\t65.8\n"\
                                  "A_then_Blast_then_B_then_Blast_then_B_1\t"\
                                  "lcl|NC_000001.11_cds_XP_024307731.1_2~[gen"\
                                  "e=LOC112268260]~[db_xref=GeneID:112268260]"\
                                  "~[protein=uncharacterized~protein~LOC11226"\
                                  "8260~isoform~X2]~[protein_id=XP_024307731."\
                                  "1]~[location=complement(join(358067..35818"\
                                  "3,373144..373323,379769..379870,399041..39"\
                                  "9100))]~[gbkey=CDS]\t1.12e-15\t65.8\n"\
                                  "A_then_Blast_then_B_then_Blast_then_B_2\t"\
                                  "lcl|NC_000001.11_cds_NP_001005484.1_1~[gen"\
                                  "e=OR4F5]~[db_xref=CCDS:CCDS30547.1,GeneID:"\
                                  "79501]~[protein=olfactory~receptor~4F5]~[p"\
                                  "rotein_id=NP_001005484.1]~[location=69091."\
                                  ".70008]~[gbkey=CDS]\t6.39e-19\t76.8\n"

    # Res for compressed blast result
    with open(os.path.join(output_folder, "compressed.fasta")) as res_file:
        res = []
        for line in res_file.readlines():
            res.append(set(line.strip().split("\t")))
        truth = []
        truth.append(set(">A_then_Blast_then_B_then_Blast_then_B_1"\
                         "|1.12e-15|65.8\n".strip().split("\t")))
        truth.append(set("lcl|NC_000001.11_cds_XP_024307731.1_2~[gene=LOC1122"\
                         "68260]~[db_xref=GeneID:112268260]~[protein=uncharac"\
                         "terized~protein~LOC112268260~isoform~X2]~[protein_i"\
                         "d=XP_024307731.1]\t"\
                         "lcl|NC_000001.11_cds_XP_024307730.1_3~[gene=LOC1122"\
                         "68260]~[db_xref=GeneID:112268260]~[protein=uncharac"\
                         "terized~protein~LOC112268260~isoform~X1]~[protein_i"\
                         "d=XP_024307730.1]\n".strip().split("\t")))
        truth.append(set(">A_then_Blast_then_B_then_Blast_then_B_2"\
                         "|6.39e-19|76.8\n".strip().split("\t")))
        truth.append(set("lcl|NC_000001.11_cds_NP_001005484.1_1~[gene=OR4F5]~"\
                         "[db_xref=CCDS:CCDS30547.1,GeneID:79501]~[protein=ol"\
                         "factory~receptor~4F5]~"\
                         "[protein_id=NP_001005484.1]\n".strip().split("\t")))
        assert res == truth
