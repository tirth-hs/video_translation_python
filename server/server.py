# server/server.py

import os
import time
import random
from flask import Flask, jsonify

app = Flask(__name__)

class TranslationStatusServer:
    def __init__(self, delay):
        """
        Simulates a video translation backend.
        Args:
            delay (float): Configurable delay (in seconds) for translation completion.
        """
        self.delay = delay  # Delay in seconds
        self.start_time = time.time()  # Start time for the translation job
        self.status = "pending"  # Initial status of the job
        self.progress = 0  # Initial progress (0%)
        self.expected_time = delay  # Expected time for job completion
        self._set_final_status_after_delay()

    def _set_final_status_after_delay(self):
        """Set the final status ('completed' or 'error') after the delay."""
        def update_status():
            self.status = "completed" if random.random() > 0.5 else "error"
            self.progress = 100  # Set progress to 100% when finished

        # Use a timer thread to simulate delay
        from threading import Timer
        Timer(self.delay, update_status).start()

    def get_status(self):
        """
        Get the current status of the job, including progress and expected time.
        Returns:
            dict: A dictionary with the current status, progress, and expected time.
        """
        elapsed_time = time.time() - self.start_time
        self.progress = min(100, int((elapsed_time / self.delay) * 100))  # Progress calculation
        return {
            "status": self.status if elapsed_time >= self.delay else "pending",
            "progress": self.progress,
            "expectedTime": self.expected_time,
        }


# Configure the server with a random delay (60 to 180 seconds)
random_translation_time = random.uniform(60, 180)
server = TranslationStatusServer(random_translation_time)

@app.route("/status", methods=["GET"])
def status_endpoint():
    """Endpoint to get the current status of the translation job."""
    return jsonify(server.get_status())

def run_server():
    """Run the Flask server."""
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    run_server()
