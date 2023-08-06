from cpython.list cimport PyList_GetItem, PyList_Size
from cpython.tuple cimport PyTuple_GetItem

from collections import deque


cdef class SpanningMixin(object):
    """Provides methods for checking whether an entity
    which has a defined start and end point over a single
    dimension contains or overlaps with another entity in
    that same dimension.
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, i):
        """Tests for point inclusion, `start <= i <= end`

        Parameters
        ----------
        i : Number
            The point to be tested

        Returns
        -------
        bool
        """
        return self._contains(i)

    cdef bint _contains(self, double i):
        """Tests for point inclusion, `start <= i <= end`

        Parameters
        ----------
        i : double
            The point to be tested

        Returns
        -------
        bool
        """
        return self.start <= i <= self.end

    cpdef bint contains(self, double i):
        """Tests for point inclusion, `start <= i <= end`

        Parameters
        ----------
        i : double
            The point to be tested

        Returns
        -------
        bool
        """
        return self._contains(i)

    cpdef bint overlaps(self, SpanningMixin interval):
        """Tests whether another spanning entity with
        a defined start and end point overlaps with
        this spanning entity

        Parameters
        ----------
        interval : SpanningMixin

        Returns
        -------
        bool
        """
        cdef bint cond
        cond = ((self.start <= interval.start and self.end >= interval.start) or (
            self.start >= interval.start and self.end <= interval.end) or (
            self.start >= interval.start and self.end >= interval.end and self.start <= interval.end) or (
            self.start <= interval.start and self.end >= interval.start) or (
            self.start <= interval.end and self.end >= interval.end))
        return cond

    cpdef double overlap_size(self, SpanningMixin interval):
        if self.start <= interval.start <= self.end and self.start <= interval.end <= self.end:
            return interval.end - interval.start
        elif interval.start <= self.start <= interval.end and interval.start <= self.end <= interval.end:
            return self.end - self.start
        if self.end >= interval.start:
            return self.end - interval.start
        elif self.start >= interval.end:
            return self.start - interval.end

    cpdef bint is_contained_in_interval(self, SpanningMixin interval):
        """Tests whether this spanning entity is
        completely contained inside the other entity

        Parameters
        ----------
        interval : SpanningMixin

        Returns
        -------
        bool
        """
        return self.start >= interval.start and self.end <= interval.end

    cpdef bint contains_interval(self, SpanningMixin interval):
        """Tests whether the other spanning entity is
        completely contained inside this entity

        Parameters
        ----------
        interval : SpanningMixin

        Returns
        -------
        bool
        """
        return self.start <= interval.start and self.end >= interval.end


cdef class SimpleInterval(SpanningMixin):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    cdef SimpleInterval _create(double start, double end):
        cdef SimpleInterval self = SimpleInterval.__new__(SimpleInterval)
        self.start = start
        self.end = end
        return self


cdef class Interval(SpanningMixin):
    def __init__(self, start, end, members=None, **kwargs):
        if members is None:
            members = []
        self.start = start
        self.end = end
        self.members = members
        self.data = kwargs

    def __repr__(self):
        return "%s(start=%r, end=%r, data=%r)" % (self.__class__.__name__, self.start, self.end, self.data)

    def __getitem__(self, k):
        return self.members[k]

    def __len__(self):
        return len(self.members)

    def __iter__(self):
        return iter(self.members)


cpdef list intervals_containing_point(list intervals, double x):
    cdef:
        size_t i
        SpanningMixin interval
        list result
    result = []
    for i in range(PyList_Size(intervals)):
        interval = <SpanningMixin>PyList_GetItem(intervals, i)
        if interval.start <= x <= interval.end:
            result.append(interval)
    return result


cdef double INF = float('inf')


cdef class IntervalTreeNode(object):

    def __init__(self, double center, IntervalTreeNode left, list contained, IntervalTreeNode right,
                 int level=0, IntervalTreeNode parent=None):
        cdef:
            double start, end, i_start, i_end
            size_t i

        self.center = center
        self.left = left
        self.contained = contained
        self.right = right
        self.level = level
        self.parent = parent

        start = INF
        end = -INF
        i = 0

        for interval in self.contained:
            i += 1
            i_start = interval.start
            if i_start < start:
                start = i_start
            i_end = interval.end
            if i_end > end:
                end = i_end

        if i > 0:
            self.start = start
            self.end = end
        else:
            self.start = self.end = center

    cpdef list contains_point(self, double x):
        cdef:
            list inner
        inner = intervals_containing_point(self.contained, x)
        if self.left is not None and self.left.start <= x <= self.left.end:
            inner.extend(self.left.contains_point(x))
            return inner
        if self.right is not None and self.right.start <= x <= self.right.end:
            inner.extend(self.right.contains_point(x))
            return inner
        else:
            return inner

    cpdef list _overlaps_interval(self, double start, double end):
        cdef:
            SpanningMixin interv
            SimpleInterval query
            size_t i
        query = SimpleInterval._create(start, end)
        result = []
        for i in range(PyList_Size(self.contained)):
            interv = <SpanningMixin>PyList_GetItem(self.contained, i)
            if query.overlaps(interv):
                result.append(interv)
        return result

    cpdef list overlaps(self, double start, double end):
        """Returns the list of all contained intervals which
        overlap with the interval described by `start` and `end`

        Parameters
        ----------
        start : float
            The start of the query interval
        end : float
            The end of the query interval

        Returns
        -------
        list
            A list of all objects which overlap the argument interval
            from all spanning nodes' `contained` list.
        """
        cdef list result = []
        if start > self.end:
            return result
        if end < self.start:
            return result
        elif start <= self.start:
            if end < self.start:
                return result
            else:
                if self.left is not None:
                    result.extend(self.left.overlaps(start, end))
                result.extend(self._overlaps_interval(start, end))
                if self.right is not None and end >= self.right.start:
                    result.extend(self.right.overlaps(start, end))
        elif start > self.start:
            if self.left is not None and self.left.end >= start:
                result.extend(self.left.overlaps(start, end))
            result.extend(self._overlaps_interval(start, end))
            if self.right is not None and end >= self.right.start:
                result.extend(self.right.overlaps(start, end))
        elif end > self.start:
            if self.left is not None:
                result.extend(self.left.overlaps(start, end))
            result.extend(self._overlaps_interval(start, end))
            if self.right is not None and end >= self.right.start:
                result.extend(self.right.overlaps(start, end))
        return result

    def __repr__(self):
        return "IntervalTreeNode(level=%d, center=%0.4f, start=%0.4f, end=%0.4f)" % (
            self.level, self.center, self.start, self.end)

    def __richcmp__(self, other, int code):
        if code == 2:
            return self._eq(other)
        elif code == 3:
            return not (self._eq(other))

    cpdef bint _eq(self, IntervalTreeNode other):
        if other is None:
            return False
        else:
            result = self.contained == other.contained
            if result:
                result = self.left == other.left
                if result:
                    result = self.right == other.right
            return result

    def __hash__(self):
        return hash((self.start, self.center, self.right, self.level))

    def __diagnostic_eq__(self, other):
        if other is None:
            return False
        else:
            result = self.contained == other.contained
            if result:
                try:
                    result = self.left.__diagnostic_eq__(other.left)
                except AttributeError:
                    result = self.left == other.left
                if result:
                    try:
                        result = self.right.__diagnostic_eq__(other.right)
                    except AttributeError:
                        result = self.right == other.right
                    if not result:
                        print self.right, "r!=", other.right
                else:
                    print self.left, "l!=", other.left
            else:
                print self, "!=", other
            return result

    @classmethod
    def build(cls, intervals):
        cdef:
            IntervalTreeNode root, parent, node, up
            list stack, members, left, right, contained, intervals_
            tuple bunch
            str side
            double center, point, accumulator
            SpanningMixin i
            size_t j, n
        stack = []
        root = cls(0, None, [], None, -1)

        intervals_ = list(intervals)
        if not intervals_:
            return root
        stack.append((root, intervals_, "left"))

        while stack:
            # parent, members, side = stack.pop()
            bunch = <tuple>stack.pop()
            parent = <IntervalTreeNode>PyTuple_GetItem(bunch, 0)
            members = <list>PyTuple_GetItem(bunch, 1)
            side = <str>PyTuple_GetItem(bunch, 2)
            n = PyList_Size(members)
            if n > 0:
                accumulator = 0.
                j = 0
                for j in range(n):
                    i = <SpanningMixin>PyList_GetItem(members, j)
                    accumulator += (i.start + i.end) / 2.
                if j > 0:
                    center = accumulator / (j + 1)
                else:
                    center = 0.0

                left = []
                right = []
                contained = []

                if n > 20:
                    j = 0
                    for j in range(n):
                        i = <SpanningMixin>PyList_GetItem(members, j)
                        if abs(i.start - center) < 1e-6 and abs(i.end - center) < 1e-6:
                            contained.append(i)
                        elif center > i.end:
                            left.append(i)
                        elif center < i.start:
                            right.append(i)
                        else:
                            contained.append(i)
                else:
                    contained = list(members)
                node = cls(center, left=None, contained=contained, right=None, level=parent.level + 1, parent=parent)
                if side == 'left':
                    parent.left = node
                    parent.start = min(node.start, parent.start)
                    up = parent.parent
                    while up is not None:
                        if up.start > node.start:
                            up.start = node.start
                        up = up.parent
                elif side == 'right':
                    parent.right = node
                    parent.end = max(node.end, parent.end)
                    up = parent.parent
                    while up is not None:
                        if up.end < node.end:
                            up.end = node.end
                        up = up.parent
                else:
                    raise ValueError(side)
                stack.append((node, left, "left"))
                stack.append((node, right, "right"))
        return root.left

    def _update_bounds(self):
        changed = False
        if self.left is not None and self.left.start < self.start:
            changed = True
            self.start = self.left.start
        if self.right is not None and self.right.end > self.end:
            changed = True
            self.end = self.right.end
        if self.parent is not None:
            self.parent._update_bounds()
        return changed

    def insert(self, interval):
        insert_in_self = False
        if self.node_contains(interval.start):
            if self.left is not None and self.left.node_contains(interval.end):
                return self.left.insert(interval)
            elif (self.right is not None and self.right.node_contains(interval.end) and
                  self.right.node_contains(interval.start)):
                return self.right.insert(interval)
            else:
                insert_in_self = True
        elif self.node_contains(interval.end):
            if self.right is not None and self.right.node_contains(interval.start):
                return self.right.insert(interval)
            else:
                insert_in_self = True
        if not insert_in_self and self.parent is None:
            insert_in_self = True
        if insert_in_self:
            self.contained.append(interval)
            changed = False
            if interval.start < self.start:
                self.start = interval.start
                changed = True
            if interval.end > self.end:
                self.end = interval.end
                changed = True
            if changed:
                self._update_bounds()

    def flatten(self):
        # perform an infix traversal of the tree and collect
        # the elements
        items = []
        stack = deque([])
        current = self
        done = False
        while not done:
            if current is not None:
                stack.append(current)
                current = current.left
            else:
                if stack:
                    current = stack.pop()
                    items.extend(current.contained)
                    current = current.right
                else:
                    done = True
        return items

    def balance(self):
        items = self.flatten()
        tree = self.build(items)
        self.left = tree.left
        self.right = tree.right
        self.contained = tree.contained
        self.start = tree.start
        self.end = tree.end
        self.center = tree.center
        self.left.parent = self
        self.right.parent = self
        self._update_bounds()

    def __iter__(self):
        flat = self.flatten()
        return iter(flat)