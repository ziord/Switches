<div align="center">
<img alt="leap image" src="assets/switches_256x256.png"/>
</div>

<div align="center">
<h1>Documentation</h1>
</div>


<br/>

## Table of Contents

- [Importing switch](#importing-switches)
- [The switch Context Manager](#switch-ctx-manager)
- [Meet the Modes: Fallthrough vs No Fallthrough](#ft-vs-nft)
    - [No-Fallthrough Mode](#nft-mode)
    - [Fallthrough Mode](#ft-mode)
- [Three Kinds of Cases](#cases)
- [switch.case](#switch-case)
- [switch.c_break](#switch-cbreak)
- [switch.icase](#switch-icase)
- [switch.fcase](#switch-fcase)
- [switch.default](#switch-default)
- [switch.as_callable](#switch-as-callable) 
- [switch.allow_fallthrough](#switch-allow-ft)
- [switch.allow_duplicates](#allow-dup)
- [switch.no_warning](#switch-no-warn)
- [switch.value](#switch-value)


\
\
<a name='importing-switches'></a>
## Importing `switch`

You can import the `switch` context manager as shown in the code snippet below:

```python
from switches.switch import switch
```

The code snippets that follows from here assumes this import is already made.

\
\
<a name='switch-ctx-manager'></a>
## The `switch` Context Manager

In the heart of Switches, is the `switch` context manager with the signature:
```python
switch(value, args=(), kwargs=None, fallthrough=False, allow_duplicates=True,
       as_callable=False, no_warning=False) 

```
`value` is the default value passed to the constructor. 
This is the value for which we compare against, in the case branches. It can be a regular value (`int`, `float`, etc.) or a `callable`.

When `value` is a `callable`, `as_callable` must be set to `True`.

More details about `as_callable` can be found [here.](#switch-as-callable)

The parameters `args` and `kwargs` are discussed [here.](#switch-args-kwargs)

Other parameters that can be passed to the constructor includes `fallthrough`, `allow_duplicates` and `no_warning`.

These are discussed in the rest of the documentation.
\
\
<a name='ft-vs-nft'></a>
## Meet the Modes: Fallthrough vs No Fallthrough

Fallthrough is what happens when execution drops from a matching case (one without a `break` specified) statement (after such case has been executed) to the _next_ case statement(s) (it continues dropping) if any (or even a default statement) in the switch block. 

[Wikipedia](https://en.wikipedia.org/wiki/Switch_statement) explains it as a scenario where control moves to the matching case, and then execution continues ("falls through") to the statements associated with the next case in the source text.

In Switches, the above definitions accounts for a `case`, `fcase` and `icase`.
<a name='default-mode'></a>
Fallthrough is not enabled by default in Switches, and it happens when you do not add a `break` statement ([c_break](#switch-cbreak) to be specific)  to each `case`, `fcase` or `icase` statement. 

Switches has two modes: 
- Fallthrough Mode
- No-Fallthrough Mode

The `switch` constructor provides a `fallthrough` argument which is disabled (`False`) by default. This implies that the default mode is **No Fallthrough.**

<br/>
<a name='nft-mode'></a>

### No-Fallthrough Mode
------------------------
In No-Fallthrough Mode (`fallthrough=False`), implicit breaks are automatically added to each `case` `fcase` or `icase` statement when the user leaves out or forgets to add a `c_break` statement (or pass in the `c_break` parameter) for a corresponding `case`, `fcase` or `icase`. 

That is:

```python
with switch(value, fallthrough=False) as s:
     s.case(test1)
     s.case(test2)
```

Is equivalent to:

```python
with switch(value) as s:
     s.case(test1)
     s.c_break()
     s.case(test2)
     s.c_break()
```

Thus explicit `c_breaks` can be omitted in No-Fallthrough Mode.

As stated [earlier](#default-mode), the default mode in Switches is No Fallthrough.

Hence, there's no need to specify `fallthrough=False` in the switch constructor if **No-Fallthrough Mode** is desired. 

The implication of No-Fallthrough Mode is that control never drops off to the succeeding statement (`case`, `icase`, `fcase`, or even `default` if any) when a "match" is found for any of the statements.

Although this can be overridden, by simply setting the `c_break` parameter to `False` in any of the case statements (`case`, `icase`, `fcase`). More details can be found [here](#switch-case)

<br/>
<a name='ft-mode'></a>

### Fallthrough Mode
------------------------

In Fallthrough Mode, implicit addition of `c_break`s is turned off.
That is, if a user leaves out or forgets to add an explicit `c_break` statement (or forgets to set `c_break` to `True` in any of the case types - `case`, `icase`, `fcase`), then control will fall through every succeeding case of a matched case.

In code:

```python
value = get_value()
with switch(value, fallthrough=True) as s:
    s.case(1, lambda: print("in case 1"))
    s.case(5, lambda: print("in case 5"))
    s.case(7, lambda: print("in case 7"))
    s.default(lambda: print("Default reached!"))
```

When `value` is `5`, the code snippet above would produce the output:

```
in case 5
in case 7 
Default reached!
```

Since `value` is `5`, it matches `s.case(5, ...)` and because it's in **Fallthrough Mode** (Switches turns off implicit addition of `c_break` statements), and no `c_break` was set (that is, passed in as a parameter to `case`) or declared after a `case` statement (that is, `s.c_break()` wasn't used) in any of the cases, control drops off to `s.case(7, ...)`, and then to `s.default(...)` (for the same reasons!)

This is the implication of Fallthrough Mode without explicit break statements.

Although Fallthrough Mode might seem terrible due to its implications or "side-effects" (especially when `c_break` is omitted unintentionally), but this can also have "advantages".

For instance, one can match multiple cases in Fallthrough Mode:


```python
with switch(value, fallthrough=True) as s:
    s.case(1, lambda: print("in case 1"))
    s.case(5)  # yes we can specify only the value! more details in switch.case section.
    s.case(6)  
    s.case(7, lambda: print("in case 7"))
    s.default(lambda: print("Default reached!"))
```

In the snippet above, the output when `value` is `5`, `6` or `7` would be:   
```
in case 7
Default reached!
```

This is because when `value` is `5`, it'll match `s.case(5)` and fall through to `s.case(6)`, `s.case(7, lambda: print("in case 7"))` and `s.default(lambda: print("Default reached!"))`.

Also when `value` is `7`, `s.case(7...)` and `s.default(lambda: print("Default reached!"))` would be executed (fallthrough). 
<a name='catch-many'></a>
It thus acts like a "catch many" feature, although, `switch.icase` may be better suited for this purpose.

You can also switch modes besides passing `fallthrough=False` to the switch constructor. 
More details [here.](#switch-allow-ft)
    
As you may have noticed, the functions passed to the case statements gets executed when a case is matched.
More details can be found [here.](#switch-case)

\
\
<a name='cases'></a>
## Three Kinds of Cases
In Switches, there are three kinds of cases namely, 
- `case`: which is the "regular" case used in switch statements
- `fcase`: case for callables
- `icase`: case for iterables

Onward, the use of "case statement" or "case" would refer to any of the three kinds listed above.
\
\
<a name='switch-case'></a>
## `switch.case`

The `switch.case` method has the signature:

```python
switch.case(value, func=None, args=(), kwargs=None, c_break=None)
```
- `value`: The value to be matched.
<a name="f-a-k-c-attributes"></a>
- `func`:  The function that is called when the case is matched. `func` must be a `callable`. If not, it is ignored even if the case is matched.

- `args`: The actual arguments to be passed to the function (passed in as `func`) if it takes any. `args` must be of `list`, `tuple` or `set` type. If otherwise, a `SwitchError` is raised.

- `kwargs`: The arguments passed as keyword arguments to the function (passed in as `func`) if it takes any. `kwargs` must be of dict type, if otherwise, a `SwitchError` is raised. 

- `c_break`: This can be set to `True` or `False` in any case statement, this is equivalent to an explicit `s.c_break()` statement after a case statement.


For example, given a function `foo`:

```python
def foo():
    pass
```
The snippet:

```python
with switch(value):
    s.case(xy, func=foo, c_break=True)
```

In **No-Fallthrough Mode**, is equivalent to:

```python
with switch(value):
    s.case(xy, func=foo)
    s.c_break()
```

Using `args` and `kwargs`:

```python
def bar(x, y):
    print(x * y)

with switch(value):
    s.case(num, func=bar, args=(1,2), c_break=True)
```

Alternatively:

```python
with switch(value):
    s.case(num, func=bar, kwargs={"x": 1, "y": 2}, c_break=True)
```

For any given case, once control drops to such case (the case is "matched"), the `func` argument, if specified, is evaluated. 

\
\
<a name='switch-cbreak'></a>
## `switch.c_break`

Break statements within switch blocks help prevent fallthrough from happening after a matched case is executed; they "break" execution flow after a matched case has been completely executed.

Switches provides `c_break` which can be used to add break statements to a corresponding case statement.

For example:

```python
with switch(foo) as s:
    s.case("a", bar)
    s.c_break()
    s.case("b", nov)
    s.c_break()
    s.default(None)
```
`c_break` should not be used before a case is declared,  it should not be used twice for a single case or `default` statement. This would result in a `SwitchError` if done. 

Also, adding `c_break` after a `default` statement is irrelevant and would produce a **warning.**

In No-Fallthrough Mode, (when fallthrough isn't desired), adding `c_break` after a case statement is irrelevant and redundant. 

-------------------------
#### A Note about `c_break`
`c_break` can be used to "override" a `switch` block's current mode.

<br/>

#### <ins>In Fallthrough Mode </ins>

Setting `c_break` to `True` would prevent a usual fallthrough.

Consider the code snippet below:

```python
with switch(value, fallthrough=True) as s:
    s.case(1, lambda: print("in case 1"), c_break=True)
    s.case(5, lambda: print("in case 5"))
    s.case(7, lambda: print("in case 7"))
    s.default(lambda: print("Default reached!"))
```

The code snippet above is in Fallthrough Mode. However, if `value` is `1`, we would have the following output:
```
in case 1
```

This is because `c_break` was set in `s.case(1, ...)` thus preventing control from falling through the entire cases (and `default` statement) like it would normally do.
<br/>

#### <ins>In No-Fallthrough Mode</ins>

Setting `c_break` to `False` in a case would actually cause a fallthrough if that case matches.

Consider the code snippet below:

```python
with switch(value, fallthrough=False) as s:
    s.case(1, lambda: print("in case 1"), c_break=False)
    s.case(5, lambda: print("in case 5"))
    s.case(7, lambda: print("in case 7"))
    s.default(lambda: print("Default reached!"))
```

The code snippet above is in No-Fallthrough Mode. However, if `value` is `1`, we would have the following output:
```
in case 1
in case 5
```

Control goes to `s.case(1, ...)` because `value` is `1`, however, unlike the regular case, `c_break` is specified as False, this turns off implicit addition of c_break in Fallthrough Mode, causing control to fall through to `s.case(5, ...)` after `s.case(1, ...)` has been executed. 

Since `s.case(5, ...)` does not explicitly turn off `c_break` like `s.case(1, ...)` does, fallthrough is halted abruptly.


------------------------

\
\
<a name='switch-icase'></a>
## `switch.icase`

The `switch.icase` method has the signature:

```python
switch.icase(iterable, func=None, args=(), kwargs=None, c_break=None)
```

- `iterable`: any iterable value

`iterable` must be a Python iterable (must implement the iterable protocol), if not a `SwitchError` is raised.

The other arguments `func`, `args`, `kwargs` and `c_break` behave exactly as described in [switch.case](#f-a-k-c-attributes)

This should be used when `value` is an iterable. Here, the value being checked is compared with items in the iterable, and if a match is found, control would yield to `icase`, depending on context (Fallthrough, No-Fallthrough, previous cases, etc.)

For example:

```python
with switch(value) as s:
    s.case(12, lambda: print("in case"), c_break=False)
    s.icase(range(10), lambda: print("in icase"))
    s.case(7, lambda: print("in case 7"))
    s.default(lambda: print("Default reached!"))
```

If `value` is between the range of `1` and `9`, `s.icase(...)` would be matched and its `func` would be executed. As explained [earlier](#catch-many), `icase` works effectively as a "catch-many" kind of case.   

\
\
<a name='switch-fcase'></a>
## `switch.fcase`

The `switch.fcase` method has the signature:

```python
switch.fcase(f_name, f_args=(), f_kwargs=None, func=None, args=(), kwargs=None, c_break=None)
```
- `f_name`: any callable value. That is if `foo()` is a callable, then `f_name` is `foo`.
- `f_args`: arguments to the callable `f_name` (must be of type `list`, `set`, or `tuple`)
- `f_kwargs`: keyword arguments to the callable `f_name` (must be of type `dict`)

`f_name` must be a Python `callable`, if not a `SwitchError` is raised. <br /> `f_args` must be of `list`, `set` or `tuple` type, if not, a `SwitchError` is raised. <br /> `f_kwargs` must be of type `dict`, else a `SwitchError` is raised.

The other arguments `func`, `args`, `kwargs` and `c_break` behave exactly as described in [switch.case](#f-a-k-c-attributes)

`fcase` should be used with callables. Specifically, when the result of (calling a) callable is to be considered as a case.

---------
**NOTE:** 
`fcase` is a ***keyword-only*** method.
Hence, values must be passed as keyword arguments.

---------

A simple example:

```python
def foo(x, y):
    return x * y

def bar(a, b):
    return a+b

value = get_value()

with switch(value) as s:
    s.case(12, lambda: print("in case"), c_break=False)
    s.fcase(f_name=foo, f_args=[2, 3], func=lambda: print("in fcase 1"))
    s.fcase(f_name=bar, f_kwargs={'a': 2, 'b': 2}, func=lambda: print("in fcase 2"))
    s.default(lambda: print("Default reached!"))
```
In the snippet above, when `value` is `6`, the first `fcase` would be matched (because the result of `foo(2, 3)` is `6`).
When `value` is `4`, the second `fcase` would be matched (because the result of `bar(2, 2)` is `4`).

\
\
<a name='switch-default'></a>
## `switch.default`

The `switch.default` method has the signature:

```python
switch.default(func=None, args=(), kwargs=None, c_break=None)
```

The arguments `func`, `args`, `kwargs` and `c_break` behave exactly as described in [switch.case](#f-a-k-c-attributes)

When no case is executed (no "match"), control yields to `default` if specified. 
Its `func` is executed, if specified. 

```python
with switch(foo) as s:
    s.case("a", bar)
    s.case("b", nov)
    s.default(default_stuff)
```

If the `default` statement is omitted, a warning (`UserWarning: Default statement omitted`) is issued.

Alternatively, if there's "no need" for a default statement in your code, you could just call default without passing any arguments, or simply passing `None`.

```python
with switch(foo) as s:
    s.case("a", bar)
    s.case("b", nov)
    s.default()  # or s.default(None)
```

\
\
<a name='switch-as-callable'></a>
## `switch.as_callable`

Sometimes, you might want to perform an action based on the result of a `callable`.

Switches provides the `as_callable` parameter and property for such instance. 

You pass in a `callable` instead of a regular value in the `switch`'s constructor and set `as_callable` to `True`.

The code snippet below:

```python
value = get_value()
with switch(value) as s:
    s.case(1, do_stuff)
    s.case(7, get_openings)
    s.default(lambda: print("Default reached!"))
```

Could be rewritten as:

```python
with switch(get_value, as_callable=True) as s:
    s.case(1, do_stuff)
    s.case(7, get_openings)
    s.default(lambda: print("Default reached!"))
```

Or using the `as_callable` property:

```python
with switch(get_value) as s:
    s.as_callable = True
    s.case(1, do_stuff)
    s.case(7, get_openings)
    s.default(lambda: print("Default reached!"))
```
<a name='switch-args-kwargs'></a>
For functions that take arguments, we could pass in those argument(s) using `args`, or `kwargs` arguments of the `switch` constructor.

For example:

```python
def get_value(x, y):
    return x * y

with switch(get_value, args=[2, 3]) as s:
    s.as_callable = True
    s.case(1, do_stuff)
    s.case(7, get_openings)
    s.default()
```
or using `kwargs`

```python
def get_value(x, y):
    return x * y

with switch(get_value, kwargs={'x': 2, 'y': 3}) as s:
    s.as_callable = True
    s.case(1, do_stuff)
    s.case(7, get_openings)
    s.default()
```

---------
**NOTE:**

`args` must be of type `list`, `set` or `tuple`. <br /> `kwargs` must be of type `dict`.

If otherwise, a `SwitchError` is raised.

---------

\
\
<a name='switch-allow-ft'></a>
## `switch.allow_fallthrough`

Switches also provides the `allow_fallthrough` property similar to `as_callable`. 
This implies that instead of passing the `fallthrough` parameter in the `switch` constructor, one could use the `allow_fallthrough` property.

For example:

```python
with switch(value) as s:
    s.allow_fallthrough = True
    s.case("fun", do_foo)
    s.default(None)
```

\
\
<a name='allow-dup'></a>
## `switch.allow_duplicates`

Switches provides the `allow_duplicates` argument both in the `switch` constructor and as a `switch` property.
This is set to `True` by default, and it implies that there can be multiple cases with the same `value` for a `case`, or `f_name` for an `fcase`.
This doesn't affect an `icase` however, as Switches allows duplicates on `icase`s whether `allow_duplicates` is turned off or not. 

`allow_duplicates` can be turned off in two ways: via the `switch` constructor or via the `allow_duplicates` property. 

**Examples:**

- Via the constructor:

```python
with switch(value, allow_duplicates=True) as s:
    s.case("fun", do_fun)
    s.default(None)
```

- Via the property:

```python
with switch(value) as s:
    s.allow_duplicates=True
    s.case("fun", do_fun)
    s.default(None)
```
\
\
<a name='switch-no-warn'></a>
## `switch.no_warning`

This shuts off all warnings in scenarios where a warning would have been issued.

By default, `no_warning` is set to `False`, implying that Switches will *warn* you depending on code context (for example, omitting a `default` statement in a `switch` block).

There are two ways to shut off warnings, 

- Using the `no_warning` argument in the `switch` constructor: 

```python
with switch(value, no_warning=True) as s:
    pass
```

- Using the `no_warning` property:

```python
with switch(value) as s:
    s.no_warning = True
```
\
\
<a name='switch-value'></a>
## `switch.value`

The value passed to the `switch` constructor's `value` argument can be referenced or accessed via the `switch.value` property.

For example:

```python
with switch(5, no_warning=True) as s:
    print(s.value)
```

The code snippet would produce the output:

```
5
```

If `value` is a `callable`, and with or without arguments, a call to `s.value` would produce the result of calling the `callable` passed.

That is:

```python
def get_value(x, y):
    return x * y

with switch(get_value, args=[2, 3]) as s:
    s.no_warnings = True
    print(s.value)
```
would output:

```
6
```
which is the result of calling `get_value` with the arguments passed, i.e. `get_value(2, 3)`


\
&copy; ziord.