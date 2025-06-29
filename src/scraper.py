import requests
import os

def scrape_html(url, output_dir):
    """
    Fetches HTML content from a given URL and saves it to a specified directory.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Extract filename from URL or use a default
        filename = url.split('/')[-1]
        if not filename or not filename.endswith('.html'):
            filename = "index.html" # Default filename if not clear from URL

        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Successfully scraped {url} to {filepath}")
        return filepath
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with actual URLs and output directory)
    # This part will likely be driven by configuration or a main script
    output_raw_dir = "data/raw"
    os.makedirs(output_raw_dir, exist_ok=True)

    # Placeholder URLs - these should be replaced with actual target URLs
    # For a real project, these URLs would likely come from a configuration file
    # or be passed as arguments.
    target_urls = [
        "http://example.com/page1.html",
        "http://example.com/page2.html"
    ]

    for url in target_urls:
        scrape_html(url, output_raw_dir)