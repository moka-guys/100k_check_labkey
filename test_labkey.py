#!/usr/bin/env python3
import pytest
from . import LabKey

# Read test patient data from file. first line = gel participant id, second line = dob (dd/mm/yyyy), third line = nhs number
with open('test_data.txt') as f:
    PID, DOB, NHSID = [ line.rstrip('\n') for line in f.readlines() ]
# Read authentication data
with open('/home/mokaguys/.netrc') as f:
    csv = [ line.split(' ') for line in f.readlines() ]
    MACHINE, UNAME, PWD = [ columns[1].rstrip('\n') for columns in csv ]

def test_optional_inputs():
    import sys
    input_set1 = ['python', '-i', str(PID)]
    input_set2 = ['python', '-i', PID, '-u', UNAME, '-p', PWD ]
    # Test with no user details
    sys.argv = input_set1
    LabKey.main()
    # Test with user details
    sys.argv = input_set2
    LabKey.main()

@pytest.fixture
def lk_object():
    '''Return Labkey object for test data PID'''
    return LabKey.LabKey_HTTP(PID, UNAME, PWD)

def test_labkey_dict(lk_object):
    assert isinstance(lk_object.data, dict)

def test_date_of_birth(lk_object):
    assert lk_object.dob.startswith(DOB)

def test_nhs_number(lk_object):
    assert lk_object.nhsid == NHSID
