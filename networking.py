from selenium import webdriver, common
from time import sleep
import secrets
import pickle
import scraping as s


slogin = 'herew26@gmail.com'
spassword = 'VYrixCH3F7CXhyi'


def get_diary_pages(login, password):
    driver = webdriver.Chrome('chromedriver.exe')

    url = 'https://dnevnik.mos.ru/?token=' + str(secrets.token_hex())  # Генерация url

    driver.get(url)
    driver.find_element_by_id('login').send_keys(login)  # Ввести логин
    driver.find_element_by_id('password').send_keys(password)  # Ввести пароль
    sleep(1)
    driver.find_element_by_id('bind').click()  # Кнопка войти

    # Если данные не верные
    if driver.find_elements_by_css_selector('blockquote ol:last-child, blockquote p:last-child, blockquote ul:last-child'):
        driver.close()
        return False

    # Если появилось еще одно окно с авторизацией

    # Получение страницы с расписанием
    while not driver.find_elements_by_tag_name('diary-student-diary-day'):  # Ожидание загрузки страницы
        continue
    sleep(1)
    timetable_page_now = driver.page_source

    # Получение страницы с расписанием на след. неделю
    old = s.get_week_info(driver.page_source)
    driver.find_element_by_css_selector('.diary-toolbar[_ngcontent-c19] .next-week-button[_ngcontent-c19]').click()  # Кнопка след. неделя

    # Ожидание загрузки страницы
    while True:
        new = s.get_week_info(driver.page_source)
        if new != old and new:
            break

    while not driver.find_elements_by_tag_name('diary-student-diary-day'):  # Ожидание загрузки страницы
        continue
    timetable_page_next = driver.page_source

    # Получение страницы с расписанием на пред. неделю
    for _ in range(2):
        old = s.get_week_info(driver.page_source)
        driver.find_element_by_css_selector('.mat-stroked-button:not([class*=mat-elevation-z])').click()  # Кнопка пред. неделя

        # Ожидание загрузки страницы
        while True:
            new = s.get_week_info(driver.page_source)
            if new != old and new:
                break

    while not driver.find_elements_by_tag_name('diary-student-diary-day'):  # Ожидание загрузки страницы
        continue
    timetable_page_pre = driver.page_source

    # Получение страницы с оценками
    driver.get('https://dnevnik.mos.ru/progress/all_marks')

    while not driver.find_elements_by_css_selector('.all-marks-data .br-text'):  # Ожидание загрузки страницы
        continue
    sleep(1)
    marks_page = driver.page_source

    driver.close()
    return timetable_page_now, timetable_page_next, timetable_page_pre, marks_page


if __name__ == '__main__':
    page = get_diary_pages(slogin, spassword)
    print(page[3])

    with open('pages2.txt', 'wb') as file:
        pickle.dump(page[3], file)

