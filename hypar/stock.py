<<<<<<< HEAD
import bisect
from dataclasses import dataclass, field
import datetime
import numpy as np
from typing import List, Dict, Any, Union, Tuple


def sort_by_start(segment):
    return segment.start


def sort_by_end(segment):
    return segment.end


def first_start(segments: Union[List, Tuple]):
    if isinstance(segments, List):
        segments.sort(key=sort_by_start)
        return segments[0].start
    if isinstance(segments, Tuple):
        return sorted(segments, key=sort_by_start)[0].start


def last_end(segments: Union[List, Tuple]):
    if isinstance(segments, List):
        segments.sort(key=sort_by_end)
        return segments[-1].end
    if isinstance(segments, Tuple):
        return sorted(segments, key=sort_by_end)[-1].end

# TODO Need to fix -- doesn't work with removal
def update(existing_segments, new_segments: Union[List, Tuple]):
    segs = [s for s in new_segments if s not in existing_segments]
    updated_segments = existing_segments
    segs.sort()
    for s in segs:
        bisect.insort_left(updated_segments, s)
    if segs[0].start < existing_segments[0].start:
        start = segs[0].start
    else:
        start = existing_segments[0].start
    new_end = last_end(new_segments)
    current_end = last_end(existing_segments)
    if new_end > current_end:
        end = new_end
    else:
        end = current_end
    return updated_segments, start, end

# TODO Consider dict with str concatenated attributes as keys
@dataclass(order=True)
class StockSegment(object):
    """Usually a portion of an entire holding of a Stock, but could also be
    equivalent to the Stock itself if held continuously over the entire
    duration of the Stock's existence.

    Includes such properties as the number of shares owned and start and end
    dates of when the StockSegment is owned. Distinction of StockSegment(s) and
    StockData is necessary when dealing with a multi-Portfolio environment in
    which the number of shares and dates vary between one or more Portfolios.
    In this way, each StockSegment in one or more Portfolios can have
    different number of shares and dates.

    Attributes:
        sort_index (datetime.datetime): Used to compare by start date.
        _ticker (str): Ticker symbol of the Stock.
        num_shares (int): Number of shares owned..
        start (datetime.datetime): Starting date; not necessarily
        end (datetime.datetime): Ending date of the StockSegment.
        anonymous (bool): True if the StockSegment is to be referred to by its
            pseudonym, and otherwise implies the StockSegment should be referred
            to by its ticker symbol.
        pseudonym (str): "S-XXX" where "XXX" is a pseudo-randomly generated
            integer between 100 and 999. Used in place of the ticker when the
            StockSegment is supposed to be anonymous.
    """

    sort_index: datetime.datetime = field(init=False, repr=False)
    ticker: str
    start: datetime.datetime
    end: datetime.datetime
    num_shares: int = 1
    anonymous: bool = field(default=False, repr=False)
    pseudonym: str = field(init=False)

    def __post_init__(self):
        if self.start:
            self.sort_index = self.start
        else:
            self.sort_index = self.end
        if self.ticker:
            self.ticker = self.ticker.upper()
        self.pseudonym = self.generate_pseudonym()

    def __repr__(self):
        return f'{self.__class__.__name__}(ticker={self.ticker}, ' \
            f'pseudonym={self.pseudonym}, start={self.start:%Y-%m-%d}, ' \
            f'end={self.end:%Y-%m-%d})'

    @staticmethod
    def generate_pseudonym(append_x=False):
        num = np.random.randint(low=100, high=1000)
        if not append_x:
            return f'S-{num}'
        else:
            return f'S-{num}x'

# TODO(Ryan) Specify type hints in more detail -- refer to PEP 483 and 484:
# https://www.python.org/dev/peps/pep-0483/#notational-conventions
# https://www.python.org/dev/peps/pep-0484/
@dataclass
class StockData(object):
    """Data about a Stock that is shared among all StockSegment(s) of a Stock.

    Collection of data that is parsed among all StockSegment(s) that, together,
    signifies the Stock activity during the date ranges in which it is owned.
    There may be regions of data that are not accessed if no StockSegment
    exists within that region of time.
=======
import datetime


class Stock:
    # TODO Complete Attributes
    """A member unit of a Portfolio that contains numerous data attributes.
