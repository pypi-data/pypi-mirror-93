Convenience facilities for objects.

*Latest release 20210131*:
SingletonMixin: new _singleton_also_indexmap method to return a mapping of secondary keys to values to secondary lookup, _singleton_also_index() to update these indices, _singleton_also_by to look up a secondary index.

## Function `as_dict(o, selector=None)`

Return a dictionary with keys mapping to the values of the attributes of `o`.

Parameters:
* `o`: the object to map
* `selector`: the optional selection criterion

If `selector` is omitted or `None`, select "public" attributes,
those not commencing with an underscore.

If `selector` is a `str`, select attributes starting with `selector`.

Otherwise presume `selector` is callable
and select attributes `attr` where `selector(attr)` is true.

## Function `copy(obj, *a, **kw)`

Convenient function to shallow copy an object with simple modifications.

Performs a shallow copy of `self` using copy.copy.

Treat all positional parameters as attribute names, and
replace those attributes with shallow copies of the original
attribute.

Treat all keyword arguments as (attribute,value) tuples and
replace those attributes with the supplied values.

## Function `flavour(obj)`

Return constants indicating the ``flavour'' of an object:
* `T_MAP`: DictType, DictionaryType, objects with an __keys__ or keys attribute.
* `T_SEQ`: TupleType, ListType, objects with an __iter__ attribute.
* `T_SCALAR`: Anything else.

## Class `O(types.SimpleNamespace)`

The `O` class is now obsolete, please subclass `types.SimpleNamespace`.

## Function `O_attritems(o)`

Generator yielding `(attr,value)` for relevant attributes of `o`.

## Function `O_attrs(o)`

Yield attribute names from `o` which are pertinent to `O_str`.

Note: this calls `getattr(o,attr)` to inspect it in order to
prune callables.

## Function `O_merge(o, _conflict=None, _overwrite=False, **kw)`

Merge key:value pairs from a mapping into an object.

Ignore keys that do not start with a letter.
New attributes or attributes whose values compare equal are
merged in. Unequal values are passed to:

    _conflict(o, attr, old_value, new_value)

to resolve the conflict. If _conflict is omitted or None
then the new value overwrites the old if _overwrite is true.

## Function `O_str(o, no_recurse=False, seen=None)`

Return a `str` representation of the object `o`.

Parameters:
* `o`: the object to describe.
* `no_recurse`: if true, do not recurse into the object's structure.
  Default: `False`.
* `seen`: a set of previously sighted objects
  to prevent recursion loops.

## Function `obj_as_dict(*args, **kwargs)`

OBSOLETE convesion of an object to a `dict`. Please us `cs.obj.as_dict`.

## Class `Proxy`

An extremely simple proxy object
that passes all unmatched attribute accesses to the proxied object.

Note that setattr and delattr work directly on the proxy, not the proxied object.

## Function `singleton(registry, key, factory, fargs, fkwargs)`

Obtain an object for `key` via `registry` (a mapping of `key`=>object).
Return `(is_new,object)`.

If the `key` exists in the registry, return the associated object.
Otherwise create a new object by calling `factory(*fargs,**fkwargs)`
and store it as `key` in the `registry`.

The `registry` may be any mapping of `key`s to objects
but will usually be a `weakref.WeakValueDictionary`
in order that object references expire as normal,
allowing garbage collection.

*Note*: this function *is not* thread safe.
Multithreaded users should hold a mutex.

See the `SingletonMixin` class for a simple mixin to create
singleton classes,
which does provide thread safe operations.

## Class `SingletonMixin`

A mixin turning a subclass into a singleton factory.

*Note*: this mixin overrides `object.__new__`
and may not play well with other classes which oeverride `__new__`.

*Warning*: because of the mechanics of `__new__`,
the instance's `__init__` method will always be called
after `__new__`,
even when a preexisting object is returned.
Therefore that method should be sensible
even for an already initialised
and probably subsequently modified object.

One approach might be to access some attribute,
and preemptively return if it already exists.
Example:

    def __init__(self, x, y):
        if hasattr(self, 'x'):
            return
        self.x = x
        self.y = y

*Note*: each class registry has a lock,
which ensures that reuse of an object
in multiple threads will call the `__init__` method
in a thread safe serialised fashion.

Implementation requirements:
a subclass should:
* provide a method `_singleton_key(*args,**kwargs)`
  returning a key for use in the single registry,
  computed from the positional and keyword arguments
  supplied on instance creation
  i.e. those which `__init__` would normally receive.
  This should have the same signature as `__init__`
  but using `cls` instead of `self`.
* provide a normal `__init__` method
  which can be safely called again
  after some earlier initialisation.

This class is thread safe for the registry operations.

Example:

    class Pool(SingletonMixin):

        @staticmethod
        def _singleton_key(foo, bah=3):
            return foo, bah

        def __init__(self, foo, bah=3):
            if hasattr(self, 'foo'):
                return
           ... normal __init__ stuff here ...
           self.foo = foo
           ...

## Class `TrackedClassMixin`

A mixin to track all instances of a particular class.

This is aimed at checking the global state of objects of a
particular type, particularly states like counters. The
tracking is attached to the class itself.

The class to be tracked includes this mixin as a superclass and calls:

    TrackedClassMixin.__init__(class_to_track)

from its __init__ method. Note that `class_to_track` is
typically the class name itself, not `type(self)` which would
track the specific subclass. At some relevant point one can call:

    self.tcm_dump(class_to_track[, file])

`class_to_track` needs a `tcm_get_state` method to return the
salient information, such as this from cs.resources.MultiOpenMixin:

    def tcm_get_state(self):
        return {'opened': self.opened, 'opens': self._opens}

See cs.resources.MultiOpenMixin for example use.

### Method `TrackedClassMixin.tcm_all_state(klass)`

Generator yielding tracking information
for objects of type `klass`
in the form `(o,state)`
where `o` if a tracked object
and `state` is the object's `get_tcm_state` method result.

### Method `TrackedClassMixin.tcm_dump(klass, f=None)`

Dump the tracking information for `klass` to the file `f`
(default `sys.stderr`).

# Release Log



*Release 20210131*:
SingletonMixin: new _singleton_also_indexmap method to return a mapping of secondary keys to values to secondary lookup, _singleton_also_index() to update these indices, _singleton_also_by to look up a secondary index.

*Release 20210122*:
SingletonMixin: new _singleton_instances() method returning a list of the current instances.

*Release 20201227*:
SingletonMixin: correctly invoke __new__, a surprisingly fiddly task to get right.

*Release 20201021*:
* @OBSOLETE(obj_as_dict), recommend "as_dict()".
* [BREAKING] change as_dict() to accept a single optional selector instead of various mutually exclusive keywords.

*Release 20200716*:
SingletonMixin: no longer require special _singleton_init method, reuse default __init__ implicitly through __new__ mechanics.

*Release 20200517*:
Documentation improvements.

*Release 20200318*:
* Replace obsolete O class with a new subclass of SimpleNamespace which issues a warning.
* New singleton() generic factory function and SingletonMixin mixin class for making singleton classes.

*Release 20190103*:
* New mixin class TrackedClassMixin to track all instances of a particular class.
* Documentation updates.

*Release 20170904*:
Minor cleanups.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* Minor tweaks.

*Release 20150118*:
move long_description into cs/README-obj.rst

*Release 20150110*:
cleaned out some old junk, readied metadata for PyPI
