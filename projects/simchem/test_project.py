import pytest
from project import molarmass, missing, ige
def test_molarmass():
    assert molarmass("H") == 1
def test_molarmass1():
    assert molarmass("He2") == 8
def test_missing():
    assert missing('X', 1) == 'H'
def test_missing2():
    assert missing('CXO', 42) == 'N'
def test_ige():
    assert ige({'V': 2.0, 'P': 'x', 'T': 273.0, 'n': 5.0, 'Rr': 0.08205736608096}) == 'P = 56.004'
def test_ige1():
    assert ige({'V': 0.5, 'P': 1.0, 'T': 300.0, 'n': 'x', 'Rr': 0.08205736608096}) == 'n = 0.020'