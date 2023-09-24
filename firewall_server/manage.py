from server import Brain

if __name__ == "__main__":
    brain = Brain("192.168.207.148", 1234, display_logs=True)
    brain.accept_requests()
