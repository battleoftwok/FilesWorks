import datetime
import shutil
import os
import re


ENCODING = 'utf-8'
PARSE_PATTERN = r'[c|с]л.кб-[отд|бр]+\..+\S'
CUR_DIR = os.path.abspath(os.curdir)
NEW_FOLDER_NAME = "update"


def generate_files(number=5):
    """
    Функция, которая генерирует пары файлов (.pdf, .txt)

    :param number: кол-во пар файлов
    :return: None
    """
    for i in range(number):
        txt_file = open(f'{i}.txt', 'w', encoding=ENCODING)
        txt_file.write(f'Это имя должен Сл. КБ/отд. иметь pdf-файл{i}')

        pdf_file = open(f'{i}.pdf', 'w', encoding=ENCODING)

        txt_file.close()
        pdf_file.close()


def parse(text: str):
    """
    Разбор строки

    :param text: строка
    :return: разобранная строка
    """
    try:
        return re.search(PARSE_PATTERN, text.replace("/", "-").replace(" ", "").lower())[0]
    except Exception:
        raise TypeError(f'По паттерну {PARSE_PATTERN} не найдено совпадений')


def search_pair_files(cur_file_name: str):
    """
    Генератор, который ищет файлы с одинаковым именем, но разными расширениями

    :param cur_file_name: имя текущего файла главного цикла
    :return: информация о файлах (номер файла в общем списке файлов текущей директории и его название)
    """
    for element in enumerate(os.listdir(CUR_DIR)):
        if os.path.splitext(element[1])[0] == os.path.splitext(cur_file_name)[0]:
            yield element[0], element[1]


def run():
    now = datetime.datetime.now().strftime("%Y%m%d")

    # Если нет папки update в текущей директории:
    if "update" not in os.listdir(CUR_DIR):

        # Создать папку:
        os.mkdir("update")

    for file in os.listdir(CUR_DIR):

        # Если объект является файлом:
        if os.path.isfile(file):

            # Если файл формата .txt:
            if os.path.splitext(file)[1] == ".txt":

                with open(f"{CUR_DIR}/{file}", 'r', encoding=ENCODING) as cur_file:
                    text_raw = cur_file.read()

                file_info = list(search_pair_files(file))

                # TODO: Данное условие является временным и костыльным (см. функцию search_pair_files) !!!
                # TODO: Создание конструкции file_info вынуждает дважды считывать список файлов текущей директории!
                if len(file_info) % 2 == 0:

                    # Переименовать перемещённый файл:
                    os.rename(shutil.move(f"{CUR_DIR}/{os.listdir(CUR_DIR)[file_info[0][0]]}",
                                          f"{CUR_DIR}/{NEW_FOLDER_NAME}"),
                              f"{CUR_DIR}/{NEW_FOLDER_NAME}/{now}_{parse(text_raw)}.pdf")

                    # Удаление txt-файла:
                    os.remove(f"{CUR_DIR}/{file}")


if __name__ == '__main__':

    # generate_files(number=4)
    run()
