from PyImports.Utils.Helpers import *


def test_dict2xml():
    converted = dict2xml({ 'a': 1, 'b': { 'c': 2, 'd': 3 } })
    expected = "<root><a>1</a><b><c>2</c><d>3</d></b></root>"
    assert converted == expected

    converted = dict2xml({ 'a': [ { 'b': 2 }, { 'c': 3 } ] })
    expected = "<root><a><b>2</b></a><a><c>3</c></a></root>"
    assert converted == expected

    converted = dict2xml({ 'a': [ { 'b': 2 }, { 'c': 3 } ] }, root_node="new_root")
    expected = "<new_root><a><b>2</b></a><a><c>3</c></a></new_root>"
    assert converted == expected
