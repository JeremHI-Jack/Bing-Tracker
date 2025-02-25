# Bing Tracker

## Overview

**Bing Tracker** is a Python script that searches Bing for multiple keywords, retrieves up to 50 pages of results for each keyword, and saves the filtered results into separate CSV files. The script handles multiple types of results (organic, sponsored, and other), filters out results from whitelisted domains, and removes entries without a valid domain.

## Features

- **Multi-threaded searches:** Processes multiple keywords concurrently (up to 10 threads by default).
- **Bing search integration:** Retrieves up to 50 pages per keyword.
- **Result types:**
  - *Organic* results (standard Bing listings)
  - *Sponsored* results (ads)
  - *Other* results (direct answers, info boxes, etc.)
- **Domain filtering:**
  - Excludes results from domains listed in `whitelist.txt`.
  - Removes entries that have no valid domain.
- **CSV output:**
  - Each keyword generates its own CSV file.
  - Uses UTF-8 encoding to handle accented characters.
- **Robustness:**
  - Utilizes a retry strategy for network requests.
  - Implements a randomized delay between page fetches to reduce the risk of being blocked.

## Project Structure
BING-TRACKER/ 
├── bing_tracker.py # Main Python script 
├── keywords.txt # List of keywords (one per line) 
├── whitelist.txt # List of domains to exclude 
└── README.md # This file

## Requirements

- Python 3.6 or higher (tested up to Python 3.13)
- Dependencies:
  - `requests`
  - `beautifulsoup4`
- Install dependencies with:
  ```bash
  pip install requests beautifulsoup4

Usage
1. Prepare Input Files:
keywords.txt: Add one keyword per line.
whitelist.txt: Add one domain per line (in lowercase) to exclude from results.

2. Run the Script:
python bing_tracker.py

3. Output:
A separate CSV file is generated for each keyword (e.g., buy_laptop.csv).
The CSV files contain the following columns: Keyword, Result Type, Title, Link, Domain, Description.
