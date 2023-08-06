from .scan.scan_iterator import ITERATION_MODE_GROUPED, ITERATION_MODE_SINGLE
from .scan.loader import ScanIterator


class ScanIteratorProxyBase(object):
    """A wrapper around a :class:`~.RandomAccessScanSource` that alters its behavior
    in some way, either limiting the range it iterates over, or filtering the items
    it would yield.

    This is an abstract base class. It should be extended to be used.

    This class re-uses the same file handle that as :attr:`scan_source`, and should
    not be used interleaved with the original source.

    Attributes
    ----------
    scan_source: :class:`~.RandomAccessScanSource`
        The object to use to load :class:`~.Scan` and :class:`~.ScanBunch` instances.
    iteration_mode: str
        A string denoting :const:`~.ITERATION_MODE_GROUPED` or :const:`~.ITERATION_MODE_SINGLE`
        that controls whether :class:`~.ScanBunch` or :class:`~.Scan` are produced
        by iteration.
    """

    def __init__(self, scan_source, *args, **kwargs):
        self.scan_source = scan_source

    @property
    def iteration_mode(self):
        '''A string denoting :const:`~.ITERATION_MODE_GROUPED` or :const:`~.ITERATION_MODE_SINGLE`
        that controls whether :class:`~.ScanBunch` or :class:`~.Scan` are produced
        by iteration.

        Returns
        -------
        str
        '''
        return self.scan_source.iteration_mode

    def has_ms1_scans(self):
        '''Checks if this :class:`ScanDataSource` contains MS1 spectra.

        Returns
        -------
        :class:`bool` or :const:`None`
            Returns a boolean value if the presence of MS1 scans is known for certain, or :const:`None`
            if it cannot be determined in the case of missing metadata.
        '''
        return self.scan_source.has_ms1_scans()

    def has_msn_scans(self):
        '''Checks if this :class:`ScanDataSource` contains MSn spectra.

        Returns
        -------
        :class:`bool` or :const:`None`
            Returns a boolean value if the presence of MSn scans is known for certain, or :const:`None`
            if it cannot be determined in the case of missing metadata.
        '''
        return self.scan_source.has_msn_scans()

    def next(self):
        '''Advance the iterator, fetching the next :class:`~.ScanBunch` or :class:`~.ScanBase`
        depending upon iteration strategy.

        Returns
        -------
        :class:`~.ScanBunch` or :class:`~.ScanBase`
        '''
        raise NotImplementedError()

    def __next__(self):
        '''Advance the iterator, fetching the next :class:`~.ScanBunch` or :class:`~.ScanBase`
        depending upon iteration strategy.

        Returns
        -------
        :class:`~.ScanBunch` or :class:`~.ScanBase`
        '''
        return self.next()

    def __iter__(self):
        return self


ScanIterator.register(ScanIteratorProxyBase)


class QueryIteratorBase(ScanIteratorProxyBase):
    """A base class for types which iterate over a subset of a :class:`~.RandomAccessScanSource`.

    Attributes
    ----------
    grouped: bool
        Whether or not to produce grouped or single scans.

    """
    def __init__(self, scan_source, grouped=True, *args, **kwargs):
        super(QueryIteratorBase, self).__init__(scan_source, *args, **kwargs)
        self.grouped = grouped

    @property
    def iteration_mode(self):
        if self.grouped:
            return ITERATION_MODE_GROUPED
        else:
            return ITERATION_MODE_SINGLE

    def make_iterator(self, iterator=None, grouped=False):
        """Configure the :class:`ScanIterator`'s behavior, selecting it's iteration strategy over
        either its default iterator or the provided ``iterator`` argument.

        Parameters
        ----------
        iterator : Iterator, optional
            Unused. Included for compatibility with :class:`ScanIterator` API
        grouped : bool, optional
            Whether the iterator should be grouped and produce :class:`.ScanBunch` objects
            or single :class:`.Scan`. If :const:`None` is passed, :meth:`has_ms1_scans` will be
            be used instead. Defaults to :const:`None`.
        """
        self.grouped = grouped
        self._make_iterator(grouped=grouped)

    def _make_iterator(self, grouped=False):
        self.scan_source.reset()
        self.scan_source.make_iterator()

    def reset(self):
        '''Reset the iterator, if possible, and clear any caches.

        Resets the underlying :class:`~.RandomAccessScanSource`
        '''
        self.scan_source.reset()
        self.make_iterator(grouped=self.grouped)


