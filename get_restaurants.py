import time
from urllib.parse import unquote
#import csv
import unicodecsv as csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

TIMEOUT =  5


def create_browser():
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    #option.add_argument("--headless")
    browser = webdriver.Chrome(executable_path="C:/Users/Aaa/Desktop/chromedriver_win32/chromedriver.exe", options=option)
    return browser

def get_all_data():
    browser = create_browser()

    for page_number in range(1, 3):
        browser.get(f"https://www.restu.cz/praha/?page={page_number}")
        page_infos = [['name', 'phone', 'website', 'facebook', 'restu_page']]
        try:
            WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='restaurant-list-content']//a[contains(@class, 'card-item-link')]")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        restaurants = browser.find_elements_by_xpath("//*[@id='restaurant-list-content']//a[contains(@class, 'card-item-link')]")
        time.sleep(2)
        for restaurant in restaurants[:5]:
            url = restaurant.get_attribute('href')
            restaurant_info = get_restaurant_info(browser=browser, url=url)
            restaurant_info.append(page_number)
            page_infos.append(restaurant_info)

        with open('restaurant_data.csv', 'ab') as file:
            output = csv.writer(file, delimiter=';')
            output.writerows(page_infos)
        
        time.sleep(2)
        #print(page_infos)


def get_restaurant_info(browser=None, url=''):
    if not browser:
        return

    script = f"window.open('{url}');"
    browser.execute_script(script)
    windows = browser.window_handles
    browser.switch_to.window(windows[1])
    try:
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='restaurant-name']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    title = browser.find_elements_by_xpath("//*[@id='restaurant-name']")
    links = browser.find_elements_by_xpath("//ul[@class='restaurant-detail-contact-buttons']//a")
    phone = browser.find_elements_by_xpath("//*[@id='restaurant-phone-0']")
    phone_number = unquote(phone[0].get_attribute('href'))

    info = [(title[0].text), phone_number.replace(u'\xa0', ' ')]
    for a in links[1:]:
        info.append(a.get_attribute('href'))

    time.sleep(2)
    browser.close()
    browser.switch_to.window(windows[0])
    print(info)
    return info



def main():
    get_all_data()

if __name__ == "__main__":
    main()
