# import datetime
import logging
# from datetime import datetime
from typing import Tuple, Union
import requests
from datetime import datetime


class FinViz():

    ticker_list = ["EURUSD", "GBPUSD", "USDJPY", "USDCAD", "USDCHF", "AUDUSD", "NZDUSD", "EURGBP", "GBPJPY", "BTCUSD"]
    time_frame_list = ["i1", "i3", "i5", "h", "d", "w", "m"]
    types = ["forex", "stock"]

    def __init__(self, timeout: int = 10, type: str = "stock") -> None:
        """FinViz class to interact with the finviz website

        Args:
            timeout (int, optional): Specifies the timeout to server in seconds. Defaults to 10.
            type (str, optional): Specifies either 'forex' or 'stock'. Defaults to forex.
        """
        if type not in self.types:
            raise Exception("Incorrect type selected. Please choose from:", self.types)

        self.URL = f"https://elite.finviz.com/api/quote.ashx?instrument={type}"
        self.type = type
        self._logger = logging.getLogger(__name__)
        self._timeout = timeout
        self._time: int = -1
        self._volume: int = -1
        self._price: float = -1.0

    def get_data(self, time_frame: str = "i1", ticker: str = "EURUSD") -> Tuple[int, int, float]:
        """Get the volume in the last specified time frame

        Args:
            time_frame (str): Choose from time_frame_list:
            ticker (str): Ticker chosen from ticker list e.g.: EURUSD

        Raises:
            Exception: If incorrect timeframe specified
            Exception: If incorrect ticker specified
            Exception: No/Error response from server

        Returns:
            int: time in POSIX format
            int: volume
            float: price
        """
        if time_frame not in self.time_frame_list:
            raise Exception("Incorrect time frame specified, please choose from the list", FinViz.time_frame_list)

        if ticker not in self.ticker_list and self.type == "forex":
            raise Exception("Incorrect ticker specified, please choose from the list", FinViz.ticker_list)

        payload = {"ticker": ticker, "timeframe": time_frame, "type": "new"}

        # Headers required to show that it is an actual computer
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        response = requests.get(self.URL, params=payload, timeout=self._timeout, headers=headers)

        if response.status_code != 200:
            raise Exception("No response from server")

        json_response = response.json()
        

        return json_response
    

    
    def get_all_data(self, time_frame: str = "i1", ticker: str = "EURUSD"):

        """Get the volume in the last specified time frame

        Args:
            time_frame (str): Choose from time_frame_list:
            ticker (str): Ticker chosen from ticker list e.g.: EURUSD

        Raises:
            Exception: If incorrect timeframe specified
            Exception: If incorrect ticker specified
            Exception: No/Error response from server

        Returns:
            int: time in POSIX format
            int: volume
            float: price
        """
        if time_frame not in self.time_frame_list:
            raise Exception("Incorrect time frame specified, please choose from the list", FinViz.time_frame_list)

        # if ticker not in self.ticker_list:
        #     raise Exception("Incorrect ticker specified, please choose from the list", FinViz.ticker_list)

        payload = {"ticker": ticker, "timeframe": time_frame, "type": "new"}

        # Headers required to show that it is an actual computer
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        response = requests.get(self.URL, params=payload, timeout=self._timeout, headers=headers)

        if response.status_code != 200:
            print(f'asset type: {self.asset_type}')
            raise Exception("No response from server")

        json_response = response.json()
        
        all_volumes = [float(i) for i in json_response["volume"]]
        all_opens = [float(i) for i in json_response["open"]]
        all_closes = [float(i) for i in json_response["close"]]
        all_dates = [float(i) for i in json_response["date"]]

        # get the current time 
        current_time = datetime.now()
        # get the UTC time
        utc_time = datetime.utcnow()
        # find out if we should add or subtract the time difference and whether should add the to the UTC or subtract the time difference
        if current_time > utc_time:
            time_difference = current_time - utc_time
            for date in range(len(all_dates)):
                all_dates[date] = datetime.utcfromtimestamp(all_dates[date]) + time_difference
        else:
            time_difference = utc_time - current_time
            for date in range(len(all_dates)):
                all_dates[date] = datetime.utcfromtimestamp(all_dates[date]) - time_difference


        return all_volumes, all_opens, all_closes, all_dates


if __name__ == "__main__":

    test = FinViz()
  