>>>>>>> 6f35e43c5e68e292d93c56847790b15dbbedc0b9

    Attributes:
        ticker (str): Symbol that represents the Stock entity.
        portfolios (list[Portfolio]): One or more Portfolios of which the Stock
            is a member. The list contains all portfolios to which the stock
            belongs.
        num_shares (dict[Portfolio, int]): Number of shares owned in each
            Portfolio. Each key is a Portfolio and the value is number of
            shares.
        start_date (dict[Portfolio, datetime]): Earliest data entry of the Stock
            in each Portfolio. Each key is a Portfolio and each value is the
            start date.
        end_date (dict[Portfolio, datetime]): Most recent data entry of the
            Stock in each Portfolio. Each key is a Portfolio and each value is
            the end date.
        price_data (dict):
        balance_sheet (dict):
        book_data (dict):
        cash_flow (dict):
        company_data (dict):
        earnings (dict):
        income_statement (dict):
        intraday_data (dict):
        key_stats (dict):
        price_target (dict):
        anonymous (dict[Portfolio, list[bool, str]): Each key is Portfolio and
            each value is a list pair: if index 0 is True, the Stock is
            "anonymous" and the pseudonym in index 1 string is displayed;
            otherwise, the real ticker is displayed. Pseudonym format is 'S-xxx'
            where 'xxx' is a randomly generated integer between 0-999.
    """
<<<<<<< HEAD
    ticker: str
    interday_pricing: List[Dict[str, Any]] = field(default_factory=list)
    balance_sheet: Dict[str, Any] = field(default_factory=dict)
    book: Dict[str, float] = field(default_factory=dict)
    cash_flow: Dict[str, Any] = field(default_factory=dict)
    company: Dict[str, Any] = field(default_factory=dict)
    earnings: Dict[str, Any] = field(default_factory=dict)
    estimate: Dict[str, Any] = field(default_factory=dict)  # NEW (7/5/19)
    income_statement: Dict[str, Any] = field(default_factory=dict)
    intraday_pricing: List[Dict[str, Any]] = field(default_factory=list)
    ipo_today: Dict[str, List] = field(default_factory=dict)  # NEW (7/5/19)
    ipo_upcoming: Dict[str, List] = field(default_factory=dict)  # NEW (7/5/19)
    key_stats: Dict[str, Any] = field(default_factory=dict)
    price_target: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.ticker:
            self.ticker = self.ticker.upper()


@dataclass(init=False, order=True)
class Stock(StockSegment):
    """A list of one or more StockSegment(s) that define the Stock.

    In the simplest case, a Stock is one StockSegment. But if the Stock is not
    held continuously over the duration of the Portfolio's time frame, more than
    one StockSegment comprises the Stock.

    Attributes:
        segments (List[StockSegment]): One or more StockSegments that contain
            uniform StockData. If there is only one continuous holding of a
            StockSegment, then the Stock and the single StockSegment are
            equivalent. StockSegments are to remain sorted by start date.
    """
    segments: List[StockSegment] = field(default_factory=list)

    def __init__(self, *args, **kwargs):
        """Creates a Stock from one or more StockSegments.

        Arguments:
            *args: One or more StockSegments.
            **kwargs: Any attribute that is intended to describe a Stock.
        """
        self.segments = sorted(list(args))
        self.ticker = self.segments[0].ticker
        # Set the start date to be the earliest start date.
        self.start = first_start(self.segments)
        # Set the end date to be the latest end date.
        self.end = last_end(self.segments)
        if len(self.segments) > 1:
            self.pseudonym = self.generate_pseudonym(append_x=True)
        else:
            self.pseudonym = self.segments[0].pseudonym
        self.__dict__.update(kwargs)

    def __repr__(self):
        return super().__repr__()

    def add_segment(self, *segments: StockSegment):
        """Add one or more StockSegments to an existing Stock. Begin by
        checking that all StockSegments to be added do not already exist.
        After adding all StockSegments, update the start and end dates if any of
        the new StockSegments have an earlier start date or later end date
        than the existing start and end date of the Stock.

        Arguments:
            *segments: One or more StockSegments to be added to the Stock.
        """
        segs = [s for s in segments if s not in self.segments]
        segs.sort()
        for s in segs:
            bisect.insort_left(self.segments, s)
        self.segments, self.start, self.end = update(self.segments, segments)

    def remove_segment(self, *segments):
        """Remove one or more StockSegments from the Stock. First checks that
        any StockSegment to be removed exists in the Stock.

        Arguments:
            *segments: One or more StockSegments to remove.
        """
        for s in segments:
            if s in self.segments:
                self.segments.remove(s)
=======

    def __init__(self, ticker, portfolios=None, num_shares=None,
                 start_date=None, end_date=None, price_data=None,
                 balance_sheet=None, book_data=None, cash_flow=None,
                 company_data=None, earnings=None, income_statement=None,
                 intraday_data=None, key_stats=None, price_target=None,
                 anonymous=None):
        """Instantiates a Stock with any associated data."""
        self.ticker = str.upper(ticker)
        # TODO Make this a set?
        self.portfolios = portfolios
        self.num_shares = num_shares
        self.start_date = start_date
        self.end_date = end_date
        self.price_data = price_data
        self.balance_sheet = balance_sheet
        self.book_data = book_data
        self.cash_flow = cash_flow
        self.company_data = company_data
        self.earnings = earnings
        self.income_statement = income_statement
        self.intraday_data = intraday_data
        self.key_stats = key_stats
        self.price_target = price_target
        self.anonymous = anonymous
        self.handle_container_status('portfolios', container_type=list)
        self.handle_container_status('num_shares',
                                     'start_date',
                                     'end_date',
                                     'anonymous',
                                     container_type=dict)

    def handle_container_status(self, *attributes, container_type=list):
        for a in attributes:
            if getattr(self, a) is None:
                setattr(self, a, container_type())
            else:
                setattr(self, a, a)
>>>>>>> 6f35e43c5e68e292d93c56847790b15dbbedc0b9
