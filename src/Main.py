import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

# Google Chrome requires a ChromeDriver to execute
# driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver-mac-arm64", "chromedriver")
# service = Service(executable_path=driver_path)
# driver = webdriver.Chrome(service=service) # Google Chrome webdriver
driver_safari = webdriver.Safari()  # safari has built-in webdriver

driver_safari.get("https://www.google.com")
time.sleep(10)
driver_safari.quit()