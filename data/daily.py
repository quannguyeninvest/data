import sys
import pandas as pd

from datetime import datetime


source = sys.argv[1]
dest = sys.argv[2]
start_date = sys.argv[3]

date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')
index = pd.read_csv(
    'VN30F/vnindex/Price.csv',
    index_col='date',
    parse_dates=['date'],
    date_parser=date_parser,
    usecols=['date']
)[start_date:]

data = pd.read_csv(
    source,
    index_col='date',
    parse_dates=['date'],
    date_parser=date_parser,
    usecols=['date','open','high','low','close','volume']
)[start_date:]

if not data.empty:
    index.join(data).fillna(method='ffill').fillna(method='bfill').dropna().to_csv(dest)
