import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

url = 'https://www.plusvalia.com/terrenos-en-venta-en-quito-pagina-%s.html'

driver_path = '/Applications/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)

print("vamos ahi")
for i in range(1, 2):
    print(i)
    
    driver.get(url%(i))
    time.sleep(15)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    j = 0    
    for element in soup.find_all(attrs={'class': 'posting-card'}):
        j+=1

        price_element = element.find(attrs={'class': 'first-price'})
        price = price_element['data-price']
        
        info_element = element.find(attrs={'class': 'posting-info'})

        title_element = info_element.find(attrs={'class': 'posting-title'})
        title = title_element.a['href']

        location_element = info_element.find(attrs={'class': 'posting-location'})
        location = location_element.value

        print("%s,%s,%s,%s"%(j,title, location, price))

driver.quit()