class TimeIntervalIterator(QueryIteratorBase):
    """Query over a retention time interval.

    Attributes
    ----------
    start: float
        The time to start the query iterator from
    end: float
        The time to end the query iterator at

    """
    def __init__(self, scan_source, start=None, end=None, grouped=True, *args, **kwargs):
        super(TimeIntervalIterator, self).__init__(
            scan_source, grouped, * args, **kwargs)
        self.start = start
        self.end = end
        self._update_bounds()
        self.make_iterator(grouped=grouped)

    def _update_bounds(self):
        if self.start is None:
            try:
                first_entry = self.scan_source[0]
                self.start = first_entry.scan_time
            except (AttributeError, TypeError):
                self.start = 0
        if self.end is None:
            try:
                last_entry = self.scan_source[-1]
                self.end = last_entry.scan_time
            except (AttributeError, TypeError):
                self.end = float('inf')

    def _make_iterator(self, grouped=False):
        self.scan_source.start_from_scan(rt=self.start, grouped=self.grouped)

    def next(self):
        result = next(self.scan_source)
        if self.grouped:
            if result.precursor.scan_time > self.end:
                raise StopIteration()
            return result
        else:
            if result.scan_time > self.end:
                raise StopIteration()
            return result


class IndexIntervalIterator(QueryIteratorBase):
    """Query over a scan index interval.

    Attributes
    ----------
    start: int
        The index to start the query iterator from
    end: int
        The index to end the query iterator at

    """

    def __init__(self, scan_source, start=None, end=None, grouped=True, *args, **kwargs):
        super(IndexIntervalIterator, self).__init__(
            scan_source, grouped, * args, **kwargs)
        self.start = start
        self.end = end
        self._update_bounds()
        self.make_iterator(grouped=grouped)

    def _update_bounds(self):
        if self.start is None:
            try:
                first_entry = self.scan_source[0]
                self.start = first_entry.index
            except (AttributeError, TypeError):
                self.start = 0
        if self.end is None:
            try:
                last_entry = self.scan_source[-1]
                self.end = last_entry.index
            except (AttributeError, TypeError):
                self.end = float('inf')

    def _make_iterator(self, grouped=False):
        self.scan_source.start_from_scan(index=self.start, grouped=self.grouped)

    def next(self):
        result = next(self.scan_source)
        if self.grouped:
            if result.precursor.index > self.end:
                raise StopIteration()
            return result
        else:
            if result.index > self.end:
                raise StopIteration()
            return result


def scan_range(scan_source, time=None, index=None, grouped=True, *args, **kwargs):
    """Create an iterator proxy over `scan_source` spanning a specified range in time
    or index.

    If neither `time` nor `index` is provided, `scan_source` is returned unchanged.
    If both are provided, an error is thrown.

    Parameters
    ----------
    scan_source : :class:`~.RandomAccessScanSource`
        The scan source to iterate over
    time : tuple[float, float], optional
        The start and stop times to use
    index : tuple[int, int], optional
        The start and top scan indices to use
    grouped : bool, optional
        Whether or not to create a :class:`~.ScanBunch` iterator or a :class:`~.Scan` iterator
    *args:
    **kwargs:
        Forwarded to the iterator proxy.

    Returns
    -------
    :class:`ScanIterator`

    Raises
    ------
    ValueError:
        If both `time` and `index` are provided.
    """
    if time and index:
        raise ValueError("Only one of time and index intervals may be specified")
    if time:
        return TimeIntervalIterator(
            scan_source, time[0], time[1], grouped=grouped, *args, **kwargs)
    elif index:
        return IndexIntervalIterator(
            scan_source, index[0], index[1], grouped=grouped, *args, **kwargs)
    else:
        return scan_source


