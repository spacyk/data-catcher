import time
from urllib.parse import unquote
import unicodecsv as csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

TIMEOUT = 5


def create_browser():
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--headless")
    browser = webdriver.Chrome(executable_path="C:/Users/Aaa/Desktop/chromedriver_win32/chromedriver.exe", options=option)
    return browser


def get_all_data():
    browser = create_browser()
    with open('restaurant_data.csv', 'ab') as file:
        output = csv.writer(file, delimiter=';')
        output.writerow(['name', 'phone', 'website', 'facebook', 'rating', 'rating_count', 'restu_page'])

    for page_number in range(1, 191):
        browser.get(f"https://www.restu.cz/praha/?page={page_number}")
        restaurants = []
        try:
            WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='restaurant-list-content']//a[contains(@class, 'card-item-link')]")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        restaurant_links = browser.find_elements_by_xpath("//*[@id='restaurant-list-content']//a[contains(@class, 'card-item-link')]")
        for link in restaurant_links:
            url = link.get_attribute('href')
            restaurant_info = get_restaurant_info(browser=browser, url=url)
            restaurant_info.append(page_number)
            restaurants.append(restaurant_info)

        with open('restaurant_data.csv', 'ab') as file:
            output = csv.writer(file, delimiter=';')
            output.writerows(restaurants)
        time.sleep(1)


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

    title_element = browser.find_elements_by_xpath("//*[@id='restaurant-name']")
    phone_element = browser.find_elements_by_xpath("//*[@id='restaurant-phone-0']")
    links_element = browser.find_elements_by_xpath("//ul[@class='restaurant-detail-contact-buttons']//a")
    rating_element = browser.find_elements_by_xpath("//strong[@class='restaurant-detail-header__rating-value']//span")
    rating_count_element = browser.find_elements_by_xpath("//span[@class='restaurant-detail-header__rating-text']")

    title = title_element[0].text if title_element else None
    phone = (unquote(phone_element[0].get_attribute('href')).replace(u'\xa0', ' ')).lstrip('tel:') if phone_element else None
    rest_link = links_element[1].get_attribute('href') if len(links_element) == 2 else None
    fb_link = links_element[2].get_attribute('href') if len(links_element) >= 3 else None
    rating = rating_element[0].text if rating_element else None
    rating_count = rating_count_element[0].text.split(' ')[1] if rating_count_element else None

    time.sleep(0.5)
    browser.close()
    browser.switch_to.window(windows[0])
    print(title, rest_link, fb_link, phone, rating, rating_count)
    return [title, phone, rest_link, fb_link, rating, rating_count]


def main():
    get_all_data()


if __name__ == "__main__":
    main()
