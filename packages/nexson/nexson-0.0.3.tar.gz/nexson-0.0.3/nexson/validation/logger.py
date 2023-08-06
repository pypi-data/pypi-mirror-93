#!/usr/bin/env python
"""Classes for recording warnings and errors
"""
from ..syntax.helper import _add_value_to_dict_bf
from .helper import SeverityCodes, VERSION
from .warning_codes import NexsonWarningCodes
from functools import cmp_to_key
import logging
import platform
import sys

_LOG = logging.getLogger(__name__)


def _err_warn_summary(w):
    d = {}
    for el in w:
        msg_adapt_inst = el[0]
        r = msg_adapt_inst.as_dict(el)
        key = r['@code']
        del r['@code']
        _add_value_to_dict_bf(d, key, r)
    return d

# noinspection PyUnusedLocal
def _create_message_list(key, w, severity):  # pylint: disable=W0613
    d = []
    for el in w:
        msg_adapt_inst = el[0]
        r = msg_adapt_inst.as_dict(el)
        r['@severity'] = severity
        d.append(r)
    return d


_LIST_0 = [0]
_LIST_1 = [0]


def _msg_data_cmp(x, y):
    xl = x.get('data', _LIST_0)
    yl = y.get('data', _LIST_1)
    if xl == yl:
        return 0
    return -1 if xl < yl else 1


def _msg_cmp(x, y):
    xr = x.get('refersTo')
    yr = y.get('refersTo')
    if xr is None:
        if yr is None:
            return _msg_data_cmp(x, y)
        else:
            return 1
    if yr is None:
        return -1
    xri = xr.get('@idref')
    yri = yr.get('@idref')
    # _LOG.debug('xri = "{x}" yri = "{y}"'.format(x=xri, y=yri))
    if xri is None:
        if yri is None:
            xrk = list(xr.keys())
            xrk.sort()
            yrk = list(yr.keys())
            yrk.sort()
            if xrk == yrk:
                xrv = [xr[i] for i in xrk]
                yrv = [yr[i] for i in xrk]
                if xrv == yrv:
                    return _msg_data_cmp(x, y)
                if xrv < yrv:
                    return -1
                return 1
            return -1 if xrk < yrk else 1
        return 1
    if yri is None:
        return -1
    if xri == yri:
        return _msg_data_cmp(x, y)
    return -1 if xri < yri else 1


_msg_key_func = cmp_to_key(_msg_cmp)


