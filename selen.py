from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from links import links

options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")

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
    for button in driver.find_elements(By.XPATH, '//td[@class="member-area-button"]/div/span'):
        try:
            button.click()
            sleep(2)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            sleep(1)
            button.click()
            driver.execute_script("window.scrollBy(0, 1_000_000)")
            sleep(1)

        # (1.5)
        # MATCH_TOTAL_FIRST_TEAM_
        # MATCH_TOTAL_SECOND_TEAM_

        # Голы (нет 2 первых)
        # data-preference-id="GOALS_93367529"

        except Exception as e:
            sleep(1)
            print(e)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    print(www_name)
    s = driver.page_source
    with open(f'./{www_name}.html', 'w', encoding='utf-8') as f:
        f.write(s)
# def fill_form(contact: User):
#     def fill_element(find_element='question_last_name', text=''):
#         element = driver.find_element(value=find_element)
#         element.clear()
#         element.send_keys(text)
#
#         sleep(1)
#
#     fill_element('question_first_name', contact.first_name)
#     sleep(0.5)
#     fill_element('question_last_name', contact.last_name)
#     sleep(0.5)
#     fill_element('question_email', contact.email)
#     sleep(0.5)
#
# driver.get(url=user.url_registration)
# sleep(1)
# # Accept Cookies and fill form
# for i in range(5):
#     try:
#         driver.find_element(value='onetrust-accept-btn-handler').click()
#         sleep(0.5)
#     except web_error:
#         sleep(1)
#
# for i in range(5):
#     driver.get(url=user.url_registration)
#     try:
#         fill_form(user)
#         sleep(1)
#         print('fill_form_ok')
#
#         try:
#             with open(FILE_XPATH_BTN_ZOOM_REGISTRATION, mode='r', encoding='utf-8') as f:
#                 xpath = f.read()
#         except FileNotFoundError:
#             xpath = '//div[@class="btn-register mgb-lg mgt-sm"]//button'
#
#         driver.find_element(By.XPATH, xpath).click()
#     except web_error:
#         sleep(4)
#         continue
#     # check page is registration - ok
#     sleep(1)
#     try:
#         driver.find_element(By.XPATH, xpath).click()
#     except web_error:
#         driver.close()
#         driver.quit()
#         sleep(1)
#         return True
#
driver.close()
driver.quit()
