import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import StandardScaler


class ThreadDetection:
    pass


class LSTMPacketThreadDetection(ThreadDetection):
    def __init__(
            self,
            model_path: Path | str = None,
            seq_length: int = 10,
            mean: list[float] = None,
            scale: list[float] = None,
            min_data_len: int = 20,
            flagged_threshold: float = 0.7,
            unsafe_threshold: float = 0.9
    ):
        if min_data_len <= seq_length:
            raise ValueError("min_data_len must be greater than seq_length")

        self.model = load_model(
            model_path or
            Path(
                os.path.dirname(os.path.abspath(__file__)),
                "pre_trained_models",
                "LSTM.keras"
            )
        )
        self.seq_length = seq_length
        self.flagged_threshold = flagged_threshold
        self.unsafe_threshold = unsafe_threshold

        self.scaler = StandardScaler()
        self.scaler.mean_ = mean or [-3.4638958368304884e-17, 6.52811138479592e-17, -4.618527782440651e-17]
        self.scaler.scale_ = scale or [0.9999999999999984, 1.0000000000000018, 0.9999999999999999]

    def preprocess_input(self, input_data):
        # Convert timestamp to seconds since the start time
        start_time = datetime.strptime("2023-01-01", "%Y-%m-%d")
        input_data['Timestamp'] = (input_data['Timestamp'] - start_time).dt.total_seconds()

        # Standardize other features
        input_features = ["PacketSize", "SourcePort", "DestinationPort"]
        input_data[input_features] = self.scaler.transform(input_data[input_features])

        return input_data[input_features].values

    def _get_traffic_rating(self, input_data):
        input_data = self.preprocess_input(input_data)

        # Check if there are enough data points for prediction
        if len(input_data) < self.seq_length:
            return "Insufficient data for prediction"

        x_input_seq = []

        # Create input sequences for the LSTM model
        for i in range(self.seq_length, len(input_data)):
            x_input_seq.append(input_data[i - self.seq_length:i])

        x_input_seq = np.array(x_input_seq)

        # Make predictions
        predictions = self.model.predict(x_input_seq)

        # Calculate the average prediction (you can use a different method based on your problem)
        avg_prediction = np.mean(predictions)

        if avg_prediction >= self.unsafe_threshold:
            return 2
        elif avg_prediction >= self.flagged_threshold:
            return 1
        else:
            return 0

    def predict(
            self,
            timestamps: list[str],
            packet_sizes: list[int],
            source_ip: list[str],
            destination_ip: list[str],
            source_port: list[int],
            destination_port: list[int]
    ):
        input_sequence = pd.DataFrame({
            "Timestamp": pd.to_datetime(timestamps),
            "PacketSize": packet_sizes,
            "SourceIP": source_ip,
            "DestinationIP": destination_ip,
            "SourcePort": source_port,
            "DestinationPort": destination_port
        })

        result = self._get_traffic_rating(input_sequence)
        print(f"Is Malicious: {result}")

        return result
