import sys
import os

# internal imports
import f_rcif.cl_rcif


_f_name = r"full.rcif"
TEST_RCIF = f_rcif.cl_rcif.RCif()
if len(sys.argv) > 1: # when run directly with pytest
        _current_location = os.path.abspath(os.path.dirname(sys.argv[1]))
else: # when run through the runTests.py wrapper
        _current_location = os.path.abspath(os.path.dirname(sys.argv[0]))

_current_location = os.path.join(_current_location, "Tests", "Data", _f_name)

TEST_RCIF.load_from_file(_current_location)
TEST_GLOB = TEST_RCIF.glob
TEST_DATA = TEST_GLOB["data"]
TEST_DATA0 = TEST_DATA[0]


def relation_tester(relation, size):
    """
    Simple size check for a list of sets
    """
    assert len(relation)==size
    # each element should have exactly 3 components
    for element in relation:
        assert len(element) == 3

