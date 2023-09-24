import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

class ThreadDetection:
    """Base class for traffic thread detection."""

    pass

class LSTMPacketThreadDetection(ThreadDetection):
    """
    LSTM-based Traffic Thread Detection.

    This class is designed to detect malicious network traffic threads using an LSTM-based model.

    Args:
        model_path (str or Path, optional): Path to the pre-trained LSTM model. Defaults to None.
        seq_length (int, optional): Length of the input sequence for the LSTM model. Defaults to 10.
        mean (list of float, optional): Mean values for feature scaling. Defaults to None.
        scale (list of float, optional): Scale values for feature scaling. Defaults to None.
        min_data_len (int, optional): Minimum required data length. Defaults to 20.
        flagged_threshold (float, optional): Threshold for flagging traffic as suspicious. Defaults to 0.5.
        unsafe_threshold (float, optional): Threshold for flagging traffic as unsafe or malicious. Defaults to 0.9.

    Raises:
        ValueError: Raised if `min_data_len` is less than or equal to `seq_length`.

    Attributes:
        model (keras.models.Model): The LSTM model for traffic detection.
        seq_length (int): Length of the input sequence.
        flagged_threshold (float): Threshold for flagging traffic as suspicious.
        unsafe_threshold (float): Threshold for flagging traffic as unsafe or malicious.
        scaler (StandardScaler): StandardScaler for feature scaling.

    Methods:
        preprocess_input(input_data): Preprocesses input data for prediction.
        _get_traffic_rating(input_data): Gets traffic rating based on input data.
        predict(timestamps, packet_sizes, source_ip, destination_ip, source_port, destination_port):
            Predicts if the network traffic is malicious or safe.

    Example:
        # Create an instance of LSTMPacketThreadDetection
        detector = LSTMPacketThreadDetection()

        # Provide input data for prediction
        result = detector.predict(
            timestamps=["2023-09-24 10:00:00"],
            packet_sizes=[1000],
            source_ip=["192.168.1.1"],
            destination_ip=["192.168.1.2"],
            source_port=[12345],
            destination_port=[80]
        )

        # Check the prediction result
        print(f"Is Malicious: {result}")
    """

    def __init__(
            self,
            model_path: Path | str = None,
            seq_length: int = 10,
            mean: list[float] = None,
            scale: list[float] = None,
            min_data_len: int = 20,
            flagged_threshold: float = 0.5,
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
        """
        Preprocesses input data for prediction.

        Args:
            input_data (pd.DataFrame): Input data containing timestamps, packet sizes, source IP, destination IP,
                source port, and destination port.

        Returns:
            np.ndarray: Preprocessed input data.
        """
        # Convert timestamp to seconds since the start time
        start_time = datetime.strptime("2023-01-01", "%Y-%m-%d")
        input_data['Timestamp'] = (input_data['Timestamp'] - start_time).dt.total_seconds()

        # Standardize other features
        input_features = ["PacketSize", "SourcePort", "DestinationPort"]
        input_data[input_features] = self.scaler.transform(input_data[input_features])

        return input_data[input_features].values

    def _get_traffic_rating(self, input_data):
        """
        Gets traffic rating based on input data.

        Args:
            input_data (pd.DataFrame): Preprocessed input data.

        Returns:
            int: Traffic rating (0 for safe, 1 for flagged, 2 for unsafe).
        """
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
        """
        Predicts if the network traffic is malicious or safe.

        Args:
            timestamps (list of str): List of timestamps.
            packet_sizes (list of int): List of packet sizes.
            source_ip (list of str): List of source IP addresses.
            destination_ip (list of str): List of destination IP addresses.
            source_port (list of int): List of source port numbers.
            destination_port (list of int): List of destination port numbers.

        Returns:
            int: Traffic rating (0 for safe, 1 for flagged, 2 for unsafe).
        """
        input_sequence = pd.DataFrame({
            "Timestamp": pd.to_datetime(timestamps),
            "PacketSize": packet_sizes,
            "SourceIP": source_ip,
            "DestinationIP": destination_ip,
            "SourcePort": source_port,
            "DestinationPort": destination_port
        })

        result = self._get_traffic_rating(input_sequence)

        return result
