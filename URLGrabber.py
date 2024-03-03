import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
def get_urls_from_page(url, visited_urls=set()):
    try:
        # Check if the URL has already been visited to avoid duplicates
        if url in visited_urls:
            return []
        # Send a GET request to the specified URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # List of HTML tags containing URLs
        url_tags = ['a', 'img', 'script', 'link', 'iframe']
        # Extract the URLs from specified tags
        extracted_urls = []
        for tag in url_tags:
            elements = soup.find_all(tag, href=True) if tag != 'script' else soup.find_all(tag, src=True)
            for element in elements:
                # Use urljoin to handle relative URLs
                extracted_url = urljoin(response.url, element.get('href') if tag != 'script' else element.get('src'))

                extracted_urls.append(extracted_url)
        # Mark the current URL as visited
        visited_urls.add(url)
        return extracted_urls
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
def save_urls_to_file(urls, output_file):
    with open(output_file, 'a') as file:
        for url in urls:
            file.write(url + '\n')
if __name__ == "__main__":
    # Check if a URL and output file are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python URLGrabber.py <URL> <output_file>")
        sys.exit(1)
    url = sys.argv[1]
    output_file = sys.argv[2]
    visited_urls = set()
    all_urls = []
    # Initial execution
    extracted_urls = get_urls_from_page(url, visited_urls)
    all_urls.extend(extracted_urls)
    # Re-execute the script for each extracted URL
    for extracted_url in extracted_urls:
        try:
            print(f"{extracted_url}")
            extracted_urls = get_urls_from_page(extracted_url, visited_urls)
            all_urls.extend(extracted_urls)
        except Exception as e:
            print(f"Error while processing {extracted_url}: {e}")
    # Remove duplicates and save to the output file
    unique_urls = list(set(all_urls))
    save_urls_to_file(unique_urls, output_file)
