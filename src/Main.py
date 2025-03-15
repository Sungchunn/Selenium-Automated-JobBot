import os
import time
import csv
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def scrape_jobs():

    # Load yaml file
    settings_path = os.path.join(os.getcwd(), "config", "jobs.yaml")
    with open(settings_path, "r") as f:
        config = yaml.safe_load(f)

    driver_path = config["chrome_driver_path"]
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    jobs_data = []

    # Loop through each job sites listed in the yaml file
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
            try:
                title = card.find_element(By.CSS_SELECTOR, job_title_selector).text
            except:
                title = "N/A"

            try:
                company = card.find_element(By.CSS_SELECTOR, job_company_selector).text
            except:
                company = "N/A"

            try:
                link = card.find_element(By.CSS_SELECTOR, job_link_selector).get_attribute("href")
            except:
                link = "N/A"

            jobs_data.append({
                "title": title,
                "company": company,
                "link": link,
                "source": board["name"]
            })

    driver.quit()

    # Output result to .scv
    data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "job_listings.csv")

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["title", "company", "link", "source"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(jobs_data)

    print(f"Scraped {len(jobs_data)} new jobs. Data saved to {csv_path}")


if __name__ == "__main__":
    scrape_jobs()