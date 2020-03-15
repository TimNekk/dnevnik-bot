from bs4 import BeautifulSoup as BS
import re
import pickle


def get_page():
    with open('pages.txt', 'r') as file:
        page = file.read()
    return page


def get_page2():
    with open('pages2.txt', 'rb') as file:
        page = file.read()
    return page


def get_periods_count(marks_page):
    page = BS(marks_page, 'html.parser')
    subject_div = page.select('.subject-periods-wrapper')[0]
    periods = subject_div.select('.subject-period')
    periods_count = len(periods)
    return periods_count


# TODO - Сделать
def get_analysis():
    pass


def get_marks(marks_page, period_count, multiply_marks=False):
    page = BS(marks_page, 'html.parser')

    subjects_div = page.select('.all-marks-data')  # Предметы
    subjects = []
    for subject_div in subjects_div:
        name = subject_div.select('.all-marks-data .br-text')[0].text  # Название предмета

        try:
            period_div = subject_div.select('.module-marks')[period_count]  # Пероид
        except IndexError:
            return False

        marks = []
        marks_div = period_div.select('.module-marks-row span')  # Оценки
        for mark_div in marks_div:
            mark = mark_div.text
            mark = re.findall(r'\d', mark)[0]

            # Вес
            try:
                weight = mark_div.select('.module-marks-row span sub')[0].text

                if multiply_marks:
                    mark = str(int(mark) * int(weight))
                else:
                    if weight == '2':
                        mark += '²'
                    elif weight == '3':
                        mark += '³'
                    elif weight == '4':
                        mark += '⁴'
                    elif weight == '5':
                        mark += '⁵'
            except IndexError:
                pass

            marks.append(mark)
        avg_mark = period_div.select('.module-avg-mark')[0].text  # Средний балл

        subject = {'name': name, 'marks': marks, 'avg_mark': avg_mark}

        subjects.append(subject)

    return subjects


def get_week_info(diary_page):
    page = BS(diary_page, 'html.parser')
    try:
        return page.select('h3[_ngcontent-c18]')[0].text
    except:
        return False


def get_grade_and_school(diary_page):
    page = BS(diary_page, 'html.parser')
    grade = page.select('.header[_ngcontent-c15] .ezd-header h2')[0].text
    grade = re.findall(r',.+', grade)[0][2:]

    school = page.select('.dropdown-profile-current')[0].text
    school = re.findall(r'\w.+', school)[0]

    return grade, school


def get_fio(diary_page):
    page = BS(diary_page, 'html.parser')
    fio = page.select('.user-account .cabinet-link')[0].text
    fio = re.findall(r'\w+ \w. \w.', fio)[0]  # Убрать пробелы
    return fio


def get_timetable(diary_page, weekday):

    page = BS(diary_page, 'html.parser')

    day = page.select('.lessons-wrapper[_ngcontent-c18]')[weekday]  # Получение нужного дня

    # Есть ли расписание на этот день
    if day.select('.empty-lessons-label[_ngcontent-c18]'):
        return False

    lessons = day.select('.lessons-wrapper[_ngcontent-c18] .schedule-item-row[_ngcontent-c18]')  # Получение уроков
    lessons_to_return = []
    for lesson in lessons:

        # Получение название
        name_div = lesson.select('.lessons-wrapper[_ngcontent-c18] .schedule-item-row[_ngcontent-c18] .subject[_ngcontent-c18]')[0]
        name = name_div.find('span').text
        name = re.findall(r'\w.+', name)[0]

        # Получение задания
        try:
            task = lesson.select('.homework-description[_ngcontent-c18]')[0].text
            task = re.findall(r'\w.+', task)[0]
        except IndexError:
            task = False

        # Получение оценок
        marks = []
        try:
            marks_div = lesson.select('.lessons-wrapper[_ngcontent-c18] .schedule-item-row[_ngcontent-c18] .marks[_ngcontent-c18] diary-student-diary-mark[_ngcontent-c18]')
        except IndexError:
            marks_div = []

        if marks_div:
            for mark_div in marks_div:
                # Оценка
                mark = mark_div.select('.student-diary-mark[_ngcontent-c28] span[_ngcontent-c28]')[0].text
                mark = re.findall(r'\d', mark)[0]
                # Вес
                try:
                    weight = mark_div.select('.mark-weight[_ngcontent-c28]')[0].text
                    if weight == '2':
                        mark += '²'
                    elif weight == '3':
                        mark += '³'
                    elif weight == '4':
                        mark += '⁴'
                    elif weight == '5':
                        mark += '⁵'
                except IndexError:
                    pass
                marks.append(mark)

        # Получение Н'ки
        try:
            n = lesson.select('.student-diary-attendance[_ngcontent-c29] > div[_ngcontent-c29]:first-child')[0]
            marks.append('Н')
        except IndexError:
            pass

        lessons_to_return.append([name, task, marks])

    return lessons_to_return


if __name__ == '__main__':
    # # Получние расписания
    # lessons = get_timetable(get_page(), 1)
    # numbers = '➀➁➂➃➄➅➆'
    # if lessons:
    #     text = ''
    #     for i, lesson in enumerate(lessons, 0):  # Проход через все уроки
    #         # Название
    #         text += f'*{numbers[i]} {lesson[0]}'
    #
    #         # Оценки
    #         if lesson[2]:
    #             text += ' | '
    #             for mark in lesson[2]:
    #                 text += f'{mark} '
    #         text += '*'
    #
    #         # Задание
    #         if lesson[1]:
    #             text += f'\n_{lesson[1]}_\n\n'
    #         else:
    #             text += '\n\n'
    # else:
    #     text = 'На этот день нет расписания'
    #
    # print(text)

    # get_week_info(get_page())

    print(get_marks(get_page2(), 1))