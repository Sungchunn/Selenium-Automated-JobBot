
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    TimeoutException
)

def auto_fill():
    # Validate ChromeDriver Path
    driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver-mac-arm64", "chromedriver")
    if not os.path.isfile(driver_path):
        print(f"[ERROR] ChromeDriver not found at {driver_path}")
        return

    # Attempt to initialize Selenium driver
    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service)
    except WebDriverException as e:
        print(f"[ERROR] Failed to initialize WebDriver: {e}")
        return

    # Check if job_listings.csv exists
    csv_path = os.path.join(os.getcwd(), "data", "job_listings.csv")
    if not os.path.isfile(csv_path):
        print(f"[WARNING] No job_listings.csv found. Please run scrape_jobs.py first.")
        driver.quit()
        return

    # Read CSV safely
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as e:
        print(f"[ERROR] Unable to read CSV: {e}")
        driver.quit()
        return

    if not rows:
        print("[INFO] No job listings found in job_listings.csv.")
        driver.quit()
        return

    job_to_apply = rows[-1]
    job_link = job_to_apply.get("link", "")
    if not job_link:
        print("[WARNING] This job entry has no link. Skipping.")
        driver.quit()
        return

    try:
        driver.get(job_link)
    except (WebDriverException, TimeoutException) as e:
        print(f"[ERROR] Failed to load job page ({job_link}): {e}")
        driver.quit()
        return

    time.sleep(5)

    try:
        driver.find_element(By.ID, "firstname").send_keys("Your Name")
        driver.find_element(By.ID, "lastname").send_keys("Last Name")
        driver.find_element(By.ID, "upload_resume").send_keys("/path/to/resume.pdf")
        driver.find_element(By.ID, "submit_button").click()

        print(f"[INFO] Applied for: {job_to_apply['title']} at {job_to_apply['company']}")
    except NoSuchElementException as e:
        print(f"[ERROR] Form element not found: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error filling form: {e}")

    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    auto_fill()