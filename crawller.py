import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
from collections import deque
import services, models,schemas
from database import session_local, sql_engine, getdb
from sqlalchemy.orm import Session


base_url = "https://www.wikipedia.org"
all_html= requests.get(base_url)

image_count = 0
text_count = 0
def extract_everything(url):
    global image_count, text_count
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    base_url = url

    # Create folders
    folder_name_images = "downloaded_images"
    folder_name_text = "downloaded_texts"
    os.makedirs(folder_name_images, exist_ok=True)
    os.makedirs(folder_name_text, exist_ok=True)


    # --- Save images ---
    for img_tag in soup.find_all('img', src=True):
        img_src = img_tag['src']
        img_url = urljoin(base_url, img_src)

        try:
            img_response = requests.get(img_url, timeout=10)
            img = Image.open(BytesIO(img_response.content))
            width, height = img.size

            if width < 100 or height < 100:
                print(f"Skipped small image: {img_url} ({width}x{height})")
                continue

            file_name = os.path.join(folder_name_images, f"image_{image_count}.jpg")
            img.convert("RGB").save(file_name)
            print(f"Downloaded: image_{image_count}.jpg ({width}x{height})")
            image_count += 1

        except Exception as e:
            print(f"Failed to download or process {img_url}: {e}")

    # --- Extract and save text ---
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()  # Remove script and style tags

    text = soup.get_text(separator='\n')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_text = "\n".join(lines)
    file_name = os.path.join(folder_name_text, f"text_{text_count}.txt")
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(full_text)
        print(f"Text content saved to: {file_name}")
        text_count += 1
        
def extract_link(url):
    response = requests.get(url)
    content_html = BeautifulSoup(response.content, "html.parser")
    base_url = url  # base for resolving relative links
    links = []
    
    for a_tag in content_html.find_all('a', href=True):
        full_url = urljoin(base_url, a_tag['href'])
        links.append(full_url)
    
    return links

def bfs(start):
    visited_nodes = set()
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        
        if node in visited_nodes:
            continue
        
        visited_nodes.add(node)
        
        # Perform scraping
        extract_everything(node)
        
        # Get and enqueue children
        try:
            child_nodes = extract_link(node)
            for child in child_nodes:
                if child not in visited_nodes:
                    queue.append(child)
        except Exception as e:
            print(f"Failed to extract links from {node}: {e}")
    
    return visited_nodes

