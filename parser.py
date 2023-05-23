from telnetlib import EC
from parser_class import Review
import driver as driver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
from selenium.common.exceptions import (NoSuchElementException, ElementNotInteractableException)
from selenium.webdriver.support.wait import WebDriverWait


def search_bar_text_input(address_postamat):
    search_box = driver.find_element_by_css_selector(".input__control._bold")
    search_box.send_keys("Почтовый терминал " + address_postamat)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)


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
            time.sleep(3) #Иначе он крутит страницу быстрее и появляються дубли отзывов
            view_more_button = driver.find_element(By.CLASS_NAME, 'tabs-select-view__title._name_reviews')
            print("Вторая кт")
            #WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.XPATH, '//*[@class="orgpage-reviews-view__loader"]')))
            view_more_button.click()

        except NoSuchElementException:
            print('К сожалению, пока отзывов и оценок нет, надеемся они скоро появятся.' )
            break

    more_buttons = driver.find_elements_by_xpath('//*[@class="business-review-view__expand"]')

    for more_button in more_buttons:

        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            time.sleep(1)
            more_button.click()

        except ElementNotInteractableException:
            pass

def get_name(soup_content):
    for data in soup_content.find_all("h1", {"class": "orgpage-header-view__header"}):
        name = data.getText()
    return name


"""def get_reviews(soup_content):
    try:
        time.sleep(5)
        driver.find_element(By.CLASS_NAME, 'tabs-select-view__title._name_reviews').click()

    except:
        print("Для данного постамата отзывов и оценок пока нет!")

"""
def search_elements():
    element = driver.find_element(By.CLASS_NAME, 'search-business-snippet-view__content')
    time.sleep(5)
    element.click()
    time.sleep(5)
    parser_url()
    driver.back()
    time.sleep(5)


if __name__ == '__main__':
    """
    Для того чтобы не отображать браузер 
    раскомментируй данные строки
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    и закомментируй следующую строку
    """
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://yandex.ru/maps/')
    address_postamat = input("Адрес постамата!")
    search_bar_text_input(address_postamat)
    search_elements()
    driver.quit()
