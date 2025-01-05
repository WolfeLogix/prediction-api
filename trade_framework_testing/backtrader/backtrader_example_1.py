import backtrader as bt
import torch
import numpy as np
from datetime import datetime

# PyTorch model class (same as training model)


class PricePredictionModel(torch.nn.Module):
    def __init__(self):
        super(PricePredictionModel, self).__init__()
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(16, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.fc(x)

# Custom Backtrader Strategy


class MultiAssetMLStrategy(bt.Strategy):
    params = (('model_path', 'model.pth'),)

    def __init__(self):
        # Load the PyTorch model
        self.model = PricePredictionModel()
        self.model.load_state_dict(torch.load(self.params.model_path))
        self.model.eval()  # Evaluation mode

        # Track open positions for each asset
        self.positions_by_asset = {d._name: None for d in self.datas}

    def next(self):
        for i, data in enumerate(self.datas):
            symbol = data._name  # Symbol name (e.g., "AAPL" or "GOOG")

            # Extract features for the current asset
            open_prev_day = data.open[-1]
            close_prev_day = data.close[-1]
            high_prev_day = data.high[-1]
            low_prev_day = data.low[-1]
            volume_prev_day = data.volume[-1]

            # Create 16-feature input for PyTorch model
            features = np.array([
                close_prev_day - open_prev_day,  # Example feature
                (high_prev_day - low_prev_day) / \
                volume_prev_day,  # Another example
                ...
            ], dtype=np.float32)

            # Convert to PyTorch tensor
            features_tensor = torch.from_numpy(features).unsqueeze(0)

            # Make prediction for this asset
            predicted_price = self.model(features_tensor).item()

            # Decision logic
            current_price = data.close[0]
            # Buy signal
            if predicted_price > current_price * 1.01 and not self.getposition(data):
                self.buy(data=data, size=10)  # Buy 10 shares
                print(f"BUY {symbol} at {current_price}")
            # Sell signal
            elif self.getposition(data) and predicted_price < current_price * 0.99:
                self.close(data=data)  # Close position
                print(f"SELL {symbol} at {current_price}")


# Initialize Backtrader Cerebro Engine
cerebro = bt.Cerebro()

# Load data feeds for multiple assets
symbols = ['AAPL', 'GOOG']
for symbol in symbols:
    data = bt.feeds.YahooFinanceData(
        dataname=symbol, fromdate=datetime(2021, 1, 1), todate=datetime(2023, 1, 1)
    )
    data._name = symbol  # Set symbol as the name for reference
    cerebro.adddata(data)

# Add strategy and pass PyTorch model path
cerebro.addstrategy(MultiAssetMLStrategy, model_path="model.pth")

# Set initial portfolio balance
cerebro.broker.setcash(100000)

# Run the backtest
cerebro.run()

# Plot results
cerebro.plot()