class ScanIteratorFilterBase(ScanIteratorProxyBase):
    """A base class for types which filter or transform scans produced
    by a :class:`~.ScanIterator` or :class:`~.RandomAccessScanSource`.

    """
    def __init__(self, scan_source, *args, **kwargs):
        super(ScanIteratorFilterBase, self).__init__(scan_source, *args, **kwargs)
        self._generator = None

    def filter_scan_bunch(self, scan_group, **kwargs):
        """Filter a scan bunch

        Parameters
        ----------
        scan : :class:`~.ScanBunch`
            The scan bunch to filter

        Yields
        ------
        :class:`~.ScanBunch`
        """
        raise NotImplementedError()

    def filter_scan(self, scan, **kwargs):
        """Filter a single scan

        Parameters
        ----------
        scan : :class:`~.Scan`
            The single scan to filter

        Yields
        ------
        :class:`~.Scan`
        """
        raise NotImplementedError()

    def filter(self, result, **kwargs):
        """Filter scans, producing only those that passed the criteria.

        This returns a generator which yields the same type as `result`

        This method will dispatch to :meth:`filter_scan` or :meth:`filter_scan_bunch`,
        whichever is appropriate for `result`

        Parameters
        ----------
        result : :class:`~.Scan` or :class:`~.ScanBunch`
            The scan or bunch to filter.

        Yields
        ------
        :class:`~.Scan` or :class:`~.ScanBunch`
        """
        if self.scan_source.iteration_mode == ITERATION_MODE_GROUPED:
            return self.filter_scan_bunch(result, **kwargs)
        else:
            return self.filter_scan(result, **kwargs)

    def _generate(self):
        for batch in self.scan_source:
            for result in self.filter(batch):
                yield result

    def next(self):
        if self._generator is None:
            self._generator = self._generate()
        return next(self._generator)


class _PredicateFilterIterator(ScanIteratorFilterBase):
    def _check(self, scan):
        raise NotImplementedError()

    def filter_scan_bunch(self, scan_group, **kwargs):
        if scan_group.products:
            yield scan_group.__class__(
                scan_group.precursor if self._check(
                    scan_group.precursor) else None,
                [scan for scan in scan_group.products if self._check(scan)])

    def filter_scan(self, scan, **kwargs):
        if self._check(scan):
            yield scan


class PolarityFilter(_PredicateFilterIterator):
    """A Scan Iterator that filters out scans with a polarity
    which do not match :attr:`polarity`

    Attributes
    ----------
    polarity: int
        The polarity to match

    """

    def __init__(self, scan_source, polarity, *args, **kwargs):
        super(PolarityFilter, self).__init__(scan_source, *args, **kwargs)
        self.polarity = polarity

    def _check(self, scan):
        return scan.polarity == self.polarity


class MSLevelFilter(_PredicateFilterIterator):
    """A Scan Iterator that filters out scans with MS levels
    which do not match :attr:`ms_level`

    Attributes
    ----------
    ms_level: int
        The MS level to require matching

    """
    def __init__(self, scan_source, ms_level, *args, **kwargs):
        super(MSLevelFilter, self).__init__(scan_source, *args, **kwargs)
        self.ms_level = ms_level

    def _check(self, scan):
        return scan.ms_level == self.ms_level


class MassAnalyzerFilter(_PredicateFilterIterator):
    """A Scan Iterator that filters out scans which were not performed using
    :attr:`mass_analyzer`

    Attributes
    ----------
    mass_analyzer: :class:`~.Component`
        The mass analyzer to match
    """
    def __init__(self, scan_source, mass_analyzer, *args, **kwargs):
        super(MassAnalyzerFilter, self).__init__(scan_source, *args, **kwargs)
        from .metadata.instrument_components import analyzer_types, Component
        if not isinstance(mass_analyzer, Component):
            mass_analyzer = analyzer_types[mass_analyzer]
        self.mass_analyzer = mass_analyzer

    def _check(self, scan):
        ic = scan.instrument_configuration
        if ic is None:
            return False
        for analyzer in ic.analyzers:
            if analyzer.is_a(self.mass_analyzer):
                return True
        return False


class CallableFilter(_PredicateFilterIterator):
    """A Scan Iterator that filters out scans which do not pass
    a user-provided callable

    Attributes
    ----------
    filter_fn: :class:`Callable`
        The callable object to use to test if a scan should be used
    """

    def __init__(self, scan_source, filter_fn, *args, **kwargs):
        super(CallableFilter, self).__init__(scan_source, *args, **kwargs)
        self.filter_fn = filter_fn

    def _check(self, scan):
        return self.filter_fn(scan)


filter_scans = CallableFilter
