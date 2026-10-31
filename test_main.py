from program import calculate_gc,gc_percentage,decode_quality,position_mean,validity,open_fastq
import gzip
import pytest

def test_open_fastq(tmp_path):
    path=tmp_path/"tiny.fastq.gz"
    with gzip.open(path,"wt") as f:
        f.write("@r1\nACGT\n+\nIII\n")
    with open_fastq(str(path)) as f:
        assert f.readline()=="@r1\n"


def test_gc():
    assert calculate_gc("AAATTT")==(0,6)
    assert calculate_gc("GGCC")==(4,4)
    assert calculate_gc("ACGTNN")==(2,4)

def test_gc_percentage():
    assert gc_percentage(5,10)==50.0
    assert gc_percentage(0,0)==0

def test_decode_quality():
    assert decode_quality("5?I#")==[20,30,40,2]

def test_position_mean():
    assert position_mean([60,50,10],[2,2,1])==[30.0,25.0,10.0]

def test_validity_1():
    assert validity("@r1","ACGT","+","IIII")==""

def test_validity_2():
    assert validity("r1","ACGT","+","IIII")=="Header must start with @ ."

def test_validity_3():
    assert validity("@r1","ATCX","+","IIII")=="The sequence contains invalid characters ."

def test_validity_4():
    assert validity("@r1","ACGT","*","IIII")=="Third line must start with + ."

def test_validity_5():
    assert validity("@r1","ACGT","+","III")=="Sequence and quality lengths differ ."



