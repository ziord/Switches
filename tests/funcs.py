"""
:copyright: Copyright (c) 2020 Jeremiah Ikosin (@ziord)
:license: MIT, see LICENSE for more details
"""

from switches.switch import switch, SwitchError


def foobar(x, y):
    return x*y


def foofoo():
    return 'foo'*2


class Foo:
    def __init__(self, n):
        self._n = n

    def __eq__(self, other):
        return self._n == other._n

    def __hash__(self):
        return sum(map(lambda x: ord(x), self._n))


class Bar:
    def __init__(self, p):
        self._p = p

    def __eq__(self, other):
        return self._p == other._p

    def __hash__(self):
        return sum(map(lambda x: ord(x), self._p))

    def __call__(self, *args, **kwargs):
        print(args, kwargs)
        return args, kwargs


valNum = 5
valList = [1, 2, 3]
valTup = (1, 2)
valCall = foofoo
valCall2 = foobar
valFoo = Foo('foo')
valBar = Bar('bar')
valRange = range(10)


##############################
#       ft
##############################
def test_valNum_ft():
    g = []
    with switch(valNum, allow_duplicates=False, fallthrough=True) as s:
        s.case(5, lambda: g.append('pop'))
        s.case(12, lambda: g.append('push'))
        s.default(None)
    return g


def test_valList_ft():
    g = []
    with switch(valList, allow_duplicates=False) as s:
        s.allow_fallthrough = True
        s.case(5, lambda x: g.append(x), args=('push',))
        s.case(12, func=lambda y: g.append(y), kwargs={'y': 'pop'})
        s.default(func=lambda x: print('default here', x), args=('yeah!',))
    return g


def test_valFoo_ft():
    g = []
    with switch(valFoo, fallthrough=True) as s:
        s.allow_duplicates = True
        s.case(5, lambda: g.append('pop'))
        s.case(12, lambda: g.append('push'))
        s.case(valFoo, lambda: g.append('poof'))
        s.case(valFoo, lambda: g.append('poof2'))
        s.default(None)
    return g


def test_valCall_ft():
    g = []
    with switch(valCall, fallthrough=True) as s:
        s.allow_duplicates = True
        s.as_callable = True
        s.case('foofoo', lambda: g.append('pop'))
        s.case(6, lambda: g.append('push'))
        s.default(None)
    return g


def test_valCall2_ft():
    g = []
    with switch(valCall2, args=(2, 3), fallthrough=True) as s:
        s.allow_duplicates = True
        s.as_callable = True
        s.case('foofoo', lambda: g.append('pop'))
        s.case(6, lambda: g.append('push'))
        s.default(None)
    return g


def test_valNum2_ft():
    g = []
    with switch(valNum, allow_duplicates=False, fallthrough=True) as s:
        s.case(5, lambda: g.append('pop'))
        s.c_break()
        s.case(12, lambda: g.append('push'))
        s.default(None)
    return g


def test_valList2_ft():
    g = []
    with switch(valList, allow_duplicates=False) as s:
        s.allow_fallthrough = True
        s.case(valList, lambda: g.append('pop'), c_break=True)
        s.case([1, 2, 3], lambda: g.append('pop'))
        s.case(12, lambda: g.append('push'))
        s.default(func=lambda: print('default here'))
    return g


def test_valFoo2_ft():
    g = []
    with switch(valFoo, fallthrough=True) as s:
        s.allow_duplicates = True
        s.case(5, lambda: g.append('pop'))
        s.case(12, lambda: g.append('push'))
        s.case(valFoo, lambda: g.append('poof'), c_break=False)
        s.case(valFoo, lambda: g.append('poof2'),)
        s.c_break()
        s.case(valFoo, lambda: g.append('poof2'))
        s.default(None)
    return g


def test_valNum3_ft():
    g = []
    with switch(valNum) as s:
        s.allow_fallthrough = True
        s.allow_duplicates = False
        s.icase([1, 2, 3], lambda: g.append('pop'))
        s.icase(range(10), lambda: g.append('push'))
        s.default(func=lambda: print('default here'))
    return g


def test_valFoo3_ft(val):
    g = []
    with switch(val, fallthrough=True) as s:
        s.allow_duplicates = True
        s.case(5,)  # case without func or break, fall through
        s.case(12,)
        s.icase([Foo('tea'), Foo('coffee'), Foo('foo'), ], lambda: g.append('poof'))
        s.c_break()
        s.case(valFoo, lambda: g.append('poof2'))
        s.default(None)
    return g


def test_valNum4_ft():
    g = []
    with switch(valNum) as s:
        s.allow_fallthrough = True
        s.allow_duplicates = False
        s.fcase(f_name=foobar, f_kwargs={'x': 5, 'y': 1}, func=lambda: g.append('push'), c_break=True)
        s.case(range(10), lambda: g.append('push'))
        s.default(func=lambda: print('default here'))
    return g


