import time

from requests import Session
from selenium.webdriver.support import expected_conditions as EC
from parser_class import Review

import driver as driver
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import (NoSuchElementException, ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth


def search_bar_text_input(address_post):
    search_box = driver.find_element(By.CSS_SELECTOR, ".input__control._bold")
    search_box.send_keys("Почтовый терминал " + address_post)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)


def star_count(self, element):
    default_count = 0
    for star in element.find_elements(By.XPATH, './/*[@class="business-rating-badge-view__stars"]/.//span'):
        if "empty" not in star.get_attribute("class"):
            default_count += 1
    return default_count


def parser_url():
    url = driver.current_url
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    # name = get_name(soup)
    # reviews = get_reviews(soup)
    # print(reviews)
    print("Прошел первую кт")
    while True:
        try:
            time.sleep(3)
            # Иначе он крутит страницу быстрее и появляються дубли отзывов
            view_more_button = driver.find_element(By.CLASS_NAME, 'tabs-select-view__title._name_reviews')
            print("Вторая кт " + view_more_button.text)
            WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.XPATH, '//*[@class="orgpage-reviews-view__loader"]')))
            view_more_button.click()

        except NoSuchElementException:
            print('К сожалению, пока отзывов и оценок нет, надеемся они скоро появятся.')
            break

        try:
            more_buttons = driver.find_elements(By.CSS_SELECTOR, '//*[@class="business-review-view__expand"]')
            print(more_buttons)

            for more_button in more_buttons:

                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
                    time.sleep(1)
                    more_button.click()

                except ElementNotInteractableException:
                    pass
        except:
            print("Ну нет этой кнопки нуу нет !")


        reviews = driver.find_elements(By.XPATH, '//*[@class="business-review-view__info"]')

        for review in reviews:
            driver.execute_script("arguments[0].scrollIntoView(true);", review)
            new_review = Review(review).__dict__
            #подвязать к бд!
            print(new_review)


def search_elements():
    element = driver.find_element(By.CLASS_NAME, 'search-business-snippet-view__content')
    time.sleep(2)
    element.click()
    time.sleep(2)
    parser_url()
    driver.back()
    time.sleep(2)


if __name__ == '__main__':
    """
    Для того чтобы не отображать браузер 
    раскомментируй данные строки
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    и закомментируй следующую строку
    """

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome('chromedriver.exe', options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get('https://yandex.ru/maps/')
    address_post = input("Адрес постамата!")
    search_bar_text_input(address_post)
    search_elements()
    driver.quit()
