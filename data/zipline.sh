#!/bin/sh

## Daily Data

mkdir -p daily
for file in VNX/*/Price.csv; do
  ticker=`echo $file | cut -d'/' -f 2`
  python daily.py $file daily/$ticker.csv 2010-01-01
  break
done

python daily.py VN30F/vnindex/Price.csv daily/VNINDEX.csv 2010-01-01

## extension.py

mkdir -p ~/.zipline
HSX=`cat hsx.py`
echo "from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

$HSX

register(
    'vn',
    csvdir_equities(
        ['daily'],
        '$PWD',
    ),
    calendar_name='HSX'
)" > ~/.zipline/extension.py