class DefaultRichLogger(object):
    """A container for warnings and errors encountered during NexSON validation.

    `store_messages=False` argument to __init__ is *deprecated*. That argument
    is retained for backwards compatibility, but ignored. Messages are store
    regardless of the value of this argument.
    """
    def __init__(self, store_messages=False):
        self.out = sys.stderr
        self.store_messages_as_obj = store_messages
        self._warn_by_type = {}
        self._err_by_type = {}
        self._warn_by_obj = {}
        self._err_by_obj = {}
        self.prefix = ''
        self.retain_deprecated = False
        self.codes_to_skip = set()

    def has_error(self):
        """Returns `True` if no errors were stored."""
        return bool(self._err_by_type)

    @property
    def errors(self):
        """Returns the values of an internal errors by value dict.

        Returns an interable. Each element will be a
        set of tuples. The first element in each tuple will be
        a `MessageTupleAdaptor` instance.
        """
        return self._err_by_type.values()

    @property
    def warnings(self):
        """Returns the values of an internal warnings by value dict.

        Returns an interable. Each element will be a
        set of tuples. The first element in each tuple will be
        a `MessageTupleAdaptor` instance.
        """
        return self._warn_by_type.values()

    def is_logging_type(self, t):
        """Base class always returns `True`, as all messages are logged."""
        # pylint: disable=W0613,R0201
        return True

    def register_new_messages(self, err_tup, severity):
        """Stores a typed error tuple by type and python ID of target.

        The `err_tup` should be a tuple of the type described in `MessageTupleAdaptor`.
        The `severity` should be either `SeverityCodes.WARNING` or `SeverityCodes.ERROR`."""
        c = err_tup[0].code
        pyid = err_tup[1]
        if severity == SeverityCodes.WARNING:
            x = self._warn_by_type.setdefault(c, set())
            x.add(err_tup)
            x = self._warn_by_obj.setdefault(pyid, set())
            x.add(err_tup)
        else:
            x = self._err_by_type.setdefault(c, set())
            x.add(err_tup)
            x = self._err_by_obj.setdefault(pyid, set())
            x.add(err_tup)

    def get_err_warn_summary_dict(self, sort=True):
        """Returns a `{'warnings': {}, 'errors': {}}` view of all logged messages.

        The values in the warnings and errors dict will have a facet of
        `NexsonWarningCodes` as keys mapped to a list of the a slimmed version of the dict
        returned by calling `MessageTupleAdaptor.as_dict` on each logged warning or error.
        A key will be absent if no warning or error of that type was encountered.
        The "slimmed version" of the dict simply omits the '@code' value, because that will
        be the same for every error of each type (and the same as the key in the containing dict).
        """
        w = {}
        for wm in self._warn_by_type.values():
            d = _err_warn_summary(wm)
            w.update(d)
        e = {}
        for em in self._err_by_type.values():
            d = _err_warn_summary(em)
            e.update(d)
        if sort:
            for v in w.values():
                if isinstance(v, list):
                    v.sort(key=_msg_key_func)
            for v in e.values():
                if isinstance(v, list):
                    v.sort(key=_msg_key_func)
        return {'warnings': w, 'errors': e}

    def create_nexson_message_list(self, sort=True):
        """Returns a list of dict-forms of the log tuples described in `MessageTupleAdaptor`.

        The list elements are organized by logged event type.
        """
        em_list = []
        for key, em in self._err_by_type.items():
            d = _create_message_list(key, em, 'ERROR')
            em_list.extend(d)
        if sort:
            em_list.sort(key=_msg_key_func)
        wm_list = []
        for key, em in self._warn_by_type.items():
            d = _create_message_list(key, em, 'WARNING')
            wm_list.extend(d)
        if sort:
            em_list.sort(key=_msg_key_func)
            wm_list.sort(key=_msg_key_func)
        em_list.extend(wm_list)
        return em_list

    def prepare_annotation(self,
                           author_name='',
                           invocation=tuple(),
                           author_version=VERSION,
                           url='https://github.com/OpenTreeOfLife/peyotl',
                           description=None,
                           annotation_label=None  # @TEMP arg for backward compat.
                           ):
        """Wraps the set of logged warnings/errors as a dict, addable to a NexSON object.

        For example:

        .. highlight:: python
        .. code-block:: python

            obj = json.load(inp)
            v_log, adaptor = validate_nexson(obj)
            annotation = v_log.prepare_annotation(author_name=SCRIPT_NAME,
                                                  invocation=sys.argv[1:],
                                                  )
            adaptor.add_or_replace_annotation(obj,
                                              annotation['annotationEvent'],
                                              annotation['agent'],
                                              add_agent_only=args.add_agent_only)
        """
        if description is None:
            description = "validator of NexSON constraints as well as constraints " \
                          "that would allow a study to be imported into the Open Tree " \
                          "of Life's phylogenetic synthesis tools"
        # @TEMP. the args are in flux between the branches of api.opentreeoflife.org.
        #    which is bad. Hopefully we don't need annotation_label and
        #   can get rid of it.
        if annotation_label is not None:
            description += annotation_label
        # checks_performed = list(NexsonWarningCodes.numeric_codes_registered)
        # for code in self.codes_to_skip:
        #     try:
        #         checks_performed.remove(code)
        #     except:
        #         pass
        # checks_performed = [NexsonWarningCodes.facets[i] for i in checks_performed]
        agent_id = 'peyotl-validator'
        aevent_id = agent_id + '-event'
        ml = self.create_nexson_message_list()
        annotation = {
            '@id': aevent_id,
            '@description': description,
            '@wasAssociatedWithAgentId': agent_id,
            # '@dateCreated': datetime.datetime.utcnow().isoformat(),
            '@passedChecks': not self.has_error(),
            '@preserve': False,
            'message': ml
        }
        invocation_obj = {
            'commandLine': [i for i in invocation if i.startswith('--')],
            # 'checksPerformed': checks_performed,
            'otherProperty': [
                {'name': 'pythonVersion',
                 'value': platform.python_version()},
                {'name': 'pythonImplementation',
                 'value': platform.python_implementation(),
                 },
            ]
        }
        agent = {
            '@id': agent_id,
            '@name': author_name,
            '@url': url,
            '@description': description,
            '@version': author_version,
            'invocation': invocation_obj,
        }
        return {'annotationEvent': annotation, 'agent': agent}


class ValidationLogger(DefaultRichLogger):
    """Subclass of `DefaultRichLogger`. Retained for backward compatibility.

    No methods are overridden, simply uses base class behavior.
    """

    def __init__(self, store_messages=False):
        DefaultRichLogger.__init__(self, store_messages=store_messages)


class FilteringLogger(ValidationLogger):
    """Subclass of `DefaultRichLogger`.

    __init__ method allows client to supply `codes_to_register` or
    `codes_to_skip` ei
    """

    def __init__(self, codes_to_register=None, codes_to_skip=None, store_messages=False):
        ValidationLogger.__init__(self, store_messages=store_messages)
        self.codes_to_skip = set()
        if codes_to_register:
            self.registered = set(codes_to_register)
            if codes_to_skip:
                for el in codes_to_skip:
                    self.codes_to_skip.add(el)
                    assert el not in self.registered
        else:
            assert codes_to_skip
            self.registered = set(NexsonWarningCodes.numeric_codes_registered)
            for el in codes_to_skip:
                self.codes_to_skip.add(el)
                self.registered.remove(el)

    def is_logging_type(self, t):
        return (t not in self.codes_to_skip) and (t in self.registered)
