#! /usr/bin/env python
import unittest
import logging
from nexson.syntax import sort_arbitrarily_ordered_nexson
from nexson.manip import merge_otus_and_trees
from nexson.test.support.pathmap import get_test_path_mapper as ntest_path_mapper

pathmap = ntest_path_mapper()

_LOG = logging.getLogger(__name__)


class TestMerge(unittest.TestCase):
    def testCanConvert(self):
        inp = pathmap.nexson_obj('merge/merge-input.v1.2.json')
        expected = pathmap.nexson_obj('merge/merge-expected.v1.2.json')
        expected = sort_arbitrarily_ordered_nexson(expected)
        inp = sort_arbitrarily_ordered_nexson(inp)
        self.assertNotEqual(inp, expected)
        merge_otus_and_trees(inp)
        pathmap.equal_blob_check(self, '', inp, expected)


if __name__ == "__main__":
    unittest.main()
