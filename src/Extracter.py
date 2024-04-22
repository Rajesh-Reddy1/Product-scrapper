from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from collections import OrderedDict

import urllib
import pandas as pd
import numpy as np

# elements for extracting

Dict={'M_Site_Name_class':"RHJRod",
        'L_Site_Name_class':"zPEcBd.LnPkof",
        'L_Product':"pymv4e",
        'L_Price':"qptdjc",
        'Info_Class':"gWeIWe.V4Wd4b",
        'Price_Xpath':"//div[@class='bLrxoe']/span",
        'Site_Link_Class':"P9159d.hMk97e.BbI1ub"}



class Scraper:
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
        self.query = None
        self.url = None


    
    def set_query(self, query):
        self.query = urllib.parse.quote_plus(query)
        self.url = "https://www.google.co.uk/search?q=" + self.query
    
    def get_site_elements(self, class_name):
        return self.driver.find_elements(by=By.ID, value=class_name)
    
    def get_price_elements(self, xpath):
        return self.driver.find_elements(by=By.XPATH, value=xpath)
    
    def get_website_elements(self, class_name):
        return self.driver.find_elements(by=By.CLASS_NAME, value=class_name)
    
    def scrape(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(1)

        try:
            site = self.get_website_elements(Dict['M_Site_Name_class'])
            info = self.get_website_elements(Dict['Info_Class'])
            price = self.get_price_elements(Dict['Price_Xpath'])
            website = self.get_website_elements(Dict['Site_Link_Class'])
        except NoSuchElementException:
            print("Error: Element not found. Check CSS selectors/XPaths.")
            self.driver.quit()
            return None 


        site_name = [i.get_attribute("innerHTML") for i in site]
        Product_info = [i.get_attribute("innerHTML") for i in info]
        Price = [i.get_attribute("innerHTML") for i in price]
        link = [i.get_attribute("href") for i in website]
        linki = list(OrderedDict.fromkeys(link))
        b=linki

        table = pd.DataFrame({'Site_Name': site_name, 'Product': Product_info, 'Price': Price, 'Site_Link':b })
        result1 = table.drop_duplicates(subset=['Product','Site_Name','Price'])
        
        site_info_elements = self.get_website_elements(Dict['L_Site_Name_class'])
        site_info_list = [element.get_attribute("innerHTML") for element in site_info_elements]

        product_name_elements = self.get_website_elements(Dict['L_Product'])
        
        product_name_list = []
        site_link_list = []
        for element in product_name_elements:
            name = element.get_attribute("innerHTML")
            if name not in product_name_list:
                product_name_list.append(name)
        
        price_elements = self.get_website_elements(Dict['L_Price'])
        price_list = [element.get_attribute("innerHTML") for element in price_elements]
        price_list=price_list[:len(product_name_list)]
        site_link_list=site_link_list[:len(product_name_list)]
        site_info_list=site_info_list[:len(product_name_list)]
        
        for i in range(0, len(product_name_list)):
            id_name = "vplap" + str(i)
            site_elements = self.get_site_elements(id_name)
            links = [element.get_attribute("href") for element in site_elements]

        # Check if links is empty before accessing index 0
            if links:
                site_link_list.append(links[0])
        
        table = pd.DataFrame({
            'Site_Name': site_name,
            'Product': Product_info,
            'Price': Price,
            'Site_Link': b  
        })

        # Create a new column with HTML anchor tags for clickable links
        table['Link'] = table['Site_Link'].apply(lambda url: f'<a href="{url}">Visit Link</a>')

        # Drop the original 'Site_Link' column
        table = table.drop('Site_Link', axis=1)
        
        result = table.drop_duplicates(subset=['Site_Name','Product','Price'])
        result2 = pd.concat([result, result1], ignore_index=True)
        res=result2.sort_values(by=['Price'],ignore_index=True)
        res.index = np.arange(1, len(result2) + 1)
        res = f'''
        <head>
    <title>Product Search</title>
    <link rel="stylesheet" href="./style.css" />
    </head>
    <body>
    <h1>Product Search Results</h1>

    <div id="table-container"></div>
    {table.to_html(escape=False)} 
    </body>
'''
    
        return res
    
    def close(self):
        self.driver.quit()