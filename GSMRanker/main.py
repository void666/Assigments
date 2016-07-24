import requests
from bs4 import BeautifulSoup
import urllib
import json
import re

__author__ = 'Sushim'


class Phone:
    name = ''
    memory = ''
    camera = ''
    battery = ''
    ram = ''
    price = ''
    image = ''

    def print(self):
        """
        Print function for Phone class
        """
        print('Name:', self.name)
        print('Camera:', self.camera)
        print('Memory:', self.memory)
        print('Ram:', self.ram)
        print('Price:', self.price)
        print('Image:', self.image)

    def __init__(self):
        return


def getLinkstoBrands(url):
    """
    function gets the links to all the brands
    from the marker page of the website
    :param url: string,
    :return: dictionary of brandnames, values as links to their all display section
    """
    brandUrls = {}
    try:
        print("Maker link being crawled  : ", url)
        request = requests.get(url)
        if request.status_code == 200:
            sourceCode = BeautifulSoup(request.text, "html.parser")
            for td in sourceCode.findAll('td'):
                link = td.find('a', href=True)
                title = td.get_text()
                url = processUrl(link['href'])
                if title not in brandUrls.keys():
                    brandUrls[title] = url
                    print(title, ' ', url)
        else:
            print('no table or row found ')
    except requests.HTTPError as e:
        print('Unable to open url', e)
    return brandUrls


def getLinksToPhonesPerBrands(url):
    """
    function to return all phone's urls for a particular brand
    :param url: url of brand
    :return: dictionary of phones, links to phones as values
    """
    urls = {}
    print("brand link being scrapped : ", url)
    try:
        request = requests.get(url)
        if request.status_code == 200:
            sourceCode = BeautifulSoup(request.content, "html.parser")
            li = sourceCode.select('#review-body div > ul > li > a')
            for link in li:
                title = link.get_text()
                url = processUrl(link['href'])
                if title not in urls.keys():
                    urls[title] = url
                    print(title, ' ', url)
        else:
            print('no table or row found ')
    except requests.HTTPError as e:
        print('Unable to open url', e)
    return urls


def getPhoneStats(url):
    """
    function to extract phone details from each phone page
    :param url: string, url of the phone's page.
    :return: Phone type object, with mem, camera, ram and price details
    """
    p = Phone()
    try:
        request = requests.get(url)
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, "html.parser")
            p.ram = get_ram(soup)
            p.memory = get_memory(soup)
            p.image = get_image(soup)
            for table in soup.findAll("table"):
                header = table.th.get_text()
                if header == 'Camera':
                    p.camera = get_camera(table)
                if header == 'Battery':
                    p.battery = get_battery(table)
                if header == 'Misc':
                    p.price = get_price(table)
        else:
            print('unable to connect ')
    except requests.HTTPError as e:
        print('Unable to open url', e)
    return p


def processUrl(url):
    """
    function to create complete processable url
    :param url: string, url
    :return: string, finished url
    """
    domain = 'http://www.gsmarena.com/'
    if domain not in url:
        url = urllib.parse.urljoin(domain, url)
    return url


def get_ram(soup):
    """
    function to extract ram details from the page HTML text
    :param soup: BeautifulSoup object, (contains page text)
    :return: ram, integer.
    """
    ram = soup.find("strong", {"class": "accent accent-expansion"})
    if len(ram):
        ram = re.findall(r'\d+\.*\d*', ram.get_text())
        if len(ram):
            ram = float(ram[0])
        else:
            ram = 0
    else:
        ram = 0
    return ram


def get_memory(soup):
    """
    function to extract memory details from the page HTML text
    :param soup: BeautifulSoup object, (contains page text)
    :return: memory, integer.
    """
    memory = soup.find_all("span", {"class": "specs-brief-accent"})
    if len(memory):
        memory = re.findall(r'\d+', memory[3].get_text())
        if len(memory):
            memory = int(memory[0])
        else:
            memory = 0
    else:
        memory = 0
    return memory


def get_camera(table):
    """
    function to extract camera details from the page HTML text
    :param table: table object from BeautifulSoup parse, (contains page text)
    :return: camera, integer.
    """
    camera = table.findAll("tr")[0].findAll("td")[1]
    if len(camera):
        camera = re.findall(r'\d+', camera.get_text())
        if len(camera):
            camera = int(camera[0])
        else:
            camera = 0
    else:
        camera = 0
    return camera


def get_battery(table):
    """
    function to extract battery details from the page HTML text
    :param table: table object from BeautifulSoup parse, (contains page text)
    :return: battery, integer.
    """

    battery = table.findAll("tr")[0].findAll("td")[1]

    if battery is not None:
        battery = re.search(r'\d+', battery.get_text())
        if battery is not None:
            battery = int(battery.group())
        else:
            battery = 0
    else:
        battery = 0
    return battery


def get_price(table):
    """
    function to extract price details from the page HTML text
    :param table: table object from BeautifulSoup parse, (contains page text)
    :return: price, integer.
    """
    price = table.find("span", {"class": "price"})
    if price is not None:
        price = re.search(r'\d+', price.get_text())
        if price is not None:
            price = int(price.group())
        else:
            price = 0
    else:
        price = 0
    return price


def get_image(soup):
    """
    function returns the image url of the phone
    :param soup: BeautifulSoup object
    :return: url of image for thumbnail
    """
    image = soup.find("div", {"class": "specs-photo-main"}).find('img')['src']
    return image


def writeToFile(jsonList):
    """
    function to write JSON objects to file.
    :param p: List of Json formatted Phone object
    """
    file = open("data.json", "w")
    file.write(json.dumps(jsonList, sort_keys=True, indent=4, separators=(',', ': ')))
    print("File written")


def toJson(p):
    """
    function to convert Phone object to JSON
    :param p:
    :return: json format data
    """
    data = {p.name: {'Memory': p.memory, 'Camera': p.camera, 'Battery': p.battery, 'Ram': p.ram, 'Price': p.price,
                     'Image url': p.image}}
    return data


if __name__ == '__main__':
    linksToBrands = getLinkstoBrands('http://www.gsmarena.com/makers.php3')
    jsonList = []
    for link in linksToBrands:
        phoneUrls = getLinksToPhonesPerBrands(linksToBrands[link])
        for links in phoneUrls:
            print(" Phone being scraped : ", links, ' : ', phoneUrls[links])
            p = getPhoneStats(phoneUrls[links])
            p.name = links
            jsonList.append(toJson(p))
    print("Writing to file")
    writeToFile(jsonList)
