import argparse
from bs4 import BeautifulSoup as BS
import requests
import csv
import re

def ReadCSV(path):
    file = open(path)
    reader = csv.reader(file)
    return reader

def GetUrl():
    pass


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-u", "--urldic", required=True)
    # parser.add_argument("-o", "--output", help="output path")
    # args = parser.parse_args()

    # url_dic = args.urldic
    # url_list = ReadCSV(url_dic)

    url_list = [["放送大学大学院","https://univ-journal.jp/daigakuin/73529/"]]


    for data in url_list:
        univ_name = data[0]
        url = data[1]

        res = requests.get(url)
        soup = BS(res.text, "html.parser")
        name = soup.find_all("div", {"class","post-single-content box mark-links"})[0]
        table = name.find_all("table")[0]
        td_ = table.find_all("td")
        td_list = []
        for td in td_:
            text = td.get_text(separator="<br/>")
            element = text.split("<br/>")
            td_list.append(element)
        print(td_list)
                    
    


if __name__ == "__main__":
    main()