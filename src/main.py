import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.plusvalia.com/terrenos-en-venta-en-quito-pagina-%s.html'
driver_path = '/Applications/chromedriver'

def read_page_content(page):
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
    
def extract_publish_time(element):
    e = element.find(attrs={'class': 'icon-g-fecha-publicado'})
    return "" if e is None else e.parent.text.strip()

def extract_finished(element):
    e = element.find(attrs={'class': 'icon-g-terminado'})
    return "" if e is None else e.parent.text.strip()

def extract_sales_date(element):
    e = element.find(attrs={'class': 'icon-g-fecha'})
    return "" if e is None else e.parent.text.strip()

def parse_item(item):
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

    return [name, location, price, area, publisher1, publisher2, publish_time, finished, sales_date]

def get_items_from_page(page_content):
    soup = BeautifulSoup(page_content, features="html.parser")
    page_items = []
    for item in soup.find_all(attrs={'class': 'posting-card'}):
        page_items.append(parse_item(item))
    return page_items

def get_items_from_website():
    items = []
    for i in range(1, 220):
        print('reading page %s'%(i))    
        page_content = read_page_content(i)
        items.extend(get_items_from_page(page_content))
    return items

print('get_items_from_website')
items = get_items_from_website()
df = pd.DataFrame(items)
df.columns = ["nombre", "sector", "precio", "area", "publicador1", "publicador2", "tiempo_publicacion", "finalizado", "fecha_venta"]
df.to_csv('output/terrenos_quito.csv', index=False, header=True)
print('%s items written to csv'%(df.shape[0]))