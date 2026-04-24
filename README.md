# Network Monitor

A Python-based tool that monitors the availability and performance of websites by performing DNS checks, HTTP status checks, and latency measurement.

---

## Features

* Checks if a website is reachable (DNS resolution)
* Sends HTTP requests to verify uptime
* Measures response latency
* Runs checks concurrently for multiple websites
* Logs results with timestamps
* Displays colored output for better readability

---

## Requirements

* Python 3.x
* Required libraries:

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Project Structure

network_monitor/

│

├── monitor.py        # Main script

├── site.txt          # List of websites to monitor

├── requirements.txt  # Dependencies

├── README.md         # Project documentation

└── .gitignore        # Ignored files

---

## How It Works

1. Reads website URLs from `site.txt`
2. Performs DNS resolution check
3. Sends HTTP request to check status
4. Measures latency
5. Logs results and prints output

---

## Usage

1. Add websites in `site.txt`
2. Run the script:

```bash
python monitor.py
```

---

## Example Output

Checking google.com : UP (HTTP 200, 120 ms)

Checking example.com : DOWN (HTTP failed)

---

## Notes

* Ensure internet connection is active
* Some websites may block requests, causing false negatives
* Modify `site.txt` to monitor different websites

---

## Future Improvements

* Add email/SMS alerts
* Create GUI dashboard
* Add retry mechanism for failed checks
* Export logs to CSV/JSON

---
