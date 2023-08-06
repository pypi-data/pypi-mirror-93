#! /usr/bin/env python
from nexson import validate_nexson
from peyutil.test.support.helper import testing_write_json as twj
from peyutil.test.support.helper import testing_read_json as trj
from nexson.test.support.pathmap import get_test_path_mapper
import unittest
import os

pathmap = get_test_path_mapper()

# round trip filename tuples
VALID_NEXSON_DIRS = ['9', 'otu', ]


class TestConvert(unittest.TestCase):
    def testInvalidFilesFail(self):
        msg = ''
        for fn in pathmap.all_files(os.path.join('nexson', 'lacking_otus')):
            if fn.endswith('.input'):
                frag = fn[:-len('.input')]
                inp = trj(fn)
                aa = validate_nexson(inp)
                annot = aa[0]
                # import json
                # print(json.dumps(annot.prepare_annotation(), indent=2))
                #for n, e in enumerate(annot.errors):
                    # print(n, type(e))
                    # for nv, v in enumerate(e):
                    #     vt = v[0]
                    #     print(nv, vt.as_dict(v))
                if len(annot.errors) == 0:
                    ofn = pathmap.nexson_source_path(frag + '.output')
                    ew_dict = annot.get_err_warn_summary_dict()
                    twj(ew_dict, ofn)
                    msg = "Failed to reject file. See {o}".format(o=str(msg))
                    self.assertTrue(False, msg)


if __name__ == "__main__":
    unittest.main()
