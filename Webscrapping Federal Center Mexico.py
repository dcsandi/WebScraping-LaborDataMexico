#!/usr/bin/env python
# coding: utf-8

# # Install

# In[3]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.firefox import GeckoDriverManager
import time


# ## Set up the Selenium driver for Firefox

# In[ ]:


driver = webdriver.Firefox()


# ## Initial URL

# In[ ]:


url = 'https://centrolaboral.gob.mx/listado-cct-nuevos-reforma/'
driver.get(url)

all_data = []

for _ in range(75):  # Assuming there are 75 pages, adjust as necessary
    # Wait for the data table to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'iddatatable')))
    
    


# ## Extract the HTML of the current page and process it with BeautifulSoup   
# 

# In[ ]:


soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find(id='iddatatable')
    rows = table.find_all('tr')
    
    for row in rows[1:]:  # Exclude the header row
        columns = row.find_all('td')
        row_data = [col.text for col in columns[:5]]  # Assuming you only want the first 5 columns
        all_data.append(row_data)   
    


# ## Try to simulate user interaction to click on "Next"
#    

# In[ ]:


next_button = driver.find_element(By.XPATH, "//a[@class='page-link' and text()='Siguiente']")
   driver.execute_script("arguments[0].scrollIntoView();", next_button)
   time.sleep(1)  # Wait for a second
   next_button.send_keys(Keys.ENTER)
   time.sleep(2)  # Wait two seconds for the page to load

driver.quit()



# ## Convert the data to a DataFrame and save to Excel

# In[ ]:


df = pd.DataFrame(all_data, columns=['Col1', 'Col2', 'Col3', 'Col4', 'Col5'])  # Adjust column names as needed
df.to_excel("datos6.xlsx", index=False, engine='openpyxl')

