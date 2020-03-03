from selenium import webdriver
from bs4 import BeautifulSoup as BS
from time import sleep

login = 'herew26@gmail.com'
password = 'VYrixCH3F7CXhyi'


def get_dairy_soup():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://login.mos.ru/")
    driver.find_element_by_css_selector('.link_primary__fU-Jd').click()
    driver.find_element_by_id('login').send_keys(login)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('bind').click()
    driver.get('https://dnevnik.mos.ru/?token=bcf2931677a1ea467493afb7ab27718b')

    while not driver.find_elements_by_tag_name('diary-student-diary-day'):
        continue

    sleep(1)
    page = driver.page_source
    driver.close()
    return page


def scraping(page):
    page = BS(page, 'html.parser')

    days = page.select('.lessons-wrapper[_ngcontent-c18]')
    for day in days:
        lessons = day.select('.lessons-wrapper[_ngcontent-c18] .schedule-item-row[_ngcontent-c18]')
        for lesson in lessons:
            name_div = lesson.select('.lessons-wrapper[_ngcontent-c18] .schedule-item-row[_ngcontent-c18] .subject[_ngcontent-c18]')[0]
            name = name_div.find('span').text
            # name = name.find_all('div')[0]
            print(name)
        print('\n')


def start():
    page = get_dairy_soup()
    scraping(page)

start()
