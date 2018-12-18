import os
import os.path
import urllib.request
from pyunpack import Archive
import inspect

input("Press <Enter> to start scraping.")
url_cat = 'https://www.tokopedia.com/p/dapur/food-drink-maker/coffee-tea-maker?ob=8&floc=5573&pmax=1000000&pmin=100000'
url_sto = 'https://www.tokopedia.com/ottencoffee?sort=8'
search_key_word = 'tupperware'
link_chrome = 'http://chromedriver.storage.googleapis.com/2.9/chromedriver_win32.zip'
z = 1
if not (os.path.exists('c:\scraping')):
    path = "c:\scraping"
    os.mkdir(path)
if not (os.path.exists('c:\scraping\image')):
    path = "c:\scraping\image"
    os.mkdir(path)
if not (os.path.isfile("C:\scraping\chromedriver.exe")):
    urllib.request.urlretrieve(link_chrome, "chromedriver_win32.zip")
    path1 = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    pat = path1 + '\\chromedriver_win32.zip'
    Archive(pat).extractall('C:\scraping')


def scrap_category(url_category):
    import csv

    img_link = []
    weight_list = []
    price_list = []
    name_list = []
    description_list = []
    print('Scraping based on category...')
    for k in get_product_link_based_on_category(url_category):
        feature_product(k, name_list, weight_list, price_list, description_list, img_link)
    print('Downloading images')
    for imglink in img_link:
        for im in imglink:
            x = len(im) - 1
            s = ''
            v = ''
            while not (im[x] == '/'):
                s += str(im[x])
                x -= 1
            for t in range(len(s) - 1, -1, -1):
                v += s[t]
            pt = "c:\scraping\image\\" + v
            urllib.request.urlretrieve(im, pt)
    print('Storing in data_scraping_category.csv')
    with open('c:\scraping\data_scraping_category.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([get_product_link_based_on_category(url_category)])
        filewriter.writerow([name_list])
        filewriter.writerow([weight_list])
        filewriter.writerow([price_list])
        filewriter.writerow([description_list])
        filewriter.writerow([img_link])


def scrap_store(url_store):
    global z
    import csv

    img_link = []
    weight_list = []
    price_list = []
    name_list = []
    description_list = []
    print('Scraping based on store...')
    for i in get_product_link_based_on_store(url_store):
        feature_product(i, name_list, weight_list, price_list, description_list, img_link)
    print('Downloading images')
    for imglink in img_link:
        for im in imglink:
            x = len(im) - 1
            s = ''
            v = ''
            while not (im[x] == '/'):
                s += str(im[x])
                x -= 1
            for t in range(len(s) - 1, -1, -1):
                v += s[t]
            pt = "c:\scraping\image\\" + v
            urllib.request.urlretrieve(im, pt)
    print('Storing in data_scraping_store.csv')
    with open('c:\scraping\data_scraping_store.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(get_product_link_based_on_store(url_store))
        filewriter.writerow(name_list)
        filewriter.writerow(weight_list)
        filewriter.writerow(price_list)
        filewriter.writerow(description_list)
        filewriter.writerow(img_link)


def scrap_search_word(search_word):
    global z
    import csv

    img_link = []
    weight_list = []
    price_list = []
    name_list = []
    description_list = []
    print('Scraping based on search...')
    for j in get_product_link_based_on_search(search_word):
        feature_product(j, name_list, weight_list, price_list, description_list, img_link)
    print('Downloading images')
    for imglink in img_link:
        for im in imglink:
            x = len(im) - 1
            s = ''
            v = ''
            while not (im[x] == '/'):
                s += str(im[x])
                x -= 1
            for t in range(len(s) - 1, -1, -1):
                v += s[t]
            pt = "c:\scraping\image\\" + v
            urllib.request.urlretrieve(im, pt)
    print('Storing in data_scraping_search.csv')
    with open('c:\scraping\data_scraping_search.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(get_product_link_based_on_search(search_word))
        filewriter.writerow(name_list)
        filewriter.writerow(weight_list)
        filewriter.writerow(price_list)
        filewriter.writerow(description_list)
        filewriter.writerow(img_link)


def get_product_link_based_on_store(url3):
    global webdriver, WebDriverWait, EC
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    browser = webdriver.Chrome("C:\\scraping\\chromedriver.exe")
    browser.implicitly_wait(10)
    browser.get(url3)
    delay = 15  # seconds
    try:
        element_present = EC.presence_of_element_located(("xpath", '//*[@id="showcase-container"]/div/div[1]/a'))
        WebDriverWait(browser, delay).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    list_link = []
    for i in range(1, 21):
        xpath = '//*[@id="showcase-container"]/div/div[' + str(i) + ']/a'
        link = browser.find_elements_by_xpath(xpath)
        list_link.append(link[0].get_attribute('href'))
    return list_link


def get_product_link_based_on_search(search):
    global webdriver, WebDriverWait, EC
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    nb_prod = nb_product_search(search)
    nb_page = int(nb_prod / 25)
    nb_page += 2
    list_link = []
    for p in range(1, 2):
        browser = webdriver.Chrome("C:\\scraping\\chromedriver.exe")
        browser.implicitly_wait(10)
        url = 'https://www.tokopedia.com/search?st=product&q=' + str(
            search) + '&unique_id=74cd661ecdab472c964fc41b60c61e50&page=' + str(p)
        browser.get(url)
        delay = 20  # seconds
        try:
            element_present = EC.presence_of_element_located(
                ("xpath", '//*[@id="content-directory"]/div[2]/div[1]/a/div[1]/img'))
            WebDriverWait(browser, delay).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        for i in range(1, 6):
            xpath = '//*[@id="promo-top-e-"]/div/div[2]/div[' + str(i) + ']/a[2]'
            link = browser.find_elements_by_xpath(xpath)
            list_link.append(link[0].get_attribute('href'))
        for i in range(1, 26):
            xpath = '//*[@id="content-directory"]/div[2]/div[' + str(i) + ']/a'
            link = browser.find_elements_by_xpath(xpath)
            list_link.append(link[0].get_attribute('href'))
        for i in range(1, 6):
            xpath = '//*[@id="product-results"]/div[3]/div/div[2]/div[' + str(i) + ']/a[2]'
            link = browser.find_elements_by_xpath(xpath)
            list_link.append(link[0].get_attribute('href'))
    return list_link


def nb_product_search(search):
    global url
    global webdriver, WebDriverWait, EC, TimeoutException, browser, delay, element_present, i, xpath, link, list_link
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    browser = webdriver.Chrome("C:\\scraping\\chromedriver.exe")
    browser.implicitly_wait(10)
    url = 'https://www.tokopedia.com/search?st=product&q=' + str(search)
    browser.get(url)
    delay = 25  # seconds
    try:
        element_present = EC.presence_of_element_located(("xpath", '//*[@id="content-directory"]/div[2]/div[16]'))
        WebDriverWait(browser, delay).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    xpath = '//*[@id="product-list-container"]/div/div[3]/div/div[1]/small/strong[2]'
    link = browser.find_elements_by_xpath(xpath)
    print(link[0].text)
    nbpage = link[0].text.replace(".", "")
    nbpage = float(nbpage)
    nb = int(nbpage)
    return nb


def feature_product(url2, name_list, weight_list, price_list, description_list, img_link):
    from bs4 import BeautifulSoup
    import urllib.request
    import time

    url_open = urllib.request.urlopen(url2)
    time.sleep(1)
    html_con = url_open.read()
    soup = BeautifulSoup(html_con, "html.parser")
    name = soup.findAll("a", {"itemprop": "name"})
    weight = soup.findAll("dd", {"class": "pull-left m-0"})
    price = soup.findAll("span", {"itemprop": "price"})
    desc = soup.findAll("p", {"itemprop": "description"})
    fg3 = soup.findAll("div", {"class": "jcarousel product-imagethumb-alt"})
    img = fg3[0].findAll("img", {"itemprop": "image"})
    img_src = []
    for i in img:
        img_src.append(i.get("src"))
    img_link.append(img_src)
    weight_list.append(weight[0].text)  # weight
    price_list.append(price[0].text)  # price
    name_list.append(name[0].text)  # name
    description_list.append(desc[0].text)  # deescription


def get_product_link_based_on_category(url1):
    global webdriver, WebDriverWait, EC
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    list_link = []
    for p in range(1, 2):
        browser = webdriver.Chrome("C:\\scraping\\chromedriver.exe")
        browser.implicitly_wait(10)
        browser.get(url1)
        delay = 20  # seconds
        try:
            element_present = EC.presence_of_element_located(
                ("xpath", '//*[@id="promo-top-e-1197"]/div/div[2]/div[1]/a[2]/div/div[1]/img'))
            WebDriverWait(browser, delay).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        for n in range(1, 6):
            xpath = '//*[@id="promo-top-e-1197"]/div/div[2]/div[' + str(n) + ']/a[2]'
            link = browser.find_elements_by_xpath(xpath)
            list_link.append(link[0].get_attribute('href'))
        for n in range(1, 26):
            xpath = '//*[@id="content-directory"]/div[2]/div[' + str(n) + ']/a'
            link = browser.find_elements_by_xpath(xpath)
            list_link.append(link[0].get_attribute('href'))
        for n in range(1, 6):
            xpath = '//*[@id="product-results"]/div[2]/div/div[2]/div[' + str(n) + ']/a[2]'
            link = browser.find_elements_by_xpath(xpath)
            list_link.append(link[0].get_attribute('href'))
    return list_link


scrap_store(url_sto)
scrap_search_word(search_key_word)
scrap_category(url_cat)
print("the data is stored at c:\scraping")
input("Press <Enter> to exit.")


