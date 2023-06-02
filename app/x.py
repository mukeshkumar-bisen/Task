import requests
from bs4 import BeautifulSoup

# Get the Pinterest board URL
board_url = "https://www.pinterest.com/board/my-board/"

# Make a request to the Pinterest URL
response = requests.get(board_url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, "html.parser")

# Find all the image tags in the HTML
images = soup.find_all("img")

# Get the src attribute of each image tag
image_urls = [image["src"] for image in images]

# Download the images
for image_url in image_urls:
    response = requests.get(image_url)
    with open(image_url.split("/")[-1], "wb") as f:
        f.write(response.content)