#!/usr/bin/env python
"""
Library for handling the NexSON format for phylogenetic trees used by the phylesystem
portion of the Open Tree of Life project
"""
# Some imports to help our py2 code behave like py3
from __future__ import absolute_import, print_function, division

__version__ = '0.0.3'  # sync with setup.py
__all__ = ['syntax',
           'validation',
           'proxy']

from .syntax import (detect_nexson_version,
                     extract_otu_nexson,
                     extract_tree_nexson,
                     nexson_frag_write_newick,
                     )
from .validation import (ot_validate,
                         validate_nexson,
                         )
from .proxy import NexsonProxy

__all__ = [  # From syntax
           'detect_nexson_version',
           'extract_otu_nexson',
           'extract_tree_nexson',
           ]



