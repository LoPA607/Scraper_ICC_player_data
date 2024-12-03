import requests
from bs4 import BeautifulSoup

# Base URL of the player listing
base_url = "https://www.espncricinfo.com/cricketers"

# Sending a GET request to the page
response = requests.get(base_url)

# Checking if the request was successful (HTTP Status 200)
if response.status_code == 200:
    print("Successfully fetched the page")
else:
    print("Failed to fetch the page")
