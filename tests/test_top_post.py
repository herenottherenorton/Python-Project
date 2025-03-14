import json
import os
from playwright.sync_api import sync_playwright

def get_top_post():
    # Determine the absolute path to the config file
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    # Load the target URLs from the config file
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            urls = config["target_urls"]
    except (FileNotFoundError, KeyError) as e:
        print(f"Configuration error: {e}")
        return

    if not urls:
        print("No URLs found in the configuration.")
        return

    # Get the first URL
    url = urls[0]

    try:
        with sync_playwright() as playwright:
            # Launch browser
            browser = playwright.chromium.launch(headless=True)

            # Open a new page
            page = browser.new_page()

            # Navigate to the URL
            page.goto(url)

            # Extract the top post title (adjust selector based on page structure)
            top_post = page.locator(".post-title").first.inner_text()

            # Close the browser
            browser.close()

            print(f"Top post from {url}: {top_post}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_top_post()