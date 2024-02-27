import argparse
from bs4 import BeautifulSoup as BS
import requests
import csv

def ReadCSV(path):
    file = open(path)
    reader = csv.reader(file)
    return reader

def GetUrl():
    pass

def Getinfo(ins):
    # Find all graduate school entries in the provided HTML
    graduate_school_entries = ins.select('.pt-cv-content-item')

    # Parse and print details of each graduate school
    for entry in graduate_school_entries:
        # Extracting the graduate school name
        name = entry.find('h4', class_='pt-cv-title').get_text(strip=True)
        
        # Extracting the research departments
        departments = entry.select('.pt-cv-ctf-list .pt-cv-ctf-column .pt-cv-ctf-value')
        departments_list = [dept.get_text(strip=True) for dept in departments]
        
        # Extracting the location (prefecture)
        location = entry.find('div', class_='pt-cv-meta-fields').get_text(strip=True)

    return name, entry.find('a')['href'], ', '.join(departments_list), location


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--urldic", default="universities.csv")
    parser.add_argument("-o", "--output", help="output path")
    args = parser.parse_args()

    url_dic = args.urldic
    url_list = ReadCSV(url_dic)


    for data in url_list:
        univ_name = data[0]
        url = data[1]
        univ_place = data[-1]


        res = requests.get(url)
        soup = BS(res.text, "html.parser")

        name, , 
                    

if __name__ == "__main__":
    main()