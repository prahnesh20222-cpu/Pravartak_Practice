import pytest

def function1(x,y):
    return x + y

def test_function1_a():
    assert function1(1,2) == 3
    
def test_function1_b():
    assert function1(0,0) == 0

def test_function1_c():
    assert function1(-1,-2) == -4
