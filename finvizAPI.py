import datetime
import logging
# from datetime import datetime
from typing import Tuple, Union
import requests


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


        # Convert the date to human readable format
        for i in range(len(json_response["date"])):
            json_response["date"][i] = datetime.datetime.utcfromtimestamp(int(json_response["date"][i]))
   

        # print(json_response)
        # self._time = (json_response["date"][-2])
        # self._volume = int(json_response["volume"][-2])
        # self._price = float(json_response["lastOpen"])
        # self._logger.info(f"SUCCESSFUL call: ticker: {ticker}, time: {self._time}, volume: {self._volume}, price: {self._price}")
        # return self._time, self._volume, self._price
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
        # self._time = int(json_response["date"][:-2])
        # self._volume = int(json_response["volume"][:-2])
        # self._price = float(json_response["lastOpen"])
        # return self._time, self._volume, self._price
        all_volumes = [float(i) for i in json_response["volume"]]
        all_opens = [float(i) for i in json_response["open"]]
        all_closes = [float(i) for i in json_response["close"]]
        all_dates = [float(i) for i in json_response["date"]]
        
        for date in range(len(all_dates)):
            all_dates[date] = datetime.datetime.utcfromtimestamp(all_dates[date])
        return all_volumes, all_opens, all_closes, all_dates


if __name__ == "__main__":

    test = FinViz()
    # print(test.get_data())
    # test.get_data()
    all_valumes, all_opens, all_closes, all_dates = test.get_all_data("i1", "AAPL")
    print(all_opens[1], all_closes[0])
    print(all_dates[-1])
    print(datetime.datetime.now()) # time now
    data = test.get_data("i1", "AAPL")
    for i in range(len(data["date"])):
        print(data["date"][i], data["open"][i], data["close"][i])
    # time, volume, price = test.get_data()
    # print("Time:", time, "Volume:", volume, "Price:", price, sep="\n")

    # print("Human readable Time:", test.get_time())
