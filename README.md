# Bing Tracker

## Overview

**Bing Tracker** is a Python script that searches Bing for multiple keywords, retrieves up to 50 pages of results for each keyword, and saves the filtered results into separate CSV files. The script handles multiple types of results (organic, sponsored, and other), filters out results from whitelisted domains, and removes entries without a valid domain.

---

## Features

- **Multi-threaded searches**: Processes multiple keywords concurrently (up to 10 threads by default).  
- **Bing search integration**: Retrieves up to 50 pages per keyword.  
- **Result types**:  
  - *Organic* (standard Bing listings)  
  - *Sponsored* (paid ads)  
  - *Other* (direct answers, info boxes, etc.)  
- **Domain filtering**:  
  - Excludes results from domains listed in `whitelist.txt`.  
  - Removes entries that have no valid domain.  
- **CSV output**:  
  - Each keyword generates its own CSV file.  
  - Uses UTF-8 encoding for accented characters.  
- **Robustness**:  
  - Retries for network requests (5 attempts, exponential backoff).  
  - Random delay to avoid blocking by Bing.

---

## Project Structure

- **BING-TRACKER/**  
  - `bing_tracker.py` — Main Python script  
  - `keywords.txt` — List of keywords (one per line)  
  - `whitelist.txt` — List of domains to exclude  
  - `README.md` — This file  

---

## Requirements

- **Python 3.6+** (tested up to 3.13)  
- **Dependencies**:  
  - `requests`  
  - `beautifulsoup4`
- Install them via:
  ```bash
  pip install requests beautifulsoup4
