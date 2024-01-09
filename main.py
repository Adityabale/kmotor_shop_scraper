import os
import time
import requests
import warnings
import pandas as pd

from pathlib import Path
from typing import Optional
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains


class KMotorShopScraper:
    main_page = 'https://www.kmotorshop.com/en/device/manu-car-list'

    def __init__(self):
        """ Initialize the webdriver"""
        self.driver: Optional[WebDriver] = None
        self.session = None

    def get_models_data(self):
        """Gets all the spare parts list for models from the main page."""
        model_count = 0
        # actions = ActionChains(self.driver)
        wait5s = WebDriverWait(self.driver, 5)
        dataframes = list()
        self.driver.get(self.main_page)
        self._click_accept_cookies()
        models_divs = wait5s.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".index__container > div")))
        while model_count < len(models_divs):
            try:
                for i, model_div in enumerate(models_divs):
                    models_divs = wait5s.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                    ".index__container > div")))
                    self._scroll_to(self.driver, models_divs[i])
                    time.sleep(2)
                    model_name = models_divs[i].find_element(By.TAG_NAME, 'h3').get_attribute('innerText').strip()
                    model_link = models_divs[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
                    self.driver.get(model_link)
                    time.sleep(2)
                    part_no_links = wait5s.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.searchtable a')))
                    for idx, link in enumerate(part_no_links):
                        part_no_links = wait5s.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                          'table.searchtable a')))
                        self._scroll_to(self.driver, part_no_links[idx])
                        time.sleep(2)
                        part_no = part_no_links[idx].get_attribute('innerText').strip()
                        self.driver.get(part_no_links[idx].get_attribute('href'))
                        time.sleep(2)
                        tables = pd.read_html(self.driver.page_source)
                        df = pd.DataFrame(tables[0])
                        df['Model'] = model_name
                        dataframes.append(df)
                        print(f"Done: {model_name}\t {part_no}")
                        self.driver.back()
                        time.sleep(2)
                    self.driver.back()
                    time.sleep(2)
                    model_count += 1
            except exceptions.TimeoutException:
                model_count += 1
        self._concat_get_csv(dataframes)

    def _scroll_to(self, driver: WebDriver, element: WebElement):
        """Scroll to the given WebElement.

        :param driver: WebDriver instance
        :param element: WebElement to scroll to
        """
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def _concat_get_csv(self, dataframes):
        """Merge all the dataframes to a single df. Save the complete file in csv format"""
        data = pd.concat(dataframes, ignore_index=True)
        data.to_csv(f'scraped-data/{datetime.strftime(datetime.now(), "%Y-%m-%d")}.csv')

    def _click_accept_cookies(self):
        """Clicks on the accept button for the cookies popup that appears."""
        wait5s = WebDriverWait(self.driver, 5)
        try:
            cookies_div = wait5s.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                       '[aria-labelledby="ch2-dialog-title"]')))
            accept_button = cookies_div.find_element(By.CSS_SELECTOR, 'button.ch2-allow-all-btn')
            accept_button.click()
        except exceptions.TimeoutException:
            pass


def main():
    CHROME_DRIVER = os.environ['CHROME_DRIVER_PATH']
    service = ChromeService(executable_path=CHROME_DRIVER)
    # chrome_options = ChromeOptions()
    driver = webdriver.Chrome(service=service)  # options=chrome_options)
    driver.maximize_window()

    warnings.simplefilter(action='ignore', category=FutureWarning)

    scraper = KMotorShopScraper()
    scraper.driver = driver
    scraper.get_models_data()


if __name__ == '__main__':
    main()
