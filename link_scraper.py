import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
#SETUP
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.lankapropertyweb.com/")
wait = WebDriverWait(driver, 10)
l_wait=WebDriverWait(driver,20)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(10)
#CHECKBOX
try:
    property_type_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Property Type']]")))
    property_type_button.click()
    time.sleep(1)
    house_option = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox'][value='House']")
    if not house_option.is_selected():
         driver.execute_script("arguments[0].click();", house_option)
except TimeoutException:
    print("alert!error in checkbox")
finally:
    time.sleep(1)
#SEARCHING PROCESS
try:
        search_bar = wait.until(EC.element_to_be_clickable((By.ID, "searchbox")))
        search_bar.click()
        search_bar.clear()
        search_bar.send_keys("Negombo")
        print(f" Search bar value: '{search_bar.get_attribute('value')}'")
        time.sleep(2)
        first_suggestion = None
        try:
            dropdown = driver.find_element(By.XPATH, "//ul[contains(@class, 'typeahead')]")
            first_suggestion = dropdown.find_element(By.XPATH, ".//li[1]")
            print(f" Found first suggestion (typeahead): {first_suggestion.text}")
        except:
            pass
        if not first_suggestion:
            try:
                dropdown = driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu')]")
                first_suggestion = dropdown.find_element(By.XPATH, ".//a[1] | .//div[1] | .//li[1]")
                print(f" Found first suggestion (dropdown-menu): {first_suggestion.text}")
            except:
                pass
        if not first_suggestion:
            try:
                dropdown = driver.find_element(By.XPATH, "//*[contains(@class, 'tt-menu')]")
                first_suggestion = dropdown.find_element(By.XPATH, ".//*[contains(@class, 'tt-suggestion')][1]")
                print(f"Found first suggestion (tt-menu): {first_suggestion.text}")
            except:
                pass
        if not first_suggestion:
            print(" Using keyboard navigation as fallback...")
            search_bar.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            search_bar.send_keys(Keys.ENTER)
            print(" Used keyboard: DOWN + ENTER")
        else:
            
            suggestion_text = first_suggestion.text
            print(f"Clicking first suggestion: '{suggestion_text}'")
            
        
            try:
                first_suggestion.click()
                print("Direct click successful")
            except:
                driver.execute_script("arguments[0].click();", first_suggestion)
                print("JavaScript click successful")
        
        time.sleep(1)
        final_value = search_bar.get_attribute('value')
        print(f" Search bar after selection: '{final_value}'")
        
        search_button = wait.until(EC.element_to_be_clickable((By.ID, "searchBtn")))
        search_button.click()
        print("Search button clicked")
        time.sleep(2)
except TimeoutException:
    print("error in searching process")
#MAIN LOOP
all_page_urls = []
while True:
    
    current_page = driver.current_url
    print(f"Finding links on page: {current_page}")
    
    # 1. Wait for listings to be present on the current page
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.col")))
        #listings = driver.find_element(By.XPATH, '//div[@class="col"]/article[@class=listing-item]/a') 
        listings = driver.find_elements(By.XPATH, "//article[@class='listing-item']")
        
        # 2. Scrape the links from the current page
        for listing in listings:
            try:
                link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
                if link and link not in all_page_urls:
                    all_page_urls.append(link)
            except Exception:
                continue # Skip if there's any error with a single link

    except TimeoutException:
        print("Could not find listings on this page. Stopping.")
        break

    # 3. After scraping, find the "Next" button and try to click it
    try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next']")))
            driver.execute_script("arguments[0].click();", next_button)
            print("Navigating to next page...")
            time.sleep(3) 
    except (NoSuchElementException, TimeoutException):
            print("No more 'Next' button found. Scraping finished.")
            break 

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break

print(f"Finished collecting links. Found {len(all_page_urls)} total listings.")

        

        