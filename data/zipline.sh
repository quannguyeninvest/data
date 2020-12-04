#!/bin/sh

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
