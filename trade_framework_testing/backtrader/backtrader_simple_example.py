import backtrader as bt
import alpaca_backtrader_api
from datetime import datetime
import argparse
import sys

# Define the SMA Strategy
class SmaCross(bt.Strategy):
    params = (
        ('pfast', 10),  # period for the fast SMA
        ('pslow', 30),  # period for the slow SMA
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast SMA
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow SMA
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast SMA crosses above slow SMA
                self.buy()
        elif self.crossover < 0:  # in the market & fast SMA crosses below slow SMA
            self.sell()

# Function to run backtest
def run_backtest(data_path):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    # Load data
    data = bt.feeds.YahooFinanceCSVData(
        dataname=data_path,
        fromdate=datetime(2020, 1, 1),
        todate=datetime(2021, 12, 31),
        reverse=False
    )
    cerebro.adddata(data)

    # Set initial cash
    cerebro.broker.setcash(100000.0)

    # Set commission
    cerebro.broker.setcommission(commission=0.001)

    # Print starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run backtest
    cerebro.run()

    # Print final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()

# Function to run live trading
def run_live(api_key, api_secret, symbol, cash, timeframe):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    # Alpaca settings
    ALPACA_API_KEY = api_key
    ALPACA_API_SECRET = api_secret
    ALPACA_PAPER = True  # Change to False for live trading

    store = alpaca_backtrader_api.AlpacaStore(
        key_id=ALPACA_API_KEY,
        secret_key=ALPACA_API_SECRET,
        paper=ALPACA_PAPER,
        usePolygon=False
    )

    DataFactory = store.getdata
    broker = store.getbroker()
    cerebro.setbroker(broker)

    data = DataFactory(
        dataname=symbol,
        timeframe=bt.TimeFrame.Minutes,
        compression=timeframe,
        historical=False
    )
    cerebro.adddata(data)

    # Set initial cash
    cerebro.broker.setcash(cash)

    # Set commission
    cerebro.broker.setcommission(commission=0.001)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run live trading
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Main function with CLI


def main():
    parser = argparse.ArgumentParser(description='Backtrader SMA Strategy')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Backtest command
    backtest_parser = subparsers.add_parser('backtest', help='Run backtest')
    backtest_parser.add_argument(
        '--data', required=True, help='Path to historical data CSV file')

    # Live command
    live_parser = subparsers.add_parser('live', help='Run live trading')
    live_parser.add_argument('--api_key', required=True, help='Alpaca API Key')
    live_parser.add_argument(
        '--api_secret', required=True, help='Alpaca API Secret')
    live_parser.add_argument('--symbol', default='AAPL',
                             help='Trading symbol, e.g., AAPL')
    live_parser.add_argument('--cash', type=float,
                             default=100000.0, help='Initial cash')
    live_parser.add_argument('--timeframe', type=int,
                             default=1, help='Timeframe in minutes')

    args = parser.parse_args()

    if args.command == 'backtest':
        run_backtest(args.data)
    elif args.command == 'live':
        run_live(args.api_key, args.api_secret,
                 args.symbol, args.cash, args.timeframe)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
