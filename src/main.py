from os import name
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.plusvalia.com/terrenos-en-venta-en-quito-pagina-%s.html'
driver_path = '/Applications/chromedriver'

def read_content(page):
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url%(page))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "react-paging")))
    content = driver.page_source
    driver.quit()
    return content

def read_file():
    f = open("page.html", "r")
    return f.read()

def extract_price(element):
    price_element = element.find(attrs={'class': 'first-price'})
    return price_element['data-price']

def extract_name(element):
    return element.find(attrs={'class': 'posting-title'}).a.text.strip()

def extract_location(element):
    return element.find(attrs={'class': 'posting-location'}).span.text.strip()

def extract_area(element):
    return element.find(attrs={'class': 'main-features'}).find_all("li")[-1].b.text.strip().replace("\t", "").replace("\n", "")

def extract_publisher1(element):
    e = element.find_all(attrs={'class': 'posting-logo-container'})
    if not e:
        return ""
    value = e[0].img['data-src']
    return value[value.rindex("/"):]

def extract_publisher2(element):
    e = element.find_all(attrs={'class': 'posting-logo-container'})
    if not e:
        return ""
    value = e[-1].img['data-src']
    return value[value.rindex("/"):]
    
def extract_publish_date(element):
    e = element.find(attrs={'class': 'icon-g-fecha-publicado'})
    return "" if e is None else e.parent.text.strip()

def extract_finished(element):
    e = element.find(attrs={'class': 'icon-g-terminado'})
    return "" if e is None else e.parent.text.strip()

def extract_sales_date(element):
    e = element.find(attrs={'class': 'icon-g-fecha'})
    return "" if e is None else e.parent.text.strip()

j = 0    
for i in range(1, 20):    
    content = read_content(i)
    # content = read_file()

    soup = BeautifulSoup(content, features="html.parser")

    for item in soup.find_all(attrs={'class': 'posting-card'}):
        j+=1
        price = extract_price(item)

        info_element = item.find(attrs={'class': 'posting-info'})
        name = extract_name(info_element)
        location = extract_location(info_element)
        area = extract_area(info_element)
        publisher1 = extract_publisher1(info_element)
        publisher2 = extract_publisher2(info_element)
        
        features_element = item.find(attrs={'class': 'posting-features'})
        publish_date = extract_publish_date(features_element)
        finished = extract_finished(features_element)
        sales_date = extract_sales_date(features_element)

        print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"%(j,name, location, price, area, publisher1, publisher2, publish_date, finished, sales_date))


    


