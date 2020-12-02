#!/bin/sh

## Daily Data

mkdir -p daily
# for file in VNX/*/Price.csv; do
#   ticker=`echo $file | cut -d'/' -f 2`
#   ln -sf ../$file daily/$ticker.csv
# done

for ticker in STB MSN FPT NVL TCB SAB PLX CTG GAS TCH HPG EIB HDB VPB MWG VJC BID ROS SBT MBB
do
  ln -sf ../VNX/$ticker/Price.csv daily/$ticker.csv
done
# ln -sf ../VN30F/vnindex/Price.csv daily/VNINDEX.csv

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
