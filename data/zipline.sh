#!/bin/sh

## Daily Data

mkdir -p daily
for file in VNX/*/Price.csv; do
  ticker=`echo $file | cut -d'/' -f 2`
  ln -sf ../$file daily/$ticker.csv
done

## extension.py

echo "import pandas as pd

from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

start_session = pd.Timestamp('2010-1-1', tz='utc')

register(
    'vn',
    csvdir_equities(
        ['daily'],
        '$PWD',
    ),
    calendar_name='24/5',
    start_session=start_session
)" > ~/.zipline/extension.py
