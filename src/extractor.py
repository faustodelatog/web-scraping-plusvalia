from os import name
from bs4 import BeautifulSoup

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
    
def extract_publish_time(element):
    e = element.find(attrs={'class': 'icon-g-fecha-publicado'})
    return "" if e is None else e.parent.text.strip()

def extract_finished(element):
    e = element.find(attrs={'class': 'icon-g-terminado'})
    return "" if e is None else e.parent.text.strip()

def extract_sales_date(element):
    e = element.find(attrs={'class': 'icon-g-fecha'})
    return "" if e is None else e.parent.text.strip()

def item_to_row(item):
    price = extract_price(item)

    info_element = item.find(attrs={'class': 'posting-info'})
    name = extract_name(info_element)
    location = extract_location(info_element)
    area = extract_area(info_element)
    publisher1 = extract_publisher1(info_element)
    publisher2 = extract_publisher2(info_element)

    features_element = item.find(attrs={'class': 'posting-features'})
    publish_time = extract_publish_time(features_element)
    finished = extract_finished(features_element)
    sales_date = extract_sales_date(features_element)

    print("%s,%s,%s,%s,%s,%s,%s,%s,%s"%(name, location, price, area, publisher1, publisher2, publish_time, finished, sales_date))
