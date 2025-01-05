import backtrader as bt
import torch
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from joblib import load  # For loading the saved scaler


# LSTM Model Definition (same as during training)
class LSTMPricePredictionModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMPricePredictionModel, self).__init__()
        self.lstm = torch.nn.LSTM(
            input_size, hidden_size, num_layers, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.lstm.num_layers, x.size(
            0), self.lstm.hidden_size)  # Hidden state
        c0 = torch.zeros(self.lstm.num_layers, x.size(
            0), self.lstm.hidden_size)  # Cell state
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])  # Last output for the sequence
        return out


# Custom Backtrader Strategy with LSTM Model
class LSTMMLStrategy(bt.Strategy):
    params = (('model_path', 'lstm_model.pth'),
              ('scaler_path', 'scaler.joblib'), ('sequence_length', 5))

    def __init__(self):
        # Load LSTM model
        self.input_size = 16  # Number of features
        self.hidden_size = 64  # Number of LSTM neurons
        self.num_layers = 2  # Number of LSTM layers
        self.output_size = 1  # Predicting next day's price
        self.model = LSTMPricePredictionModel(
            self.input_size, self.hidden_size, self.num_layers, self.output_size)
        self.model.load_state_dict(torch.load(self.params.model_path))
        self.model.eval()

        # Load the pre-trained MinMaxScaler
        self.scaler = load(self.params.scaler_path)

        # Store sequences for each stock
        self.sequences = {d._name: [] for d in self.datas}

    def next(self):
        for i, data in enumerate(self.datas):
            symbol = data._name  # Symbol for the data feed

            # Extract the most recent historical data for the sequence
            features = [
                [
                    data.open[-j],
                    data.high[-j],
                    data.low[-j],
                    data.close[-j],
                    data.volume[-j],
                    data.close[-j] - data.open[-j],  # Example custom feature
                    (data.high[-j] - data.low[-j]) / \
                    (data.volume[-j] + 1),  # Avoid division by zero
                    ...
                ]
                for j in range(self.params.sequence_length)
            ]

            # Convert to NumPy array
            features = np.array(features, dtype=np.float32)

            # Normalize the features
            features_scaled = self.scaler.transform(
                features)  # Use pre-fitted scaler
            features_tensor = torch.from_numpy(features_scaled).unsqueeze(
                0)  # Shape: (1, seq_len, input_size)

            # Make prediction
            predicted_price = self.model(features_tensor).item()

            # Decision logic
            current_price = data.close[0]
            if predicted_price > current_price * 1.01 and not self.getposition(data):
                self.buy(data=data, size=10)  # Buy 10 shares
                print(f"BUY {symbol} at {current_price}")
            elif self.getposition(data) and predicted_price < current_price * 0.99:
                self.close(data=data)  # Close position
                print(f"SELL {symbol} at {current_price}")


# Backtrader Setup
if __name__ == "__main__":
    cerebro = bt.Cerebro()

    # Load data feeds (multiple symbols)
    symbols = ['AAPL', 'GOOG']
    for symbol in symbols:
        data = bt.feeds.YahooFinanceData(
            dataname=symbol, fromdate=datetime(2021, 1, 1), todate=datetime(2023, 1, 1)
        )
        data._name = symbol  # Set symbol as name for easy reference
        cerebro.adddata(data)

    # Add strategy with LSTM model
    cerebro.addstrategy(LSTMMLStrategy, model_path="lstm_model.pth",
                        scaler_path="scaler.joblib", sequence_length=5)

    # Set initial portfolio balance
    cerebro.broker.setcash(100000)

    # Run the strategy
    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    # Plot results
    cerebro.plot()
