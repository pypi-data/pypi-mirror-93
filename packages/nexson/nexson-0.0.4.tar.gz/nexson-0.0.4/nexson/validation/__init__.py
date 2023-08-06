#!/usr/bin/env python
"""Functions for validating NexSON.
"""
from nexson.validation.adaptor import create_validation_adaptor
from nexson.validation.logger import FilteringLogger, ValidationLogger
from nexson.validation.warning_codes import NexsonWarningCodes
from nexson.syntax import NexsonError

def validate_nexson(obj,
                    warning_codes_to_skip=None,
                    retain_deprecated=True,
                    **kwargs):
    """Takes a NexSON `obj`. Returns a `(validatation_log, adaptor)` pair.

    `warning_codes_to_skip` is None or an iterable collection of integers
        that correspond to facets of NexsonWarningCodes. Warnings associated
        with any code in the list will be suppressed.
    `retain_deprecated` if False, then `obj` may be modified to replace
        deprecated constructs with new syntax. If it is True, the `obj` will
        not be modified.

    `validatation_log` will be an instance of a `DefaultRichLogger` subclass.
        it will hold warning and error messages.
    `adaptor` will be an instance of `NexsonValidationAdaptor`.
        it holds a reference to `obj` and the bookkeepping data necessary to attach
        the log message to `obj` if
    """
    if warning_codes_to_skip:
        v = FilteringLogger(codes_to_skip=list(warning_codes_to_skip), store_messages=True)
    else:
        v = ValidationLogger(store_messages=True)
    v.retain_deprecated = retain_deprecated
    n = create_validation_adaptor(obj, v, **kwargs)
    return v, n


def ot_validate(nexson, **kwargs):
    """Returns three objects:
        an annotation dict (NexSON formmatted),
        the validation_log object created when NexSON validation was performed, and
        the object of class NexSON which was created from nexson. This object may
            alias parts of the nexson dict that is passed in as an argument.

    Currently the only kwargs used is 'max_num_trees_per_study'
    """
    # stub function for hooking into NexSON validation
    codes_to_skip = [NexsonWarningCodes.UNVALIDATED_ANNOTATION]  # pylint: disable=E1101
    v_log, adaptor_obj = validate_nexson(nexson, codes_to_skip, **kwargs)
    annotation = v_log.prepare_annotation(author_name='api.opentreeoflife.org/validate',
                                          description='Open Tree NexSON validation')
    return annotation, v_log, adaptor_obj

from ._validation_base import NexsonAnnotationAdder, replace_same_agent_annotation
