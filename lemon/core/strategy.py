from abc import ABC, abstractmethod
import logging
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
        return (next_day - entered_time).total_seconds() 
        
    def websocket(self):
        pass

    @abstractmethod
    def do_algorithm(self, data: List):
        pass


class TradingStrategy(Strategy):
    is_running: bool = False



    @property
    def running(self):
        return self.is_running

    @running.setter
    def cancel(self, b:bool = True):
        self.is_running = not b # Wenn 

    def do_algorithm(self) -> None:
        """
        Trading Algorithm
        """
        self.cancel = False
        while self.is_running:
            market_open = False
            current_day_time = datetime.datetime.now()
            if current_day_time.weekday() <= 4:
                if current_day_time.hour in range(7, 24):
                    logging.info('Market open, order creation possible')
                    market_open = True
                else:
                    logging.info('Market currently not open, checking again soon')
                    market_open = False
                    seconds = self.seconds_till_market_opens(
                        datetime.datetime.now())
                    logging.info(f"Market will open in {seconds} seconds.")
                    time.sleep(seconds)
            else:
                market_open = False
                seconds = self.seconds_till_market_opens(
                    datetime.datetime.now())
                logging.info(
                    f"Market currently not open, will be open in {seconds} seconds. Sleeping for that time.")
                time.sleep(seconds)
            time.sleep(5)
  