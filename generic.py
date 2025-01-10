import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import hashlib
import re

# List of common image extensions
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def download_images_from_url(url, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all anchor tags (<a>) that contain images (<img>) and have an href attribute
        a_tags = soup.find_all('a', href=True)
        for a_tag in a_tags:
            img_tag = a_tag.find('img')
            if img_tag and img_tag.get('src'):
                img_url = a_tag['href']  # Use the href of the <a> tag (not the img src)
                
                # If the href URL points to a thumbnail, we modify it to point to the full-size image
                img_url = urljoin(url, img_url)  # Make it absolute if needed
                
                # If the image URL contains '_thumb', remove it to get the full-size image
                if '_thumb' in img_url:
                    img_url = img_url.replace('_thumb', '')
                
                # Ensure we are downloading an image (based on file extension)
                if img_url.endswith(IMAGE_EXTENSIONS):
                    download_image(img_url, url, output_directory)
    
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")

def generate_image_filename(url, img_url):
    # Create a hash of the URL to ensure unique filenames
    url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:8]  # Shorten the hash for the filename
    img_name = os.path.basename(img_url)
    
    # Ensure the image filename is valid (remove any special characters)
    img_name = re.sub(r'[^a-zA-Z0-9_\-.]', '_', img_name)
    
    # Prepend the hash to the image name
    return f"{url_hash}_{img_name}"

def download_image(img_url, url, output_directory):
    img_name = generate_image_filename(url, img_url)
    img_path = os.path.join(output_directory, img_name)
    
    if os.path.exists(img_path):
        print(f"Image already downloaded: {img_name}")
        return
    
    try:
        # Try downloading the image
        response = requests.get(img_url, headers=HEADERS, stream=True)
        response.raise_for_status()
        
        # Check if the image is downloaded correctly
        success = save_and_check_image(response, img_path)
        
        if not success:
            print(f"Retrying download for {img_name}")
            response = requests.get(img_url, headers=HEADERS, stream=True)  # Try again
            response.raise_for_status()
            save_and_check_image(response, img_path)  # Check again after retry
        
        print(f"Downloaded: {img_name}")
    
    except requests.RequestException as e:
        print(f"Failed to download {img_url}: {e}")

def save_and_check_image(response, img_path):
    # Save the image to the file
    with open(img_path, 'wb') as img_file:
        for chunk in response.iter_content(1024):
            img_file.write(chunk)
    
    # Verify if the image is valid
    try:
        with open(img_path, 'rb') as img_file:
            img = Image.open(img_file)
            img.verify()  # Verify that the image is not corrupted
        return True
    except (IOError, SyntaxError) as e:
        print(f"Corrupted image detected: {img_path}")
        os.remove(img_path)  # Remove the corrupted file
        return False

if __name__ == "__main__":
    url = input("Please enter the URL: ").strip()
    OUTPUT_DIRECTORY = "downloaded_images"
    
    download_images_from_url(url, OUTPUT_DIRECTORY)