def test_valNum5_ft():
    g = []
    with switch(value='foo'*2) as s:
        s.allow_fallthrough = True
        s.allow_duplicates = False
        s.fcase(f_name=foofoo, f_args=[], func=lambda: g.append('foofoo'))
        s.icase(['foo', 'foofoo', 'foobar'], lambda: g.pop(), c_break=True)
        s.case(range(10), lambda: g.append('push'))
        s.default(func=lambda: print('default here'))
    return g


def test_new_ft():
    g = []
    with switch(value=100) as s:
        s.allow_fallthrough = True
        s.allow_duplicates = False
        s.fcase(f_name=foofoo, f_args=(), func=lambda x: g.append(x), args=['foofoo',])
        s.icase(['foo', 'foofoo', 'foobar'], lambda: g.pop(), c_break=True)
        s.case(range(10), lambda: g.append('push'))
        s.default(func=lambda: g.append('defaulted'))
    return g


def test_call_ft():
    g = []
    with switch(value=Bar(2)(2, 3), as_callable=True) as s:
        s.allow_fallthrough = True
        s.case(1)
        s.case(((2, 3), {}), lambda: g.append(s.value))
        s.default(None)
        print('s.value', s.value)
    return g[0]


##############################
#       nft
##############################
def test_valNum_nft():
    g = []
    # fallthrough is False by default
    with switch(valNum, allow_duplicates=False, fallthrough=False) as s:
        s.case(5, lambda: g.append('pop'))
        s.case(12, lambda: g.append('push'))
        s.default(None)
    return g


def test_valList_nft():
    g = []
    with switch(valList, allow_duplicates=False) as s:
        s.case(5, lambda arg: g.append(arg), kwargs=dict(arg='pop'))
        s.case(12, lambda: g.append('push'))
        s.default(func=lambda: print('default here'))
    return g


def test_valFoo_nft():
    g = []
    with switch(valFoo) as s:
        s.allow_duplicates = True
        s.case(valFoo, func=lambda v: g.append(v), args=['poof'])
        s.case(6, lambda: g.append('poof2'))
        s.default(None)
    return g


def test_valNum2_nft():
    g = []
    with switch(valNum, allow_duplicates=False,) as s:
        s.case(5, lambda: g.append('pop'), c_break=False)
        s.case(12, lambda: g.append('push'))
        s.default(None)
    return g


def test_valCall_nft():
    g = []
    with switch(valCall,) as s:
        s.allow_duplicates = True
        s.as_callable = True
        s.case('foofoo', lambda: g.append('pop'))
        s.case(6, lambda: g.append('push'))
        s.default(None)
    return g


def test_valCall2_nft():
    g = []
    with switch(valCall2, args=(2, 3),) as s:
        s.allow_duplicates = True
        s.as_callable = True
        s.case('foofoo', lambda: g.append('pop'))
        s.case(12, lambda: g.append('push'))
        s.default(None)
    return g


def test_valList2_nft():
    g = []
    with switch(valList, allow_duplicates=False) as s:
        s.case(valList, lambda: g.append('pop'), c_break=True)
        s.case([1, 2, 3], lambda: g.append('pop'))
        s.default(func=lambda: print('default here'))
    return g


def test_valFoo2_nft():
    g = []
    with switch(valFoo,) as s:
        s.allow_duplicates = True
        s.case(12, lambda: g.append('push'))
        s.case(valFoo, lambda: g.append('poof'), c_break=False)
        s.case(valFoo, lambda: g.append('poof2'),)
        s.c_break()  # redundant
        s.case(valFoo, lambda: g.append('poof2'))
        s.default(None)
    return g


def test_valNum3_nft():
    g = []
    with switch(valNum) as s:
        s.allow_duplicates = False
        s.icase([1, 2, 3], lambda: g.append('pop'))
        s.icase(range(10), lambda: g.append('push'))
        s.default(func=lambda: print('default here'))
    return g


def test_valFoo3_nft(val):
    g = []
    with switch(val, allow_duplicates=True) as s:
        s.case(5,)  # case without func or break, no fall through
        s.case(12,)
        s.icase([Foo('tea'), Foo('coffee'), Foo('foo'), ], lambda: g.append('poof'))
        s.case(valFoo, lambda: g.append('poof2'))
        s.default(None)
    return g


def test_valNum4_nft():
    g = []
    with switch(valNum, allow_duplicates=False) as s:
        s.fcase(f_name=foobar, f_kwargs={'x': 5, 'y': 1}, func=lambda: g.append('push'), c_break=True)
        s.case(range(10), lambda: g.append('push'))
        s.default(func=lambda: print('default here'))
    return g


def test_valNum5_nft():
    g = []
    with switch(value='foo'*2, allow_duplicates=False) as s:
        s.fcase(f_name=foofoo, func=lambda: g.append('foofoo'))
        s.icase(['foo', 'foofoo', 'foobar'], lambda: g.pop(), c_break=True)
        s.case(range(10), lambda: g.append('push'))
        s.default(func=lambda: print('default here'))
    return g


