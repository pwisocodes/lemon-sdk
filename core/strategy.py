from abc import ABC, abstractmethod
from typing import List
import datetime
from datetime import timedelta
import time


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def do_algorithm(self, data: List):
        pass


class TradingStrategy(Strategy):

    def seconds_till_market_opens(self, entered_time):
        """
        Helper function with which we can determine how many more seconds need to pass until the stock market opens

        Args:
            entered_time ([type]): datetime.datetime.now()

        Returns:
            [type]: seconds
        """
        if entered_time.weekday() <= 4:
            d = (entered_time + timedelta(days=1)).date()
        else:
            days_till_market_opens = 0 - entered_time.weekday() + 7
            d = (entered_time + timedelta(days=days_till_market_opens)).date()
        # slightly later than actual market open time to avoid unstable market
        next_day = datetime.datetime.combine(d, datetime.time(10, 30))
        # number of seconds until market reopens
        seconds = (next_day - entered_time).total_seconds()
        return seconds  # we can then later combine this function with the time.sleep()-function to determine
        # how long we need to wait until our next execution

    def do_algorithm(self, account) -> None:
        """
        Trading Algorithm
        """
        print(account.total_balance)
        while True:
            market_open = False
            current_day_time = datetime.datetime.now()
            print()
            if current_day_time.weekday() <= 4:
                if current_day_time.hour in range(7, 24):
                    print('Market open, order creation possible')
                    market_open = True
                else:
                    print('Market currently not open, checking again soon')
                    market_open = False
                    seconds = self.seconds_till_market_opens(
                        datetime.datetime.now())
                    print(f"Market will open in {seconds} seconds.")
                    time.sleep(seconds)
            else:
                market_open = False
                seconds = self.seconds_till_market_opens(
                    datetime.datetime.now())
                print(
                    f"Market currently not open, will be open in {seconds} seconds. Sleeping for that time.")
                time.sleep(seconds)
