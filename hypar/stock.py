from dataclasses import dataclass, field
import datetime
from typing import List, Dict, Any


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
        ticker (str): Ticker symbol of the Stock.
        num_shares (int): Number of shares owned..
        start_date (datetime): Starting date; not necessarily
        end_date (datetime): Ending date of the StockSegment.
        anonymous (bool): True if the StockSegment is to be referred to by its
            pseudonym, and otherwise implies the StockSegment should be referred
            to by its ticker symbol.
        pseudonym (str): "S-XXX" where "XXX" is a pseudo-randomly generated
            integer between 100 and 999.
    """
    ticker: str = None
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None
    num_shares: int = 1
    anonymous: bool = field(default=False, repr=False)
    pseudonym: str = field(default=None, repr=False)

    def __post_init__(self):
        self.ticker = self.ticker.upper()

    def __repr__(self):
        return f'{self.__class__.__name__}(ticker={self.ticker}, ' \
            f'start={self.start_date:%Y-%m-%d}, end={self.end_date:%Y-%m-%d})'


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

    Attributes:
        ticker (str): Ticker symbol of the Stock.
        interday_pricing (List[Dict[str, Any]]): Daily adjusted and
        unadjusted price and volume information.
        balance_sheet (Dict[str, Any]): Balance sheet information of the most
            recent available quarter.
        book (Dict[str, Any]): Book data.
        cash_flow (Dict[str, Any]): Cash flow information of the most recent
            available quarter.
        company (Dict[str, Any]): Company information, such as the website,
            description, tags, and CEO.
        earnings (Dict[str, Any]): Earnings data for a given company,
            including the actual EPS, consensus, and fiscal period. Earnings are
            available for the most recent four quarters.
        estimate (Dict[str, Any]): Latest consensus estimate for the next
            fiscal period.
        income_statement (Dict[str, Any]): Income statement information from
            the most recent available quarter.
        intraday_pricing (Dict[str, Any]): Intraday trading information in
            one-minute intervals.
        ipo_today (Dict[str, List]): IPOs occurring today.
        ipo_upcoming (Dict[str, List]): IPOs in the near future.
        key_stats (Dict[str, Any]): Various summary data.
        price_target (Dict[str, Any]): Latest average, high, and low analyst
            price target.
    """
    ticker: str = None
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
        self.ticker = self.ticker.upper()


@dataclass(init=False)
class Stock(StockSegment):
    """A list of one or more StockSegment(s) that define the Stock.

    In the simplest case, a Stock is one StockSegment. But if the Stock is not
    held continuously over the duration of the Portfolio's time frame, more than
    one StockSegment comprises the Stock.

    Attributes:
        segments (List[StockSegment]): One or more StockSegments that contain
            uniform StockData. If there is only one continuous holding of a
            StockSegment, then the Stock and the single StockSegment are
            equivalent.
    """
    segments: List[StockSegment] = field(default_factory=list)

    def __init__(self, *args, **kwargs):
        self.segments = sorted(list(args), key=sort_by_start)
        if self.segments:
            self.ticker = self.segments[0].ticker
            self.start_date = self.segments[0].start_date
            self.end_date = sorted(self.segments, key=sort_by_end)[-1].end_date
        self.__dict__.update(kwargs)
        self.ticker.upper()

    def __repr__(self):
        return super().__repr__()

    #  TODO Make sure to update start/end dates of Stock
    def add_segment(self):
        pass

    def remove_segment(self):
        pass


def sort_by_start(segment):
    return segment.start_date


def sort_by_end(segment):
    return segment.end_date
