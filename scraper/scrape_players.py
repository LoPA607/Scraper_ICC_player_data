import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL of the cricketers list page
base_url = "https://www.espncricinfo.com/cricketers"

# Send a GET request to fetch the page content
response = requests.get(base_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Successfully fetched the page!")
else:
    print("Failed to retrieve the page.")
    exit()

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all player profile URLs (links that start with /cricketers/)
player_links = soup.find_all('a', href=True, class_='ds-inline-flex')

# Extract player profile URLs and player names
player_data = []
for link in player_links:
    href = link['href']
    if href.startswith("/cricketers/"):
        player_name = link.get_text(strip=True)
        player_url = "https://www.espncricinfo.com" + href
        player_data.append((player_name, player_url))

# Print out all the player profile URLs
print("Found Player URLs:")
for name, url in player_data:
    print(f"{name}: {url}")

# Now, visit each player profile and scrape additional data
for player_name, player_url in player_data:
    print(f"\nScraping profile for {player_name} - {player_url}")

    # Send a GET request to the player's profile page
    player_response = requests.get(player_url)

    # Check if the request was successful (status code 200)
    if player_response.status_code != 200:
        print(f"Failed to retrieve profile for {player_name}")
        continue

    # Parse the player profile page
    player_soup = BeautifulSoup(player_response.content, 'html.parser')

    # Try to find the bio section
    bio_section = player_soup.find('div', class_='ci-player-bio-content')
    
    # If the bio section is found, extract the relevant data
    if bio_section:
        ipl_section = bio_section.find_all('p')  # Find all paragraphs within the bio section
        if ipl_section:
            player_bio = "\n".join([p.get_text(strip=True) for p in ipl_section])
        else:
            player_bio = "No detailed bio found."
    else:
        player_bio = "No bio section found."
    
    # Print the scraped bio (you can store it into CSV or process it as needed)
    print(f"Bio for {player_name}:\n{player_bio}\n")

    # Sleep to avoid making requests too quickly (you can adjust the delay)
    time.sleep(1)

    # Save to a CSV file or process the data as needed
    with open('player_profiles.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player_name, player_url, player_bio])
