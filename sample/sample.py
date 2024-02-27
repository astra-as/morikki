from bs4 import BeautifulSoup

# Load the sample HTML content from a file
file_path = './sample.html'

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all graduate school entries in the provided HTML
graduate_school_entries = soup.select('.pt-cv-content-item')

# Parse and print details of each graduate school
for entry in graduate_school_entries:
    # Extracting the graduate school name
    name = entry.find('h4', class_='pt-cv-title').get_text(strip=True)
    
    # Extracting the research departments
    departments = entry.select('.pt-cv-ctf-list .pt-cv-ctf-column .pt-cv-ctf-value')
    departments_list = [dept.get_text(strip=True) for dept in departments]
    
    # Extracting the location (prefecture)
    location = entry.find('div', class_='pt-cv-meta-fields').get_text(strip=True)
    
    print(f"Name: {name}")
    print(f"URL: {entry.find('a')['href']}")
    print(f"Departments: {', '.join(departments_list)}")
    print(f"Location: {location}")
    print("----------")