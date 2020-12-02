import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from urllib import request


def get_pricing(symbol, start_date='2018-01-01', end_date=None, frequency='daily', fields=None):
    """Get pricing

    Keyword arguments:
    symbol (str) -- Asset symbol
    start_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date or start intraday minute for the returned data. Defaults to '2018-01-01'.
    end_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date or start intraday minute for the returned data. Defaults to None.
    frequency ({'daily', 'minute'}, optional) -- Resolution of the data to be returned
    fields (str or list, optional) -- String or list drawn from {'open', 'high', 'low', 'close', 'volume'}. Default behavior is to return all fields.
    """
    usecols = None
    if fields is not None:
        usecols = ['date']
        if type(fields) is list:
            for field in fields:
                usecols.append(field)
        else:
            usecols.append(fields)

    file = 'Price'
    date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')
    if frequency == 'minute':
        file = 'Prices'
        date_parser = lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M')

    for exchange in os.listdir():
        filepath = '{}/{}/{}.csv'.format(exchange, symbol, file)
        if os.path.isfile(filepath):
            prices = pd.read_csv(
                filepath,
                index_col='date',
                parse_dates=['date'],
                date_parser=date_parser,
                usecols=usecols
            )[start_date:end_date]
            prices.exchange = exchange
            prices.symbol = symbol
            return prices

    return None


def get_prices(*symbols, start_date='2018-01-01', end_date=None, frequency='daily', field='close'):
    """Get prices

    Keyword arguments:
    symbols (list of str) -- Asset symbols
    start_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date or start intraday minute for the returned data. Defaults to '2018-01-01'.
    end_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date or start intraday minute for the returned data. Defaults to None.
    frequency ({'daily', 'minute'}, optional) -- Resolution of the data to be returned
    field (str, optional) -- String or list drawn from {'open', 'high', 'low', 'close', 'volume'}. Default behavior is to return 'close'.
    """
    prices = None
    for symbol in symbols:
        price = get_pricing(symbol, start_date=start_date, end_date=end_date, frequency=frequency, fields=field)
        if price is None:
            continue
        
        price = price.rename(columns={field: symbol})
        if prices is None:
            prices = price
        else:
            prices = prices.join(price)
    
    return prices


def get_events(symbol, start_date=None, end_date=None):
    """Get events

    Keyword arguments:
    symbol (str) -- Asset symbol
    start_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date. Defaults to None.
    end_date (str or pd.Timestamp, optional) -- String or Timestamp representing a start date. Defaults to None.
    """
    for exchange in os.listdir():
        filepath = '{}/{}/Events.csv'.format(exchange, symbol)
        if os.path.isfile(filepath):
            return pd.read_csv(
                filepath,
                index_col='disclosuredDate',
                parse_dates=['disclosuredDate'],
                date_parser=lambda x: datetime.strptime(x, '%Y-%m-%d')
            )[start_date:end_date]

    return None


def StocksVN():
    """Get list of stocks in VN Market
    """
    return pd.read_csv('VNX.csv', index_col='ticker')


def TradableStocksVN():
    """Get list of tradable stocks in VN Market
    """
    tickers = StocksVN()
    return tickers[tickers.AvgValue20P > 8e8]


class Fundamentals:
    @staticmethod
    def loadCsv(symbol, file):
        """Load data from csv file

        Keyword arguments:
        symbol (str) -- Asset symbol
        file (str) -- File name
        """
        for exchange in os.listdir():
            filepath = '{}/{}/{}.csv'.format(exchange, symbol, file)
            if os.path.isfile(filepath):
                data = pd.read_csv(
                    filepath,
                    index_col=['Year', 'Quarter'] # data.loc[(year, quarter)]
                )

                filepath = '{}/{}/Report.csv'.format(exchange, symbol)
                if os.path.isfile(filepath):
                    data = data.join(pd.read_csv(
                        filepath,
                        index_col=['Year', 'Quarter'],
                        parse_dates=['date'],
                        date_parser=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                    ))

                return data

        return None


    @staticmethod
    def BalanceSheetQuarter(symbol):
        """Get balance sheet quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'BalanceSheetQuarter')


    @staticmethod
    def IncomeStatementQuarter(symbol):
        """Get imcome statement quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'IncomeStatementQuarter')


    @staticmethod
    def DCashFlowQuarter(symbol):
        """Get direct cash flow quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'DCashFlowQuarter')


    @staticmethod
    def ICashFlowQuarter(symbol):
        """Get indirect cash flow quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'ICashFlowQuarter')


    @staticmethod
    def CashFlowQuarter(symbol):
        """Get cash flow quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        cfq = Fundamentals.ICashFlowQuarter(symbol)
        if cfq is None:
            return Fundamentals.DCashFlowQuarter(symbol)
        
        return cfq


    @staticmethod
    def IndicatorsQuarter(symbol):
        """Get indicators quarterly

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'IndicatorsQuarter')


    @staticmethod
    def BalanceSheet(symbol):
        """Get balance sheet data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'BalanceSheet')


    @staticmethod
    def IncomeStatement(symbol):
        """Get income statement data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'IncomeStatement')


    @staticmethod
    def DCashFlow(symbol):
        """Get direct cash flow data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'DCashFlow')


    @staticmethod
    def ICashFlow(symbol):
        """Get indirect cash flow data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'ICashFlow')


    @staticmethod
    def CashFlow(symbol):
        """Get cash flow data

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        cf = Fundamentals.ICashFlow(symbol)
        if cf is None:
            return Fundamentals.DCashFlow(symbol)
        
        return cf


    @staticmethod
    def Indicators(symbol):
        """Get indicators

        Keyword arguments:
        symbol (str) -- Asset symbol
        """
        return Fundamentals.loadCsv(symbol, 'Indicators')


def join_price(price, fundamental):
    fund = fundamental
    if not isinstance(fundamental.index, pd.DatetimeIndex):
        fund = fund.reset_index().set_index('date')
    
    fund = pd.DataFrame(index=price.index).join(fund, how='outer')
    return price.join(fund.fillna(method='ffill'))
