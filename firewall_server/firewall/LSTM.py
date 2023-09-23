import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

seq_length = 10


def preprocess_input(input_data):
    # Convert timestamp to seconds since the start time
    start_time = datetime.strptime("2023-01-01", "%Y-%m-%d")
    input_data['Timestamp'] = (input_data['Timestamp'] - start_time).dt.total_seconds()

    # Standardize other features
    input_features = ["PacketSize", "SourcePort", "DestinationPort"]
    input_data[input_features] = scaler.transform(input_data[input_features])

    return input_data[input_features].values


def test_sequence(input_data, model):
    input_data = preprocess_input(input_data)

    # Check if there are enough data points for prediction
    if len(input_data) < seq_length:
        return "Insufficient data for prediction"

    X_input_seq = []

    # Create input sequences for the LSTM model
    for i in range(seq_length, len(input_data)):
        X_input_seq.append(input_data[i - seq_length:i])

    X_input_seq = np.array(X_input_seq)

    # Make predictions
    predictions = model.predict(X_input_seq)

    # Calculate the average prediction (you can use a different method based on your problem)
    avg_prediction = np.mean(predictions)

    # Define a threshold for classifying the sequence as malicious or not
    threshold = 0.5

    if avg_prediction >= threshold:
        return "Malicious"
    else:
        return "Not Malicious"


# Example usage:
# Load the trained model and scaler
model = load_model(Path(os.path.dirname(os.path.abspath(__file__)), "pre_trained_models", "LSTM.keras"))

scaler = StandardScaler()
scaler.mean_ = np.array([-3.4638958368304884e-17, 6.52811138479592e-17, -4.618527782440651e-17])
scaler.scale_ = np.array([0.9999999999999984, 1.0000000000000018, 0.9999999999999999])

# Create an example input data (sequence) with 20 data points
input_sequence = pd.DataFrame({
    "Timestamp": pd.to_datetime([
                                    "2023-01-01 01:00:00", "2023-01-01 01:01:00", "2023-01-01 01:02:00",
                                    "2023-01-01 01:03:00",
                                    "2023-01-01 01:04:00", "2023-01-01 01:05:00", "2023-01-01 01:06:00",
                                    "2023-01-01 01:07:00",
                                    "2023-01-01 01:08:00", "2023-01-01 01:09:00", "2023-01-01 01:10:00",
                                    "2023-01-01 01:11:00",
                                    "2023-01-01 01:12:00", "2023-01-01 01:13:00", "2023-01-01 01:14:00",
                                    "2023-01-01 01:15:00",
                                    "2023-01-01 01:16:00", "2023-01-01 01:17:00", "2023-01-01 01:18:00",
                                    "2023-01-01 01:19:00",
                                ] * 50),
    "PacketSize": [1500, 1600, 1700, 1550, 1650, 1750, 1600, 1500, 1550, 1700, 1750, 1600, 1650, 1500, 1700, 1750, 1550,
                   1600, 1650, 1500] * 50,
    "SourceIP": ["192.168.0.1"] * 1000,
    "DestinationIP": ["10.0.0.2"] * 1000,
    "SourcePort": [5000] * 1000,
    "DestinationPort": [80] * 1000
})

# Test the input sequence
result = test_sequence(input_sequence, model)
print(f"Sequence Classification: {result}")
