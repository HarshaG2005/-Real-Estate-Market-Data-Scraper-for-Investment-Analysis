import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from link_scraper import all_page_urls
#setup
driver=webdriver.Chrome()
wait = WebDriverWait(driver, 10)
l_wait=WebDriverWait(driver,20)
details=[]
#main loop

for url in all_page_urls:
 
    driver.get(url)
    l_wait.until(EC.presence_of_element_located((By.TAG_NAME,"body")))
    print(f"Scraping data from:{url}")
    try:
       title_con=l_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.col.pt-2")))
       title=driver.find_element(By.TAG_NAME,"h1").text
       PRICE=driver.find_element(By.CSS_SELECTOR,"span.main_price.mb-3.mb-sm-0").text
       num_rooms=driver.find_element(By.XPATH,"//div[text()='Bedrooms']/following-sibling::div").text
       num_bathrooms=driver.find_element(By.XPATH,"//div[text()='Bathrooms/WCs']/following-sibling::div").text
       property_size=driver.find_element(By.XPATH,"//div[text()='Area of land']/following-sibling::div").text
       iframe_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
       google_map= iframe_element.get_attribute("src")
       details.append([title,PRICE,num_rooms,num_bathrooms,property_size,google_map])
    except (NoSuchElementException, TimeoutException):
        print(f"Could not find all details on {url}. Skipping.")
        continue
#saving data to csv file
try:
    with open("negombo_state.csv","w",encoding="utf-8",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["title","Property_price","Number_of_rooms","Number_of_Bathrooms","Property_size","Link_of_Location"])
        if details:
            writer.writerows(details)
    print("succesfully saved to negombo_state.csv")
except Exception as e:
    print(f"error writing to file:{e}")
finally:
    driver.quit()





