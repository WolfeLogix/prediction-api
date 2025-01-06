import backtrader as bt
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

# Main function with CLI


def main():
    parser = argparse.ArgumentParser(description='Backtrader SMA Strategy')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Backtest command
    backtest_parser = subparsers.add_parser('backtest', help='Run backtest')
    backtest_parser.add_argument(
        '--data', required=True, help='Path to historical data CSV file')

    args = parser.parse_args()

    if args.command == 'backtest':
        run_backtest(args.data)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
