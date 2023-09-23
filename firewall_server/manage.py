from server import Brain

if __name__ == "__main__":
    brain = Brain("127.0.0.1", 12345, display_logs=True)
    brain.accept_requests()
