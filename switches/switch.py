"""
:copyright: Copyright (c) 2020 Jeremiah Ikosin (@ziord)
:license: MIT, see LICENSE for more details
"""

from collections import namedtuple
import warnings


class SwitchError(Exception): ...


class switch:
    def __init__(self, value, args=(), kwargs=None, fallthrough=False, allow_duplicates=True,
                 as_callable=False, no_warning=False):
        self._as_callable = as_callable
        self._fth = fallthrough
        self._allow_dup = allow_duplicates
        self._warn = not no_warning
        self._v_args = args
        self._v_kwargs = kwargs
        self._validate_func_arguments(self._v_args, self._v_kwargs)
        self._cval = value(*self._v_args, **(self._v_kwargs or {})) \
            if callable(value) and self._as_callable else value
        self._ccount = 0
        self._dft = self._dft_flg = None
        self._from_icase = self._from_fcase = False
        self._cases, self.__all_fvals = [], []
        self.__all_nvals, self.__all_ivals = [], []

    def __enter__(self):
        self.__update_cval()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            return
        else:
            self.__exec()

    def __create_case(self, bool_val, func, args=(), kwargs=None, brk=None, ind=None):
        Case = namedtuple("Case", "ind bval func args kwargs brk")
        return Case(self._ccount, bool_val, func, args, kwargs, brk) if not ind \
            else Case(ind, bool_val, func, args, kwargs, brk)

    def __create_break(self, from_user=False):
        Break = namedtuple("Break", "ind upd_count")
        return Break(self._ccount, 0) if not from_user else Break(self._ccount, 1)

    def __set_default(self, func=None, args=(), kwargs=None, brk=None):
        Default = namedtuple("Default", "func args kwargs brk")
        kwargs = {} if not kwargs else kwargs
        self._dft = Default(func, args, kwargs, brk)
        self._cases.append(self._dft_flg)

    def __update_cval(self):
        self._cval = self._cval(*self._v_args, **(self._v_kwargs or {})) \
            if callable(self._cval) and self._as_callable else self._cval

    def __exc(self, start_index):
        cflag = False
        __cases = self._cases[start_index:]
        for case in __cases:
            if case:  # case is None when end of __cases is reached
                case.func(*case.args, **case.kwargs) if case.func and callable(case.func) else ...
                if case.brk:
                    cflag = True
                    break
        if not cflag:
            self._dft.func(*self._dft.args, **self._dft.kwargs) \
                if self._dft and callable(self._dft.func) else ...

    def __exec_ft(self):
        start_index = None
        for case in self._cases:
            if case is self._dft_flg:
                self._cases.pop()
                break
            if self.__is_equal(case.bval):
                start_index = case.ind
                break
        if start_index is not None:
            self.__exc(start_index)
        else:
            self._dft.func(*self._dft.args, **self._dft.kwargs) \
                if self._dft and callable(self._dft.func) else ...

    def __exec_nft(self):
        _case, start_index = None, None
        for case in self._cases:
            if case is self._dft_flg:
                self._cases.pop()
                break
            if self.__is_equal(case.bval):
                _case = case
                if case.brk:
                    break
                else:
                    start_index = case.ind
                    break
        if start_index is not None:
            self.__exc(start_index)
        else:
            if _case:
                _case.func(*_case.args, **_case.kwargs) \
                    if _case.func and callable(_case.func) else ...
            else:
                self._dft.func(*self._dft.args, **self._dft.kwargs) \
                    if self._dft and callable(self._dft.func) else ...

    def __exec(self):
        if self._dft is None:
            self._cases.append(None)
            if self._warn:
                warnings.warn("Default statement omitted")
        if self._fth:
            self.__exec_ft()
        else:
            self.__exec_nft()

    def __is_equal(self, val):
        try:
            return self._cval == val
        except (AttributeError, Exception):
            return False

    def __get_duplicates(self):
        dups = []
        if len(set(self.__all_nvals)) != len(self.__all_nvals):
            dups.append("case")
        # allow_duplicates shouldn't affect icase... due to caveat of using
        # case as the base for fcase and icase
        if len(set(self.__all_fvals)) != len(self.__all_fvals):
            dups.append("fcase")
        return dups

    @staticmethod
    def _isinstance(obj, cls):
        if obj.__class__.__name__ == cls.__name__:
            return True
        return False

    @staticmethod
    def _isiterable(p_iterable):
        return hasattr(p_iterable, '__iter__') or \
               hasattr(p_iterable, '__next__') or \
               hasattr(p_iterable, '__getitem__')

    def _validate_values(self):
        try:
            dups = self.__get_duplicates()
            if dups:
                if not self._allow_dup:
                    self._error(f"Duplicate {', '.join(dups)} values")
        except (TypeError, Exception) as E:
            if isinstance(E, SwitchError):
                raise E
            ...  # no __hash__ attr TODO: deep equals for objects without __hash__ ?

    def _validate_break(self, from_user):
        if from_user:
            if not hasattr(self, '_dft__c'):
                self._dft__c = 1
            else:
                self._dft__c += 1
                if self._dft__c >= 2:
                    self._error(
                        "Cannot use multiple breaks for a default statement")
        if self._warn:
            warnings.warn(
                'Irrelevant addition of break after default statement.')

    def _validate_func_arguments(self, args, kwargs):
        # args represents arguments passed in as tuples, lists, or sets
        if not any(isinstance(args, _) for _ in (tuple, list, set)):
            self._error("args must be tuple, list or set type if specified")
        # kwargs represents keyword arguments
        if kwargs is not None and not isinstance(kwargs, dict):
            self._error("kwargs must be dict type if specified")

    def _add_value(self, v, from_icase=False, from_fcase=False):
        if from_fcase:
            self.__all_fvals.append(v)
        elif from_icase:
            self.__all_ivals.append(v)
        else:
            self.__all_nvals.append(v)

    def _add_break(self, from_user=False):
        if self._dft is not None:
            self._validate_break(from_user)
            return
        _case = self._cases.pop()
        upd_count = _case.brk.upd_count + 1 if _case.brk else (
            1 if from_user else 0
        )
        if _case.brk and upd_count >= 2:
            self._error(
                "Cannot use multiple break statements for a single case")

        brk = self.__create_break(from_user)
        brk = brk._replace(upd_count=upd_count)

        _case = _case._replace(brk=brk)
        self._cases.append(_case)

    def _add_case(self, case):
        if self._dft is not None:
            self._error(
                "Cannot add a case after default statement")
        self._cases.append(case)

    @staticmethod
    def _error(cause):
        raise SwitchError(cause)

    def _scase(self, bool_val, func=None, args=(), kwargs=None, c_break=None):
        self.__update_cval()
        _case = None
        brk = self.__create_break()
        kwargs = {} if kwargs is None else kwargs
        self._validate_func_arguments(args=args, kwargs=kwargs)
        if c_break is None:
            if not self._fth:  # not fallthrough? then implicitly add breaks
                _case = self.__create_case(bool_val, func, args, kwargs, brk)
            else:
                _case = self.__create_case(bool_val, func, args, kwargs, None)
        else:  # break explicitly declared in method call
            if c_break:  # could be True, False
                _case = self.__create_case(bool_val, func, args, kwargs, brk)
            else:
                _case = self.__create_case(bool_val, func, args, kwargs, None)
        # separate storage of values for duplicate checking later
        if self._from_icase:
            self._add_value(bool_val, from_icase=True)
        elif self._from_fcase:
            self._add_value(bool_val, from_fcase=True)
        else:
            self._add_value(bool_val)
        self._validate_values()
        self._add_case(_case)
        self._ccount += 1

    def _s_icase(self, iterable, func, args=(), kwargs=None, c_break=None):
        self.__update_cval()
        if not self._isiterable(iterable):
            self._error(f"Cannot use non-iterable in icase: {iterable}")
        _val = None
        for val in iterable:
            v = self.__is_equal(val()) if callable(val) else self.__is_equal(val)
            if v:
                _val = val
                break
        self._from_icase = True
        if _val:
            self._scase(_val, func, args, kwargs, c_break)
        else:
            self._scase(iterable, func, args, kwargs, c_break)
        self._from_icase = False

    def _s_fcase(self, *, f_name, f_args=(), f_kwargs=None, func=None, args=(), kwargs=None, c_break=None):
        if not callable(f_name):
            self._error(f"f_name in fcase is not callable: {f_name}")
        _args, _kwargs = (), {}
        # args represents arguments passed in as tuples, lists, or sets
        if any(isinstance(f_args, _) for _ in (tuple, list, set)):
            _args = f_args
        else:
            self._error("f_args in fcase must be tuple, list or set type if specified")
        # kwargs represents keyword arguments
        if isinstance(f_kwargs, dict):
            _kwargs = f_kwargs
        elif f_kwargs is not None:
            self._error("f_kwargs in fcase must be dict type if specified")
        val = f_name(*_args, **_kwargs)
        self._from_fcase = True
        self._scase(val, func, args, kwargs, c_break)
        self._from_fcase = False

    #################################
    #       public interface
    #################################

    @property
    def allow_fallthrough(self):
        return self._fth

    @allow_fallthrough.setter
    def allow_fallthrough(self, val):
        self._fth = bool(val)

    @property
    def allow_duplicates(self):
        return self._allow_dup

    @allow_duplicates.setter
    def allow_duplicates(self, val):
        self._allow_dup = bool(val)

    @property
    def as_callable(self):
        return self._as_callable

    @as_callable.setter
    def as_callable(self, val):
        self._as_callable = bool(val)

    @property
    def no_warning(self):
        return not self._warn

    @no_warning.setter
    def no_warning(self, val):
        self._warn = not bool(val)

    @property
    def value(self):
        return self._cval

    def c_break(self):
        if self._ccount - 1 < 0:
            self._error(
                "Cannot use break without a case")
        self._add_break(from_user=True)

    def default(self, func=None, args=(), kwargs=None, c_break=None):
        if self._dft is not None:
            self._error(
                "Cannot set multiple defaults for a single switch statement")
        self.__set_default(func, args, kwargs, c_break)

    def case(self, value, func=None, args=(), kwargs=None, c_break=None):
        self._scase(bool_val=value, func=func,
                    args=args, kwargs=kwargs, c_break=c_break)

    def icase(self, iterable, func=None, args=(), kwargs=None, c_break=None):
        self._s_icase(iterable=iterable, func=func,
                      args=args, kwargs=kwargs, c_break=c_break)

    def fcase(self, *, f_name, f_args=(), f_kwargs=None,
              func=None, args=(), kwargs=None, c_break=None):
        self._s_fcase(f_name=f_name, f_args=f_args, f_kwargs=f_kwargs,
                      func=func, args=args, kwargs=kwargs, c_break=c_break)
