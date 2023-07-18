import requests
import os,sys
import json
from bs4 import BeautifulSoup
from time import sleep
from PyPDF2 import PdfFileMerger
import glob

def scrape_content():
    url = "https://pages.cs.wisc.edu/~remzi/OSTEP/"

    content = ""
    with open("/Users/griffin/Dropbox/_Courses/5143-Operating-Systems/.trunk/scrape_book/source.html") as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    tds = soup.findAll("td")

    chapters = []

    for td in tds:
        childTag = td.find('small')
        if childTag:
            # do stuff
            page = td.small.text
            link = td.a["href"]
            if int(page) < 10:
                page = "0"+page
            chapters.append(f"{page}.{link}")

    chapters = sorted(chapters)

    for chapter in chapters:
        print(url+chapter[3:])
        print(chapter)
        response = requests.get(url+chapter[3:])
        with open(f"/Users/griffin/Dropbox/_Courses/5143-Operating-Systems/.trunk/scrape_book/chapters/{chapter}", 'wb') as f:
            f.write(response.content)
        sleep(.5)

def concat_chapters():
    pdfs = glob.glob("/Users/griffin/Dropbox/_Courses/5143-Operating-Systems/.trunk/scrape_book/chapters/*.pdf")
    pdfs = sorted(pdfs)

    merger = PdfFileMerger()

    for pdf in pdfs:
        print(pdf)
        merger.append(pdf)

    merger.write("99.ostep.pdf")
    merger.close()

if __name__=='__main__':
    concat_chapters()