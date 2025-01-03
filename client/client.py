import requests
import time
import random
import math
import logging

logging.basicConfig(level=logging.INFO)

class StatusFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_status(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error fetching status: {e}")
            return {"status": "error", "progress": 0, "expectedTime": 0}


class AdaptivePollingStrategy:
    def __init__(self, transition_progress=60):
        self.transition_progress = transition_progress

    def get_interval(self, attempt, progress, expected_time):
        dynamic_max_interval = expected_time / 3.5
        dynamic_base_interval = expected_time / 30

        if progress < self.transition_progress:
            backoff_interval = min(dynamic_base_interval * (2 ** attempt), dynamic_max_interval)
            return self._add_jitter(backoff_interval)
        else:
            progress_factor = (progress - self.transition_progress) / (100 - self.transition_progress)
            decay_interval = dynamic_base_interval + (dynamic_max_interval - dynamic_base_interval) * math.exp(-progress_factor * 2.5)
            return self._add_jitter(max(dynamic_base_interval, min(decay_interval, dynamic_max_interval)))

    def _add_jitter(self, interval):
        jitter = random.uniform(-0.1 * interval, 0.1 * interval)
        return interval + jitter


class TranslationClient:
    def __init__(self, url):
        self.fetcher = StatusFetcher(url)
        self.strategy = AdaptivePollingStrategy()

    def poll_status(self):
        attempt = 0
        while True:
            status_data = self.fetcher.fetch_status()
            status, progress, expected_time = (
                status_data.get("status"),
                status_data.get("progress"),
                status_data.get("expectedTime"),
            )
            logging.info(
                f"Attempt {attempt + 1}: Status - {status}, Progress - {progress}%, Expected Time - {expected_time}s"
            )

            if status in ["completed", "error"]:
                return status

            interval = self.strategy.get_interval(attempt, progress, expected_time)
            logging.info(f"Waiting for {interval:.2f} seconds before retrying...")
            time.sleep(interval)
            attempt += 1
