from bs4 import BeautifulSoup
import time,requests


class Scraper:
    
    def __init__(self):
        self.url = "https://www.scrapethissite.com/pages/forms/"
        self.base_url = "https://www.scrapethissite.com"
        self.csvFile = open("hockey.csv","w")
        self.headerWritten = False
        self.getPageLinks()

    def parseUrl(self,href):
        """Creates a url with received href text"""
        url = self.base_url + href
        return url

    def open(self,url):
        """Opens a url"""
        response = requests.get(url)
        return response.text

    def bs(self,response):
        """Creates and returns a beautifulsoup object from a received response variable"""
        bs = BeautifulSoup(response,"html.parser")
        return bs

    def getPageLinks(self):
        """Scraping Actions"""
        response = self.open(self.url)
        bs = self.bs(response)

        """ GET ALL PAGE LINKS/URLS"""
        divs = bs.findAll("div",{"class":"col-md-10 text-center"})
        links = [li.find("a") for li in divs[0].findAll("li")]
        hrefs = [a['href'] for a in links]
        
        #During production, page number 1 appears twice so this condition aims to remove the extra link to page 1
        if hrefs[0] == hrefs[-1]:
            hrefs.pop(-1)
        else:
            pass
    
        pages = [self.parseUrl(href) for href in hrefs]
        print("bonaBOT has started scraping......")
        for page in pages:
            html = self.open(page)
            bs = self.bs(html)
            self.scrapeTableData(bs)
        self.csvFile.close()
        print("bonaBOT finished running.......")
        print("Scraped Data saved to Csv file in current working directory")

    def scrapeTableData(self,bs):
        """Scrape data from table on a given beautifulsoup object"""
        table = bs.find("table",{"class":"table"})
        table_headers = [header.text.strip() for header in table.findAll("th")]
        self.writeCsv(table_headers)
        table_data = [tr.findAll("td") for tr in table.findAll("tr",{"class":"team"})]
        data = [[td.text.strip() for td in each_row_data] for each_row_data in table_data]
        self.writeCsv(data)

    def writeCsv(self,data):
        if type(data[0]) != list:       # Table Header Data
            if self.headerWritten:
                pass
            else:        
                writeValue = ",".join(data) + "\n"
                self.csvFile.write(writeValue)
                self.headerWritten = True

        elif type(data[0]) == list:     # Table Row Data
            for d in data:
                value = ",".join(d) + "\n"
                self.csvFile.write(value)
                
Scraper()
