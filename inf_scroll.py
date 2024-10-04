from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--window_size=1920,1080")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    driver.get("https://intoli.com/blog/scrape-infinite-scroll/demo.html")
    data_dir = os.path.join(os.getcwd(), 'data', 'items.csv')

    all_items = []

    last_height = driver.execute_script("return document.body.scrollHeight")

    itemTargetCount = 100

    while itemTargetCount > len(all_items):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

        elements = driver.find_elements(By.CSS_SELECTOR, "#boxes > div")
        textElements = []
        for element in elements:
            textElements.append({
                "title": element.text
            })
        
        all_items = textElements

    df = pd.DataFrame(data=all_items, columns=all_items[0].keys())
    df.to_csv(data_dir, index=False)