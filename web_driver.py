import os
import random
import time
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

from config import dir_html


class WebDriver():
    web_error = (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException)

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        # options.add_argument("--headless")
        options.add_argument("--disable-notifications")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        stealth(self.driver,
                languages=["ru-RU", "ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def run_scalp(self, url):
        country = url.split('/')[6]
        championship = url.split('/')[7]
        os.makedirs(f'./{dir_html}/{country}/{championship}', exist_ok=True)

        self.driver.get(url=url)
        sleep(0.5)
        count_buttons = len(self.driver.find_elements(By.XPATH, '//td[@class="member-area-button"]/div/span'))
        for i in range(count_buttons):
            button = self.driver.find_elements(By.XPATH, '//td[@class="member-area-button"]/div/span')[i]

            scroll_origin = ScrollOrigin.from_viewport(1000, 500)
            ActionChains(self.driver) \
                .scroll_from_origin(scroll_origin, 0, 46) \
                .perform()

            try:
                button.click()
                sleep(3)

                with open(f'./{dir_html}/{country}/{championship}/{i}.html', mode='w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)

                button.click()
            except Exception as e:
                print(f'[Error] i \n {e}')
            finally:
                sleep(1)

    def close(self):
        self.driver.close()
        self.driver.quit()
