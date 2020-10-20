import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://www.plusvalia.com/terrenos-en-venta-en-quito.html"
# url = "https://www.remax.com.ec/terrenos-de-venta-en-quito/"
# url = "https://www.properati.com.ec/quito/terreno/venta/1/"

driver_path = '/Applications/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get(url)
results = []
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
print(content)
driver.quit()


