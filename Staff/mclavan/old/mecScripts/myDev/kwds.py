[Tutor] kwds

John Fouhy john at fouhy.net 
Wed Apr 11 07:41:37 CEST 2007
Previous message: [Tutor] kwds
Next message: [Tutor] urllib2_realm??
Messages sorted by: [ date ] [ thread ] [ subject ] [ author ]
On 11/04/07, Adam Pridgen <atpridgen at mail.utexas.edu> wrote:
> Hello,
>
> I am having a difficult time understanding the whole "def
> function(*args, **kwds):" business, and I have not really found a
> clear or concise explanation via Google.
>
> My question is pretty much this, is **kwds a dictionary and can I use
> it like a dictionary, and what is the deal with the * or **?

Short answer: kwds is a dictionary.

Longer answer:

You can use *args and **kwargs to collect "extra" positional and
keyword parameters.  This is easier to demonstrate than explain, so I
will try to illustrate with examples.

Here's a function that takes two arguments:

>>> def f(x, y):
...  print x, y
...

I can call it:

>>> f(1, 3)
1 3

But if I try to call it with more than two arguments, python complains:

>>> f(1, 3, 5)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: f() takes exactly 2 arguments (3 given)

Here's another function.  This one takes _at least_ two arguments:

>>> def f(x, y, *extra):
...  print x, y, extra
...

I can call it as before.  Notice that 'extra' is a 0-tuple:

>>> f(1, 2)
1 2 ()

I can also give it some extra positional arguments.  Python will take
the first two positional arguments and assign them the local names 'x'
and 'y', and it will put the remaining positional arguments into a
tuple, and call that 'extra'.

>>> f(1, 2, 3, 4, 5)
1 2 (3, 4, 5)

But f has two named parameters, so I need to give it _at least_ two arguments.

>>> f(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: f() takes at least 2 arguments (1 given)

Finally, f doesn't handle keyword arguments.

>>> f(1, 2, foo=3)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: f() got an unexpected keyword argument 'foo'

Here's a function that takes two keyword arguments:

>>> def f(x=1, y=2):
...  print x, y
...

I can use it as normal:

>>> f(y=5)
1 5

But if I give it a keyword argument it doesn't expect, python complains:

>>> f(y=5, z=9)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: f() got an unexpected keyword argument 'z'

Here's another function.  This function will collect undeclared
keyword arguments into a dictionary.

>>> def f(x=1, y=2, **kwargs):
...  print x, y, kwargs
...

If I don't give any extra keyword arguments, the dictionary is empty.

>>> f()
1 2 {}

If I do, the dictionary will be populated.  I hope you can see the
connection between the keyword arguments and the dictionary structure.

>>> f(z=9, foo='bar')
1 2 {'z': 9, 'foo': 'bar'}

**kwargs will only collect keyword arguments.  So if I provide extra
positional arguments, python will still complain.

>>> f(1, 2, 3)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: f() takes at most 2 arguments (3 given)

You can combine explicit positional and keyword arguments and the
*args / **kwargs forms.  I hope it should be obvious how things work;
if it's not, experiment :-)

You can also use the syntax in the opposite direction (as it were).
If 'args' is a list and you use '*args' in a function call, python
will expand args into positional parameters.

eg, here is a function:

>>> def f(x, y, *args):
...  print 'x:%s, y:%s, args:%s' % (x, y, args)
...

I can call it with four positional parameters:

>>> f(1, 2, 3,4)
x:1, y:2, args:(3, 4)

Or I can build a list of four elements, and convert the list into
positional parameters:

>>> lst = [1, 2, 3, 4]
>>> f(*lst)
x:1, y:2, args:(3, 4)

You can do the same thing with keyword arguments and dictionaries:

>>> def f(x=1, y=2, **kw):
...  print 'x:%s, y:%s, kw:%s' % (x, y, kw)
...
>>> args = {'y':9, 'z':13, 'k':42}
>>> f(**args)
x:1, y:9, kw:{'k': 42, 'z': 13}

And, obviously, you can combine both of these.

You might commonly see this when dealing with inheritance -- a
subclass will define some of its own parameters, and use *args/**kw to
collect any other arguments and pass them on to the base class.  eg:

class MySubClass(BaseClass):
    def __init__(self, x, y, foo='foo', *args, **kw):
        BaseClass.__init__(*args, **kw)
        # Do stuff with x, y, foo

> and I have not really found a clear or concise explanation via Google.

I don't think this counts as "concise", but I hope it is clear :-)

-- 
John.
Previous message: [Tutor] kwds
Next message: [Tutor] urllib2_realm??
Messages sorted by: [ date ] [ thread ] [ subject ] [ author ]
More information about the Tutor mailing list
