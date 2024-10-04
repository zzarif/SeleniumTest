from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os


if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--window_size=1920,1080")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A172584&qid=1728010014&ref=sr_pg_1")
    data_dir = os.path.join(os.getcwd(), 'data', 'products.csv')

    all_products = []
    next_page_exists = True

    while next_page_exists:

        elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//div[@data-component-type="s-search-result"]')
        ))

        product_container = driver.find_element(By.CSS_SELECTOR, "div.s-main-slot.s-result-list.s-search-results.sg-row")
        products = product_container.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        for product in products:
            title = price = rating = img = "Not Found"

            try: title = product.find_element(By.CSS_SELECTOR, "h2 > a > span").text
            except: pass
            
            try: price = product.find_element(By.CLASS_NAME, "a-price").text.replace('\n', '.')
            except: pass

            # try: rating = product.find_element(By.CSS_SELECTOR, '//div[@data-cy="reviews-block"]') \
            #                     .find_element(By.TAG_NAME, "span").get_attribute("aria-label")
            # except: pass

            try: img = product.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
            except: pass

            all_products.append({ 
                "title": title, 
                "price": price, 
                # "rating": rating,
                "img": img
            })

            df = pd.DataFrame(data=all_products, columns=all_products[0].keys())
            df.to_csv(data_dir, index=False)

        next_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "s-pagination-next")
        ))
        next_page_exists = "disabled" not in next_btn.get_attribute("class")

        if next_page_exists:
            driver.find_element(By.CLASS_NAME, "s-pagination-next").click()
        print(len(all_products))

    # driver.quit()
