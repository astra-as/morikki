from bs4 import BeautifulSoup
import requests
import csv
import time

# URL of the page to scrape
url = "https://univ-journal.jp/daigakuin-list/"

# Initialize an empty list to store the data
universities = []

# Function to scrape data
def scrape_page(page_url):
    # Make an HTTP GET request to the URL
    response = requests.get(page_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all graduate school entries in the provided HTML
        graduate_school_entries = soup.select('.pt-cv-content-item')

        # Parse details of each graduate school
        for entry in graduate_school_entries:
            # Check if the necessary elements exist before accessing them
            title_element = entry.find('h4', class_='pt-cv-title')
            if title_element:
                name = title_element.get_text(strip=True)
            else:
                # If the title element is not found, skip to the next entry
                continue
            
            url_element = entry.find('a')
            entry_url = url_element['href'] if url_element else 'URL not found'
            
            departments_elements = entry.select('.pt-cv-ctf-list .pt-cv-ctf-column .pt-cv-ctf-value')
            departments_list = [dept.get_text(strip=True) for dept in departments_elements]
            
            location_element = entry.find('div', class_='pt-cv-meta-fields')
            location = location_element.get_text(strip=True) if location_element else 'Location not found'
            
            # Append the extracted details to the list
            universities.append({
                "Name": name,
                "URL": entry_url,
                "Departments": ', '.join(departments_list),
                "Location": location
            })

# Scrape the initial page
scrape_page(url)

# Define how many seconds to wait between requests
wait_time = 1

# Scrape additional pages
for i in range(1, 30):
    add_path = f"?_page={i}"
    next_url = url + add_path
    
    # Wait for a specified amount of time before making the next request
    time.sleep(wait_time)
    
    scrape_page(next_url)

# Define the path for the CSV file
csv_file_path = "./universities.csv"

# Write the scraped data to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'URL', 'Departments', 'Location']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for school in universities:
        writer.writerow(school)

print("CSVファイルが正常に保存されました。")
