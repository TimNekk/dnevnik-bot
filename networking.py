from selenium import webdriver, common
from bs4 import BeautifulSoup as BS
from time import sleep
from threading import Thread


slogin = 'herew26@gmail.com'
spassword = 'VYrixCH3F7CXhyi'

timer_work = True


def start_timer():
    i = 0
    while timer_work:
        sleep(1)
        i += 1
        print(i)


def get_diary_page(login, password):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://login.mos.ru/")
    driver.find_element_by_css_selector('.link_primary__fU-Jd').click()
    driver.find_element_by_id('login').send_keys(login)
    driver.find_element_by_id('password').send_keys(password)
    sleep(1)
    driver.find_element_by_id('bind').click()

    # Получение страницы с расписанием
    driver.get('https://dnevnik.mos.ru/?token=1673527472d3add00f032929d0a553d4')

    try:
        driver.find_element_by_id('login').send_keys(login)
        driver.find_element_by_id('password').send_keys(password)
        sleep(1)
        driver.find_element_by_id('bind').click()
    except common.exceptions.NoSuchElementException:
        pass

    while not driver.find_elements_by_tag_name('diary-student-diary-day'):  # Ожидание загрузки страницы
        continue
    sleep(1)
    timetable_page = driver.page_source

    # Получение страницы с оценками
    driver.get('https://dnevnik.mos.ru/progress/all_marks')

    while not driver.find_elements_by_tag_name('.all-marks-data .br-text'):  # Ожидание загрузки страницы
        continue
    sleep(1)
    marks_page = driver.page_source

    driver.close()
    return timetable_page, marks_page


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
    Thread(target=start_timer).start()
    timetable_page, marks_page = get_diary_page()
    # scraping()

# start()
