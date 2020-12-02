import data
import zipline

def get_benchmark_returns(symbol):
    """
    Get a Series of benchmark returns associated with `symbol`.
    Default is `VNINDEX`.

    Parameters
    ----------
    symbol : str
        Benchmark symbol for which we're getting the returns.
    """
    if symbol == 'SPY':
        symbol = 'VNINDEX'

    df = data.get_pricing(symbol, start_date=None)['close']

    return df.tz_localize('UTC').pct_change(1).iloc[1:]

# Patching
zipline.data.benchmarks.get_benchmark_returns = get_benchmark_returns
