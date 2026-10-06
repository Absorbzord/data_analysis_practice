from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os

# 2a
driver = webdriver.Firefox()

driver.get("https://www.pap.pl")
accept_cookies = driver.find_element(By.XPATH, "//*[contains(text(), 'Akceptuję']")
accept_cookies.click()

# 2b
driver.maximize_window()

# 2c
language_switch = driver.find_element(By.XPATH, "//*[@title='English']")
language_switch.click()

# 2d
business_section = driver.find_element(By.LINK_TEXT, "Business")
business_section.click()

#2e
titles = [title.text for title in driver.find_elements(By.CSS_SELECTOR, ".article-title")]
print(titles)

# 2f
images = driver.find_elements(By.TAG_NAME, "img")
for idx, img in enumerate(images):
    src = img.get_attribute("src")
    if src:
        response = requests.get(src)
        with open(f"image_{idx}.jpg", "wb") as file:
            file.write(response.content)
print("Files saved!")

# 2g
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 2h
last_page_button = driver.find_element(By.LINK_TEXT, "Last")
last_page_button.click()

last_page_number = driver.find_element(By.CLASS_NAME, "page-number-class").text  # Adjust class
print("Last page number:", last_page_number)