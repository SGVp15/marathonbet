from time import sleep
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from links import links
from parser import get_bs

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
stealth(driver,
        languages=["ru-RU", "ru"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
web_error = (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException)
www_name = 0

for url in links:
    www_name += 1
    driver.get(url=url)
    for i, button in enumerate(driver.find_elements(By.XPATH, '//td[@class="member-area-button"]/div/span')):
        sleep(1)

        s121 = driver.find_elements(By.XPATH, '//td[@class="member-area-button"]/div/span')[0]

        try:
            button.click()
            sleep(2)
            # get_bs(driver.page_source)
            sleep(1)
            if i == 2:
                print(www_name)
                s = driver.page_source
                with open(f'./{www_name}.html', 'w', encoding='utf-8') as f:
                    f.write(s)

            button.click()

        except Exception as e:
            sleep(1)
            print(e)

driver.close()
driver.quit()
