import math
import operator
import funct.Array as A


class ASeq:
    __slots__ = []

    # make copy when 'dangerous function is called? 
    #   checkout itertools.tee

    # or just make warning docs? 
    #  " careful with all/foreach! it exhausts the sequence/iterator "

    def to_Array(self):
        """ Converts all iterables in the Array to Arrays """
        return A.Array(
            map(
                lambda e: A.Array(e).to_Array() if isinstance(e, A.Iterable) else e,
                self,
            )
        )

    def sum_(self, start=0):
        """ Returns the sum of the Array elements. """
        return sum(self, start)

    def product_(self, start=1):
        """ Returns the product of the Array elements. """
        return A.reduce(lambda a, b: a * b, self, start)

    def forall_(self, l):
        """
        Returns whether the specified predicate
        holds for all elements of this Array.
        """
        return all(map(l, self))

    def forany_(self, l):
        """
        Returns whether the specified predicate
        holds for any element of this Array.
        """
        return any(map(l, self))

    def foreach_(self, l):
        for e in self:
            l(e)

    def reduce_(self, l, init=None):
        """ Reduces the elements of this Array using the specified operator. """
        if init is not None:
            return A.reduce(l, self, init)
        return A.reduce(l, self)

    def maxby_(self, l):
        """ Finds the maximum value measured by a function. """
        return max(self, key=l)

    def minby_(self, l, **kwargs):
        """ Finds the minimum value measured by a function. """
        return min(self, key=l, **kwargs)

    def argmax_(self):
        """ Returns the index of the maximum value """
        return self.enumerate_.maxby_(lambda e: e[1])[0]

    def argmin_(self):
        """ Returns the index of the minimum value """
        return self.enumerate_.minby_(lambda e: e[1])[0]

    def all_(self):
        """ Returns true if bool(e) is True for all elements in this Array. """
        return all(self)

    def any_(self):
        """ Returns true if bool(e) is True for any element e in this Array. """
        return any(self)

    def max_(self, **kwargs):
        return max(self, **kwargs)

    def min_(self, **kwargs):
        return min(self, **kwargs)

    def add_(self, e):
        """
        Lazy element-wise addition with given scalar or sequence.
        """
        return self.__lazy_operate(operator.add, e)

    def sub_(self, e):
        """
        Lazy element-wise subtraction with given scalar or sequence.
        """
        return self.__lazy_operate(operator.sub, e)

    def mul_(self, e):
        """
        Lazy element-wise multiplication with given scalar or sequence.
        """
        return self.__lazy_operate(operator.mul, e)

    def div_(self, e):
        """
        Lazy element-wise division with given scalar or sequence.
        """
        return self.__lazy_operate(operator.truediv, e)

    def pow_(self, e):
        """
        Raises elements of this Array to given power,
        or sequence of powers, element-wise.
        """
        return self.__lazy_operate(operator, e)

    def mod_(self, e):
        """
        Computes the remainder between elements in this Array
        and given scalar or sequence, element-wise.
        """
        return self.__lazy_operate(operator.mod, e)

    def bitwiseAnd_(self, e):
        """
        Computes the bit-wise AND between elements in this Array
        and given scalar or sequence, element-wise.
        """
        return self.__lazy_operate(operator.and_, e)

    def bitwiseOr_(self, e):
        """
        Computes the bit-wise OR between elements in this Array
        and given scalar or sequence, element-wise.
        """
        return self.__lazy_operate(operator.or_, e)

    def abs_(self):
        """ Element-wise absolute value. """
        return AFunc._map(abs, self)

    def floor_(self):
        """ Floors the Array elements. """
        return AFunc._map(math.floor, self)

    def ceil_(self):
        """ Ceils the Array elements. """
        return AFunc._map(math.ceil, self)

    def round_(self, d=0):
        """ Rounds the Array to the given number of decimals. """
        return AFunc._map(lambda e: round(e, d), self)

    def gt_(self, e):
        """ Computes x > y element-wise """
        return self.__lazy_operate(operator.gt, e)

    def ge_(self, e):
        """ Computes x >= y element-wise """
        return self.__lazy_operate(operator.ge, e)

    def lt_(self, e):
        """ Computes x < y element-wise """
        return self.__lazy_operate(operator.lt, e)

    def le_(self, e):
        """ Computes x <= y element-wise """
        return self.__lazy_operate(operator.le, e)

    def eq_(self, e):
        """ Computes x == y element-wise """
        return self.__lazy_operate(operator.eq, e)

    def ne_(self, e):
        """ Computes x != y element-wise """
        return self.__lazy_operate(operator.ne, e)

    def isfinite_(self):
        """
        Tests element-wise whether the elements are neither infinity nor NaN.
        """
        return Amap(math.isfinite, self)

    def astype_(self, t):
        """
        Converts the elements in this Array to given type.
        """
        return AFunc._map(t, self)

    def int_(self):
        """ Converts elements in this Array to integers. """
        try:
            return AFunc._map(lambda e: ord(e) if isinstance(e, str) else int(e), self)
        except TypeError:
            raise TypeError("Expected an Array of numbers or characters") from None

    def float_(self):
        return AFunc._map(float, self)

    def bool_(self):
        """ Converts elements in this Array to booleans. """
        return AFunc._map(bool, self)

    def char_(self):
        """ Converts an Array of integers to chars. """
        return AFunc._map(chr, self)

    def clip_(self, _min, _max):
        """
        Clip the values in the Array between the interval (`_min`, `_max`).
        """
        return AFunc._map(lambda e: max(min(e, _max), _min), self)

    def map_(self, l):
        """ Lazy map """
        return AFunc._map(l, self)

    def starmap_(self, l):
        """ Lazy starmap """
        return AFunc._map(lambda a: l(*a), self)

    def filter_(self, l):
        """ Lazy filter """
        return AFunc._filter(l, self)

    def takewhile_(self, l):
        """ Takes the longest prefix of elements that satisfy the given predicate. """
        return AFunc._iter(A.itertools.takewhile(l, self))

    def dropwhile_(self, l):
        """ Drops the longest prefix of elements that satisfy the given predicate. """
        return AFunc._iter(A.itertools.dropwhile(l, self))

    def groupby_(self, l):
        """
        Groups this Array into an Array of Array-tuples according
        to given discriminator function.
        """
        return AFunc._iter((e, A.Array(g)) for e, g in A.itertools.groupby(self, l))

    def zip_(self, *args):
        """ Lazy zip """
        return AFunc._zip(self, *args)

    def unzip_(self):
        """
        'Unzips' nested Arrays by unpacking its elements into a zip.

        >>> Array((1, "a"), (2, "b")).unzip()
        Array(Array(1, 2), Array('a', 'b'))
        """
        return AFunc._zip(*self)

    def zip_all_(self, *args, default=None):
        """
        Zips the sequences. If the iterables are
        of uneven length, missing values are filled with default value.
        """
        return AFunc._iter(A.itertools.zip_longest(self, *args, fillvalue=default))

    @property
    def head_(self):
        return next(self)

    def head_option_(self, default=None):
        return next(self, default)

    @property
    def enumerate_(self):
        """ Zips the Array with its indices """
        return AFunc._enum(self)

    def __lazy_operate(self, f, e):
        # TODO seq validation possible? or remove from both?
        # currently removed from both...
        if isinstance(e, A.Iterable):
            return AFunc._map(f, self, e)
        return AFunc._map(f, self, A.itertools.repeat(e))


class AFunc:
    __slots__ = []

    @staticmethod
    def _map(*args, **kwargs):
        return Amap(*args, **kwargs)

    @staticmethod
    def _filter(*args, **kwargs):
        return Afilter(*args, **kwargs)

    @staticmethod
    def _iter(*args, **kwargs):
        return Aiter(*args, **kwargs)

    @staticmethod
    def _range(*args, **kwargs):
        return Aiter(iter(range(*args, **kwargs)))

    @staticmethod
    def _enum(*args, **kwargs):
        return Aenum(*args, **kwargs)

    @staticmethod
    def _zip(*args, **kwargs):
        return Azip(*args, **kwargs)

    def result(self):
        return A.Array(self)


class Amap(ASeq, AFunc, map):
    __slots__ = []


class Afilter(ASeq, AFunc, filter):
    __slots__ = []


class Azip(ASeq, AFunc, zip):
    __slots__ = []


class Aenum(ASeq, AFunc, enumerate):
    __slots__ = []


class Aiter(ASeq, AFunc):
    __slots__ = '__val'

    def __init__(self, val):
        self.__val = val

    def __next__(self):
        return next(self.__val)

    def __iter__(self):
        return iter(self.__val)
