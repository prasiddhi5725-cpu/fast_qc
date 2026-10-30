from program import calculate_gc
from program import gc_percentage
from program import decode_quality
from program import position_mean
from program import validity

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



