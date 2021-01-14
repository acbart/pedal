"""
Holds the SandboxResult proxy that emulates other classes as perfectly
as possible.
"""

# This module provides a version of ``len`` that handles SandboxResult
#   correctly, requiring us to hold a reference to the original ``len``.
import math

_original_len = len


class SandboxResult:
    """
    Proxy class for wrapping results from executing student code. Attempts
    to perfectly emulate the underlying data value, so that users will never
    realize they have a proxy. The advantage is that special information is
    available in the corresponding Sandbox about this result that can give
    more context.
    
    Attributes:
        value (any): The actual data stored in this class that we are proxying.
            If the underlying proxy object has a field called `value`, then
            you can use either `_actual_value` to access the proxied object.
        _actual_context_id (int): The call that was used to generate this result.
        _actual_sandbox (Sandbox): The sandbox that was used to generate this
            result. If None, then the sandbox was lost.
    
    """
    ASSIGNABLE_ATTRS = ['value', '_actual_context_id', '_actual_sandbox',
                        '_clone_this_result']

    def __init__(self, value, context_id=None, sandbox=None):
        """
        Args:
            value (any): Literally any type of data.
            context_id (int): The unique call ID that generated this result. If
                None, then the SandboxResult was generated by manipulating an earlier
                result.
                TODO: We could actually remember the operations applied to this
                    instance and use them to reconstruct the transformations...
            sandbox (Sandbox): The sandbox that was used to generate this
                result. If None, then the sandbox was lost.
        """
        self.value = value
        self._actual_context_id = context_id
        self._actual_sandbox = sandbox

    def __getattribute__(self, name):
        """
        Get the attribute with the given `name`. This allows us to pass
        most attributes along to the underlying `value`, while still
        maintaining access to the proxy's attributes.
        """
        v = object.__getattribute__(self, "value")
        if name == "__class__":
            return v.__class__
        elif name == "__actual_class__":
            return object.__getattribute__(self, "__class__")
        elif name == "_actual_value":
            return v
        elif name in SandboxResult.ASSIGNABLE_ATTRS:
            return object.__getattribute__(self, name)
        elif name == "value" and not hasattr(v, "value"):
            return v
        else:
            return SandboxResult(object.__getattribute__(v, name),
                                 object.__getattribute__(self, "_actual_context_id"),
                                 object.__getattribute__(self, "_actual_sandbox"))

    def __setattr__(self, name, value):
        if name in SandboxResult.ASSIGNABLE_ATTRS:
            object.__setattr__(self, name, value)
        else:
            setattr(self.value, name, value)

    def __delattr__(self, name):
        if name in SandboxResult.ASSIGNABLE_ATTRS:
            object.__delattr__(self, name)
        else:
            delattr(self.value, name)

    def _clone_this_result(self, new_value):
        """
        Create a new SandboxResult based on this current one. Copies over the
        `context_id` and `sandbox`.
        
        Args:
            new_value (any): The new value to be proxying.
        Returns:
            SandboxResult
        """
        return SandboxResult(new_value,
                             context_id=self._actual_context_id,
                             sandbox=self._actual_sandbox)

    def __repr__(self):
        """
        Returns the representation of the proxied object.
        
        Returns:
            str: The `repr` of the proxied object.
        """
        return repr(self.value)

    def __str__(self):
        """
        Returns the string representation of the proxied object.
        
        Returns:
            str: The `str` of the proxied object.
        """
        return str(self.value)

    def __bytes__(self):
        return bytes(self.value)

    def __format__(self, format_spec):
        return format(self.value, format_spec)

    def __call__(self, *args):
        """
        Returns the result of calling the proxied object with the args.
        
        Returns:
            SandboxResult: A proxy of the Sandbox object.
        """
        return self._clone_this_result(self.value(*args))

    def __hash__(self):
        return hash(self.value)

    def __bool__(self):
        return bool(self.value)

    def __dir__(self):
        return dir(self.value)

    def __instancecheck__(self, instance):
        return isinstance(self.value, instance)

    def __subclasscheck__(self, subclass):
        return issubclass(self.value, subclass)

    def __len__(self):
        """
        Fun fact: cpython DEMANDS that __len__ return an integer. Not something
        that looks like an integer, but a true, honest-to-god integer that
        can fit into a slot.
        https://stackoverflow.com/questions/42521449/how-does-python-ensure-the-return-value-of-len-is-an-integer-when-len-is-cal
        """
        return _original_len(self.value)

    def __getitem__(self, key):
        return self._clone_this_result(self.value[key])

    def __setitem__(self, key, value):
        self.value[key] = value

    def __delitem__(self, key):
        del self.value[key]

    def __missing__(self, key):
        return self.value.__missing__(key)

    def __iter__(self):
        return iter(self.value)

    def __reversed__(self):
        return reversed(self.value)

    def __contains__(self, item):
        return self.value.__contains__(item)

    def __eq__(self, other):
        """
        Test if the proxied object is equal to the given `other`.
        
        Args:
            other (any): The other object.
        
        Returns:
            bool or any: Returns whatever the proxy object's __eq__ returns.
        """
        if isinstance(other, SandboxResult):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, SandboxResult):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, SandboxResult):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, SandboxResult):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, SandboxResult):
            return self.value >= other.value
        return self.value >= other

    def __ne__(self, other):
        if isinstance(other, SandboxResult):
            return self.value != other.value
        return self.value != other

    # Numeric Operations

    def __add__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value + other.value)
        return self._clone_this_result(self.value + other)

    def __sub__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value - other.value)
        return self._clone_this_result(self.value - other)

    def __mul__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value * other.value)
        return self._clone_this_result(self.value * other)

    def __matmul__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__matmul__(other.value))
        return self._clone_this_result(self.value.__matmul__(other))

    def __truediv__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__truediv__(other.value))
        return self._clone_this_result(self.value.__truediv__(other))

    def __floordiv__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__floordiv__(other.value))
        return self._clone_this_result(self.value.__floordiv__(other))

    def __mod__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__mod__(other.value))
        return self._clone_this_result(self.value.__mod__(other))

    def __divmod__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__divmod__(other.value))
        return self._clone_this_result(self.value.__divmod__(other))

    def __pow__(self, other, *modulo):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__pow__(other.value, *modulo))
        return self._clone_this_result(self.value.__pow__(other, *modulo))

    def __lshift__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__lshift__(other.value))
        return self._clone_this_result(self.value.__lshift__(other))

    def __rshift__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__rshift__(other.value))
        return self._clone_this_result(self.value.__rshift__(other))

    def __and__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__and__(other.value))
        return self._clone_this_result(self.value.__and__(other))

    def __xor__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__xor__(other.value))
        return self._clone_this_result(self.value.__xor__(other))

    def __or__(self, other):
        if isinstance(other, SandboxResult):
            return self._clone_this_result(self.value.__or__(other.value))
        return self._clone_this_result(self.value.__or__(other))

    def __radd__(self, other):
        if isinstance(self.value, str):
            return self._clone_this_result(self.value.__add__(other))
        return self._clone_this_result(self.value.__radd__(other))

    def __rsub__(self, other):
        return self._clone_this_result(self.value.__rsub__(other))

    def __rmul__(self, other):
        return self._clone_this_result(self.value.__rmul__(other))

    def __rmatmul__(self, other):
        return self._clone_this_result(self.value.__rmatmul__(other))

    def __rtruediv__(self, other):
        return self._clone_this_result(self.value.__rtruediv__(other))

    def __rfloordiv__(self, other):
        return self._clone_this_result(self.value.__rfloordiv__(other))

    def __rmod__(self, other):
        return self._clone_this_result(self.value.__rmod__(other))

    def __rdivmod__(self, other):
        return self._clone_this_result(self.value.__rdivmod__(other))

    def __rpow__(self, other):
        return self._clone_this_result(self.value.__rpow__(other))

    def __rlshift__(self, other):
        return self._clone_this_result(self.value.__rlshift__(other))

    def __rand__(self, other):
        return self._clone_this_result(self.value.__rand__(other))

    def __rxor__(self, other):
        return self._clone_this_result(self.value.__rxor__(other))

    def __ror__(self, other):
        return self._clone_this_result(self.value.__ror__(other))

    # TODO: __iadd__ and other in-place assignment operators?

    def __neg__(self):
        return self._clone_this_result(self.value.__neg__())

    def __pos__(self):
        return self._clone_this_result(self.value.__pos__())

    def __abs__(self):
        return self._clone_this_result(self.value.__abs__())

    def __invert__(self):
        return self._clone_this_result(self.value.__invert__())

    def __complex__(self):
        return self._clone_this_result(self.value.__complex__())

    def __int__(self):
        return int(self.value)
        #return self._clone_this_result(int(self.value))
        #return self._clone_this_result(self.value.__int__())

    def __float__(self):
        return self._clone_this_result(self.value.__float__())

    def __round__(self, *ndigits):
        return self._clone_this_result(self.value.__round__(*ndigits))

    def __trunc__(self):
        return math.truncate(self.value)

    def __floor__(self):
        return self._clone_this_result(self.value.__floor__())

    def __ceil__(self):
        return self._clone_this_result(self.value.__ceil__())

    def __enter__(self):
        return self.value.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.value.__exit__(exc_type, exc_value, traceback)

    def __await__(self):
        return self.value.__await__()

    def __aiter__(self):
        return self.value.__aiter__()

    def __anext__(self):
        return self.value.__anext__()

    def __aenter__(self):
        return self.value.__aenter__()

    def __aexit__(self, exc_type, exc_value, traceback):
        return self.value.__aexit__(exc_type, exc_value, traceback)

    def __index__(self):
        return self.value.__index__()


def is_sandbox_result(value) -> bool:
    """
    Determines if the given value is secretly a proxied SandboxResult.
    """
    if hasattr(value, "__actual_class__"):
        if value.__actual_class__ == SandboxResult:
            return True
    return False


def len(s):
    """
    Return the length (the number of items) of an object. The argument may be
    a sequence (such as a string, bytes, tuple, list, or range) or a collection
    (such as a dictionary, set, or frozen set).

    Replacement for builtin :py:func:`len` function that is compatible
    with SandboxResult. See
    :py:func:pedal.sandbox.result.SandboxResult.__len__ for details on this
    weird thing.
    """
    if is_sandbox_result(s):
        return s._clone_this_result(_original_len(s.value))
    return len(s)


def share_sandbox_context(new_value, original_value):
    """ Produces a new version of the `new_value`, but using the sandbox,
    context ID, and metadata of the `original_value`."""
    if is_sandbox_result(original_value):
        return SandboxResult(new_value,
                             original_value._actual_context_id,
                             original_value._actual_sandbox)
    return new_value