def test_new_nft():
    g = []
    with switch(value=100, allow_duplicates=False) as s:
        s.fcase(f_name=foofoo, f_args=set(), func=lambda: g.append('foofoo'))
        s.icase(['foo', 'foofoo', 'foobar'], lambda: g.pop(), c_break=True)
        s.case(range(10), lambda: g.append('push'))
        s.default(func=lambda: g.append('defaulted'))
    return g


def test_call_nft():
    g = []
    with switch(value=Bar(2)(2, 3), as_callable=True) as s:
        s.case(1)
        s.case(((2, 3), {}), lambda: g.append(s.value))
        s.default(None)
        print('s.value', s.value)
    return g[0]


##########################
#  warnings
##########################
def test_valNum_wn():
    g = []
    with switch(valNum) as s:
        s.allow_duplicates = True
        s.allow_fallthrough = True
        s.case(5, lambda: g.append('pop'))
        s.case(5, lambda: g.append('push'))
        s.default(None)
        s.c_break()
    return g


def test_valTup_wn():
    g = []
    with switch(valTup) as s:
        s.allow_fallthrough = True
        s.case(5, lambda: g.append('pop'))
        s.case(5, lambda: g.append('push'))
        s.c_break()
    return g


##########################
#   errors
##########################
def test_dup_err():
    # duplicate error
    g = []
    with switch(valNum) as s:
        s.allow_duplicates = False
        s.allow_fallthrough = True
        s.case(5, lambda: g.append('pop'))
        s.case(5, lambda: g.append('push'))
        s.default(None)
    return g


def test_double_cbreak_err():
    # double c_break
    g = []
    with switch(valNum) as s:
        s.allow_duplicates = False
        s.allow_fallthrough = True
        s.case(5, lambda: g.append('pop'))
        s.case(5, lambda: g.append('push'))
        s.default(None)
        s.c_break()
        s.c_break()
    return g


def test_double_cbreak2_err():
    # double c_break
    g = []
    with switch(valNum) as s:
        s.allow_duplicates = False
        s.allow_fallthrough = True
        s.case(5, lambda: g.append('pop'))
        s.c_break()
        s.c_break()
        s.case(5, lambda: g.append('push'))
        s.default(None)
    return g


def test_case_after_default_err():
    # case after default
    g = []
    with switch(valNum) as s:
        s.allow_duplicates = False
        s.allow_fallthrough = True
        s.case(5, lambda: g.append('pop'))
        s.case(5, lambda: g.append('push'))
        s.default(None)
        s.case(10)
    return g


def test_call_err():
    # callable error
    g = []
    with switch(valNum, as_callable=False, fallthrough=True) as s:
        s.allow_duplicates = False
        s.fcase(f_name=5, func=lambda: g.append('pop'))
        s.default(None)
    return g


def test_iter_err():
    # iterable error
    g = []
    with switch(valNum, as_callable=False, fallthrough=True) as s:
        s.allow_duplicates = False
        s.icase(5, func=lambda: g.append('pop'))
        s.default(None)
    return g


def test_double_default_err():
    # double default statements
    with switch(valNum, as_callable=False, fallthrough=True) as s:
        s.default(None)
        s.default(None)


def test_value_args_err():
    with switch(valCall, args={},) as s:
        s.no_warning = True
        pass


def test_value_kwargs_err():
    with switch(valCall, kwargs=(),) as s:
        s.no_warning = True
        pass


def test_fcase_f_args_err():
    # f_args in fcase, passed in as the wrong type
    with switch(valNum, as_callable=False, fallthrough=True) as s:
        s.fcase(f_name=foofoo, f_args={})
        s.default(None)


def test_fcase_f_kwargs_err():
    # f_kwargs in fcase, passed in as the wrong type
    with switch(valNum, as_callable=False, fallthrough=True) as s:
        s.fcase(f_name=foobar, f_kwargs=())
        s.default(None)


def test_case_args_err():
    # args in case, passed in as the wrong type
    with switch(valCall,) as s:
        s.as_callable = True
        s.case(5, func=foofoo, args={})
        s.default(None)


def test_case_kwargs_err():
    # kwargs in case, passed in as the wrong type
    with switch(Bar('test'),) as s:
        s.as_callable = True
        s.case(Bar('test'), func=foobar, kwargs=())
        s.default(None)


def test_icase_args_err():
    # args in icase, passed in as the wrong type
    with switch(valTup, as_callable=False,) as s:
        s.allow_fallthrough = True
        s.icase((2, 3, 4), func=foofoo, args={})
        s.default(None)


def test_icase_kwargs_err():
    # kwargs in icase, passed in as the wrong type
    with switch(valNum, as_callable=False, fallthrough=True) as s:
        s.icase(foofoo, func=lambda **kwargs: print(kwargs), kwargs=[])
        s.default(None)

