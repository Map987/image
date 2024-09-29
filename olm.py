
import requests
from bs4 import BeautifulSoup
import json
import os

# URL of the website
url = "https://www.olm.co.jp/works"

# Fetching the content of the website
response = requests.get(url)
response_content = response.content

# Parsing the content using BeautifulSoup
soup = BeautifulSoup(response_content, 'html.parser')

# Find the script tag containing the JSON data
script_tag = soup.find('script', type='application/json', id='wix-warmup-data')
json_data = script_tag.string

# Parse the JSON data
try:
    data = json.loads(json_data)
except json.JSONDecodeError:
    print("Error decoding JSON data.")
    exit()

# Function to extract poster URLs
def extract_poster_urls(data):
    poster_urls = []

    # Traverse the data to find poster URLs
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'posters' and isinstance(value, str):
                poster_urls.append(value)
            elif isinstance(value, (dict, list)):
                poster_urls.extend(extract_poster_urls(value))
    elif isinstance(data, list):
        for item in data:
            poster_urls.extend(extract_poster_urls(item))

    return poster_urls

# Extract the poster URLs
poster_urls = extract_poster_urls(data)

# Write the poster URLs to a text file
output_folder = 'olm.co.jp'
output_file = os.path.join(output_folder, 'poster_urls.txt')

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)


def write_unique_urls_to_file(poster_urls, output_file):
    """
    Write unique poster URLs to a file, skipping any URLs that already exist in the file.

    :param poster_urls: List of poster URLs to write.
    :param output_file: File where URLs will be written.
    """
    existing_urls = set()

    # Check if the file exists and read existing URLs
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            for line in file:
                existing_urls.add(line.strip())

    # Write only new URLs to the file
    with open(output_file, 'a') as file:
        for poster_url in poster_urls:
            # Assuming the URL is in the format: "https://static.wixstatic.com/media/..."
            # We need to unquote it
            unquoted_url = requests.utils.unquote(poster_url)
            if unquoted_url not in existing_urls:
                file.write(unquoted_url + '\n')
                print(f"Added {unquoted_url} to {output_file}")
            else:
                print(f"Skipped {unquoted_url}, already exists in {output_file}")

write_unique_urls_to_file(poster_urls, output_file)
# Output the number of poster URLs found

print(f"{len(poster_urls)} poster URLs found and written to {output_file}")


import requests
import os
import re


import requests
import os
import re

def download_images(poster_urls, folder):
    """
    Download images from the given URLs and save them to the specified folder
    if they don't already exist.

    :param poster_urls: List of poster URLs to download.
    :param folder: Folder where images will be saved.
    """
    os.makedirs(folder, exist_ok=True)

    for url in poster_urls:
        # Extract the main part of the URL using regex
        match = re.search(r'wix:image:\/\/v1\/(.*?~mv2\.(jpg|png|webp|tif|tiff|psd|bmp|jpeg))', url)
        if match:
            image_name = match.group(1)
            full_url = f"https://static.wixstatic.com/media/{image_name}"
            image_path = os.path.join(folder, image_name)

            # Check if the file already exists
            if not os.path.exists(image_path):
                try:
                    response = requests.get(full_url)
                    response.raise_for_status()  # Check for request errors

                    with open(image_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded {image_name}")
                except requests.RequestException as e:
                    print(f"Could not download {full_url}. Reason: {e}")
            else:
                print(f"Skipped {image_name}, file already exists.")
def ok():
    # URL of the website
    url = "https://www.olm.co.jp/works"

    # Fetching the content of the website and parsing JSON data
    # ... (The previous code for fetching and parsing the website)

    # Extract the poster URLs
  #  poster_urls = extract_poster_urls(data)

    # Download the images
    download_images(poster_urls, 'olm.co.jp')


ok()
