# prérequis: pip3 install beautifulsoup4 requests

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import re
import csv
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter, Retry
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Function to read a file and return a list of non-empty lines
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Secure function to extract a link from an HTML element
def extract_link(element):
    link_tag = element.find('a')
    return link_tag['href'] if link_tag and 'href' in link_tag.attrs else 'No link'

# Function to sanitize keyword to create a valid filename
def sanitize_filename(keyword):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', keyword)

# Create a session with retry strategy
def create_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Function to perform Bing search and extract results with a limit of 50 pages
def search_bing(keyword, max_pages=50, delay_range=(1, 3)):
    print(f"🔍 Starting search for keyword: '{keyword}'", flush=True)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    session = create_session()
    results = []

    for page in range(max_pages):
        offset = page * 10
        url = f"https://www.bing.com/search?q={keyword}&first={offset}"
        print(f"➡️ Fetching page {page + 1} for '{keyword}'...", flush=True)

        try:
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ [ERROR] Failed to retrieve page {page + 1} for '{keyword}': {e}", flush=True)
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        organic_results = soup.find_all('li', class_='b_algo')
        sponsored_results = soup.find_all('li', class_='b_ad')
        other_results = soup.find_all('li', class_='b_ans')

        page_results_count = len(organic_results) + len(sponsored_results) + len(other_results)
        print(f"✅ Found {page_results_count} results on page {page + 1} for '{keyword}'.", flush=True)

        if page_results_count == 0:
            print(f"ℹ️ No more results found for '{keyword}'. Stopping search.", flush=True)
            break

        for item in organic_results:
            results.append(parse_result(item, keyword, 'Organic'))

        for ad_section in sponsored_results:
            results.append(parse_result(ad_section, keyword, 'Sponsored'))

        for other_section in other_results:
            results.append(parse_result(other_section, keyword, 'Other'))

        time.sleep(random.uniform(*delay_range))  # Randomized delay to avoid detection

    # Remove results without a valid domain
    filtered_results = [result for result in results if result['domain'] != 'no domain']
    removed_count = len(results) - len(filtered_results)

    if removed_count > 0:
        print(f"🗑️ Removed {removed_count} results without a valid domain for '{keyword}'.", flush=True)

    print(f"🏁 Completed search for '{keyword}' with {len(filtered_results)} valid results.\n", flush=True)
    return filtered_results

# Helper function to parse result items
def parse_result(item, keyword, result_type):
    title = item.find('h2')
    link = extract_link(item)
    description = item.find('p').text if item.find('p') else 'No description'
    domain = urlparse(link).netloc if link != 'No link' else 'no domain'
    return {
        'keyword': keyword,
        'result_type': result_type,
        'title': title.text.strip() if title else 'No title',
        'link': link,
        'domain': domain.lower(),
        'description': description.strip()
    }

# Function to write results to a CSV file
def write_results_to_csv(results, whitelist_domains, output_file):
    print(f"💾 Saving results to '{output_file}'...", flush=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Keyword', 'Result Type', 'Title', 'Link', 'Domain', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        saved_count = 0
        for result in results:
            if result['domain'] not in whitelist_domains:
                writer.writerow({
                    'Keyword': result['keyword'],
                    'Result Type': result['result_type'],
                    'Title': result['title'],
                    'Link': result['link'],
                    'Domain': result['domain'],
                    'Description': result['description']
                })
                saved_count += 1
    print(f"✅ Saved {saved_count} filtered results to '{output_file}'.", flush=True)

# Function to process a single keyword
def process_keyword(keyword, whitelist_domains):
    results = search_bing(keyword, max_pages=50)
    output_filename = f"{sanitize_filename(keyword)}.csv"
    write_results_to_csv(results, whitelist_domains, output_filename)
    print(f"🎉 Completed processing for '{keyword}'.\n", flush=True)

# Main function
def main():
    keywords = read_file('keywords.txt')
    whitelist_domains = set(domain.lower() for domain in read_file('whitelist.txt'))

    max_threads = min(10, len(keywords))  # Limit threads to avoid overload

    print(f"🚀 Starting search for {len(keywords)} keywords with up to {max_threads} concurrent threads.\n", flush=True)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(process_keyword, keyword, whitelist_domains) for keyword in keywords]

        for future in as_completed(futures):
            try:
                future.result()  # Ensure exceptions are caught
            except Exception as e:
                print(f"❌ [ERROR] {e}", flush=True)

    print("✅ All searches completed.", flush=True)

if __name__ == "__main__":
    main()
