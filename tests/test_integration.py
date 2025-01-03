import pytest
import multiprocessing
import time
import os
import requests

from server.server import run_server
from client.client import TranslationClient




@pytest.fixture(scope="module")
def server_process():
    os.environ["PORT"] = "5001"  # Ensure the port matches the server
    proc = multiprocessing.Process(target=run_server)
    proc.start()

    # Wait for the server to start
    for _ in range(10):  # Try for 10 seconds
        try:
            response = requests.get("http://localhost:5001/status")
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(1)
    else:
        proc.terminate()
        pytest.fail("Server failed to start")

    yield proc
    proc.terminate()
    proc.join()

def test_poll_status(server_process):
    client = TranslationClient("http://localhost:5001")
    result = client.poll_status()
    assert result in ["completed", "error"], "Expected result to be 'completed' or 'error'"
    print(f"Final Status: {result}")
