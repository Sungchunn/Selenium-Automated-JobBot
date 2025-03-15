import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

# Google Chrome requires a ChromeDriver to execute
driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver-mac-arm64", "chromedriver")
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service) # Google Chrome webdriver
# driver_safari = webdriver.Safari()  # safari has built-in webdriver

driver.get("https://www.google.com")
input_element = driver.find_element(By.CLASS_NAME, "") # taps into HTML files and finds the CLASS attribute
input_element.send_keys("" + Keys.ENTER) # Scaling locally would be problematic with this appraoch


time.sleep(10)
driver.quit()