import os
import time
import csv
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def safe_find_element_text(parent, by, selector, default="N/A"):
    try:
        return parent.find_element(by, selector).text
    except NoSuchElementException:
        return default

def safe_find_element_attr(parent, by, selector, attr, default="N/A"):
    try:
        return parent.find_element(by, selector).get_attribute(attr)
    except NoSuchElementException:
        return default

def save_jobs_to_csv(csv_path, jobs_data):
    # Check if CSV exists, read existing rows
    file_exists = os.path.isfile(csv_path)
    existing_links = set()
    if file_exists:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_links.add(row["link"])

    # Filter new jobs
    unique_jobs = []
    for job in jobs_data:
        if job["link"] not in existing_links:
            unique_jobs.append(job)

    # Append only unique jobs
    with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["title", "company", "link", "source"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(unique_jobs)

    print(f"Scraped {len(jobs_data)} new jobs, wrote {len(unique_jobs)} unique jobs.")

def scrape_jobs():
    # Load yaml file
    settings_path = os.path.join(os.getcwd(), "config", "jobs.yaml")
    with open(settings_path, "r") as f:
        config = yaml.safe_load(f)

    driver_path = config["chrome_driver_path"]
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    jobs_data = []

    # Loop through each job site listed in the yaml file
    for board in config["job_boards"]:
        search_url = board["search_url"]
        driver.get(search_url)
        time.sleep(3)

        job_card_selector = board["job_card_selector"]
        job_title_selector = board["job_title_selector"]
        job_company_selector = board["job_company_selector"]
        job_link_selector = board["job_link_selector"]

        job_cards = driver.find_elements(By.CSS_SELECTOR, job_card_selector)

        for card in job_cards:
            title = safe_find_element_text(card, By.CSS_SELECTOR, job_title_selector)
            company = safe_find_element_text(card, By.CSS_SELECTOR, job_company_selector)
            link = safe_find_element_attr(card, By.CSS_SELECTOR, job_link_selector, "href")

            jobs_data.append({
                "title": title,
                "company": company,
                "link": link,
                "source": board["name"]
            })

    driver.quit()
    data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "job_listings.csv")

    save_jobs_to_csv(csv_path, jobs_data)

if __name__ == "__main__":
    scrape_jobs()