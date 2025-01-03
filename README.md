
# Translation Client Library - README

## Overview

The Translation Client Library is designed to interact with a simulated video translation backend. It provides an efficient way to repeatedly query the translation job status using an **Adaptive Polling Strategy**. This strategy dynamically adjusts polling intervals based on progress and expected completion time, optimizing resource usage while ensuring timely updates. The library reduces unnecessary network requests during early stages and increases polling frequency as the task nears completion.

This documentation will guide you through the steps to use the library effectively.

---

## Getting Started

### Installation

Clone the repository containing the server and client code, and navigate to the project directory:

```bash
git clone https://github.com/your-repo/video-translation-python.git
cd video-translation-python
```

### Prerequisites

To use the client library, ensure you have the following installed:

- **Python 3.8 or above**
- **Virtual environment** (optional but recommended)

Install dependencies by running:
```bash
pip install -r requirements.txt
```

---

## Assumptions

### Server

1. The server provides **progress** updates along with the status of video translation. These updates are essential for the hybrid polling strategy to function effectively, enabling dynamic adjustments based on job progress.

2. The server sends an **expectedTime** value, which is an approximate estimate of the time required for video translation completion. While this value may not be exact due to the volatile nature of translation, it helps determine suitable polling intervals dynamically.

3. The server simulates video translation with a **randomly assigned delay** ranging between **1 to 3 minutes**. This delay is configurable and can be adjusted based on specific requirements.

### Client Library

1. The **transitionProgress** parameter defines the point at which the polling strategy switches from **exponential backoff** to **exponential decay**. Currently, this value is set to **60%**, as experimentation demonstrated that this threshold offers an optimal balance between responsiveness and efficiency.

2. Variables within the **get_interval** function were determined through extensive experimentation to balance resource efficiency and responsiveness, ensuring effectiveness across varying scenarios.

---

## Integration Test

To demonstrate the client library's functionality, an integration test has been provided. The test spins up the server and uses the client library to fetch the final job status.

### Automation of Server Startup

The integration test automatically starts the server as a child process before testing and uses **pytest** fixtures to manage the server lifecycle.

- **Benefit**: This automation simplifies the testing process, ensuring the server is running and ready before tests execute. This demonstrates best practices and enhances the developer experience.

To run the integration test:
```bash
pytest tests/
```

You may see logs like the following during execution:

```
Attempt 1: Status - pending, Progress - 10%, Expected Time - 120s
Waiting for 5 seconds before retrying...
...
Final Status: completed
```

---

## Using the Client Library

The client library consists of three main components:

1. **StatusFetcher**  
   - Fetches the status of the translation job from the server.  
   - Returns a JSON response that includes `{ status, progress, expectedTime }`.  
   - **Error Handling**: Catches network errors during HTTP requests and returns a default error status, ensuring the client can continue operating even if a temporary network error occurs.

2. **AdaptivePollingStrategy**  
   - Determines the polling interval based on job progress to optimize resource usage.  
   - **Dynamic Adjustment**: Uses the **expectedTime** returned by the server to calculate suitable intervals based on job duration.  
   - **Configurable Parameters**: Allows customization of polling intervals, decay factors, and transition progress thresholds.

3. **StatusChecker**  
   - Uses the fetcher and polling strategy to query the status until the job is completed or fails.  
   - **Comprehensive Logging**: Logs detailed information at each polling attempt, including status, progress, expected time, and waiting intervals, aiding monitoring and troubleshooting.

---

## Running the Server

The translation server simulates a video translation backend with a configurable random delay. You need to start the server before running the client.

```bash
python server/server.py
```

This will start the server on `http://localhost:5001`. You should see a message like:
```
Server running on http://localhost:5001
```

---

## Example Usage

Here’s an example of how to use the client library to query the status of a translation job:

```python
from client.client import TranslationClient

client = TranslationClient("http://localhost:5001")
final_status = client.poll_status()
print(f"Final Status: {final_status}")
```

---

## Implementation Details

- **StatusFetcher**  
  - Sends repeated GET requests to fetch job status.
  - Handles network failures by returning a default `error` status.

- **AdaptivePollingStrategy**  
  - Implements **exponential backoff** when progress is below a certain threshold.  
  - Shifts to **exponential decay** as progress nears completion.  
  - Uses jitter to avoid synchronized requests.

- **StatusChecker**  
  - Coordinates polling by using both **StatusFetcher** and **AdaptivePollingStrategy**.  
  - Logs status and progress at each attempt.

---

## Conclusion

The Translation Client Library provides an optimized, user-friendly way to interact with a simulated video translation backend. By implementing **adaptive polling**, it balances server load and responsiveness, ensuring timely updates for the user. The code is built following a modular design, making it easier to update or extend individual components without affecting the rest of the library.

Additionally, features such as **error handling** and **comprehensive logging** make the client robust. The inclusion of an automated integration test reflects a **customer-centric approach** that aims to provide a smooth experience for both developers and end-users.

---

