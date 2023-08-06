# lebesgue.py
# ported to python 3.*
# tests moved to test_lebesgue.py
# source file: algebre.tm
# license: MIT license (http://en.wikipedia.org/wiki/MIT_License)
# copyright (c) 2010 Gribouillis at www.daniweb.com

""" Module lebesgue
This module defines a class LebesgueSet which instances represent
finite unions of intervals of real numbers. Set operations on these
finite unions of intervals include intersection, union, set difference,
symmetric difference (xor), set complement.
Topological operations like testing wither a point is interior
or on the boundary, or adherent to the set are provided as well as
access to certain quantities, like the set's upper and lower bound
and the Lebesgue measure of the set.
Of course, the class is improperly named LebesgueSet because
a Lebesgue Set in mathematics is a wild set which can be much more
complicated than a finite union of intervals. However, conceptually,
it's best to consider that the intervals are nor opened nor closed,
and that an instance represents a union of intervals up to a set of
measure 0.
In this class, infinite values are represented by using the python value Float("infinity").
Infinite floats can be tested with math.isinf().
"""
import itertools
from bisect import bisect
import operator

class LebesgueSet(object):
    _inf = float('infinity')  # can be tested with math.isinf()
    _minf = -_inf
    UNION, INTER, XOR = range(3)

    def __init__(self, points, left_infinite=False, fast=False):
        """Create a new LebesgueSet object.
        @ points: a sequence of real numbers
        @ left_infinite : a boolean, True if the first interval is
                          semi-infinite ]-infinity, .[
        @ fast : can be set to True if the sequence of points is
                 already sorted and has no duplicates.
        """
        if not fast:
            points = sorted(set(points))
        self.points = list(points)
        self.left_infinite = bool(left_infinite)

    def intervals(self):
        start = 0
        p = self.points
        n = len(p)
        if self.left_infinite:
            if n:
                yield (self._minf, p[0])
                start = 1
            else:
                yield (self._minf, self._inf)
                return
        while start + 1 < n:
            yield (p[start], p[start + 1])
            start += 2
        if start < n:
            yield (p[start], self._inf)

    def __str__(self):
        return str(list(self.intervals()))

    def __bool__(self):
        return self.left_infinite or bool(self.points)

    def __eq__(self, other):
        return (self.left_infinite == other.left_infinite and
                self.points == other.points)

    def __contains__(self, x):
        """True if x is in one of the closed intervals defining self."""
        return self.status(x) >= 0

    def __invert__(self):
        """Compute the set's complement"""
        return LebesgueSet(self.points, not self.left_infinite, fast=True)

    def is_bounded(self):
        return not (self.left_infinite or (len(self.points) & 1))

    def lower_bound(self):
        if self.left_infinite:
            return self._minf
        elif not self.points:
            return self._inf
        else:
            return self.points[0]

    def upper_bound(self):
        if self.left_infinite ^ (len(self.points) & 1):
            return self._inf
        elif not self.points:
            return self._minf
        else:
            return self.points[-1]

    def zoom(self, center=0.0, factor=1.0):
        if factor == 0.0:
            points = ()
            left_infinite = False
        else:
            points = [center + factor * (x - center) for x in self.points]
            if factor > 0.0:
                left_infinite = self.left_infinite
            else:
                left_infinite = (self.upper_bound() == self._inf)
                points = reversed(points)
        return LebesgueSet(points, left_infinite, fast=True)

    def measure(self):
        """self.measure() -> a finite or infinite float.
        Compute the Lebesgue measure of the set self. If this
        measure is infinite, return float('infinity')."""
        if self.is_bounded():
            p = self.points
            return sum(p[i + 1] - p[i] for i in range(0, len(p) // 2, 2))
        else:
            return self._inf

    def status(self, x_real):
        """self.status(x) returns -1, 0, 1 depending on x being outside,
        on the boundary, or inside the set self (x is a real number)"""
        i = bisect(self.points, x_real)
        if (i > 0) and x_real == self.points[i - 1]:
            return 0
        return 1 if self.left_infinite ^ (i & 1) else -1

    def is_interior(self, x):
        """True if x is in the topological interior of the set self."""
        return self.status(x) == 1

    def is_exterior(self, x):
        """True if x is in the topological interior of the complement."""
        return self.status(x) == -1

    def is_boundary(self, x):
        """True if x is one end of one of the intervals"""
        return self.status(x) == 0

    def deltas(self, negated=False):
        infinite = self.left_infinite ^ (1 if negated else 0)
        assert infinite in (0, 1)
        for i, x in enumerate(self.points):
            yield (x, -1 if (infinite ^ (i & 1)) else 1)

    def __lshift__(self, offset):
        """This of it as a blue shift toward shorter wavelengths"""
        return self >> (-offset)

    def __rshift__(self, offset):
        """This of it as a red  shift toward longer wavelengths"""
        points = [point + offset for point in self.points]
        return LebesgueSet(points, left_infinite=self.left_infinite, fast=True)

    @classmethod
    def operate(cls, op, family):
        """Compute the union, intersection or xor of a family of sets.
        @ op : one of LebesgueSet.UNION or .INTER or .XOR
        @ family : a non empty sequence of LebesgueSet's.
        A real number x belongs to the xor of the family if it belongs
        to an odd number of members of the family.
        """
        family = tuple(family)
        value = sum(u.left_infinite for u in family)
        new_points = []
        if op == cls.XOR:
            left_infinite = bool(value & 1)
            old_points = sorted(itertools.chain(*(u.points for u in family)))
            for k, group in itertools.groupby(old_points):
                if len(tuple(group)) & 1:
                    new_points.append(k)
        else:
            inter = (op == cls.INTER)
            if inter:
                value = len(family) - value
            left_infinite = not value if inter else bool(value)
            old_points = sorted(itertools.chain(*(u.deltas(inter) for u in family)))
            for k, group in itertools.groupby(old_points, key=operator.itemgetter(0)):
                group = tuple(group)
                new_value = value + sum(delta[1] for delta in group)
                if not (value and new_value):
                    new_points.append(k)
                value = new_value
        return LebesgueSet(new_points, left_infinite, fast=True)

    def __and__(self, other):
        """self & other -> intersection of self and other."""
        return self.operate(self.INTER, (self, other))

    def __or__(self, other):
        """self | other, self + other -> union of self and other."""
        return self.operate(self.UNION, (self, other))

    __add__ = __or__

    def __xor__(self, other):
        """self ^ other -> symetric difference of self and other."""
        return self.operate(self.XOR, (self, other))

    def __sub__(self, other):
        """self - other -> set difference."""
        return self & ~other

    @classmethod
    def union(cls, family):
        """union of a family of Lebesgue sets."""
        return cls.operate(cls.UNION, family)

    @classmethod
    def inter(cls, family):
        """intersection of a family of Lebesgue sets"""
        return cls.operate(cls.INTER, family)

    @classmethod
    def xor(cls, family):
        """xor of a family of Lebesgue sets."""
        return cls.operate(cls.XOR, family)
