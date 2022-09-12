from pathlib import Path
import datetime
import shutil
import sys
import os
import re
sddddddddddd


ENCODING = 'utf-8'
PARSE_PATTERN = r'[c|с]л.кб-[отд|бр]+\..+\d+'
NEW_FOLDER_NAME = "update"


def generate_files(number=5):
    for i in range(number):
        txt_file = open(f'{i}.txt', 'w', encoding=ENCODING)
        txt_file.write(f'Это имя должен Сл. КБ/отд. иметь pdf-файл{i}634\n34tg4hty6hnerbtse56va6565')

        pdf_file = open(f'{i}.pdf', 'w', encoding=ENCODING)

        txt_file.close()
        pdf_file.close()


def parse(text: str):
    result = re.findall(PARSE_PATTERN, text.replace("/", "-").replace(" ", "").lower())
    return result[0] if result else None


def search_pair_files():
    return map(lambda element: (element, Path(str(element.parent.joinpath(element.stem)) + '.txt')),
               filter(lambda x: x.suffix == '.pdf', map(Path, os.listdir('.'))))


def run():
    now = datetime.datetime.now().strftime("%Y%m%d")
    os.makedirs(NEW_FOLDER_NAME, exist_ok=True)

    for pdfs, txts in search_pair_files():
        with txts.open('r', encoding=ENCODING) as cur_file:
            text_raw = cur_file.read()

        parse_result = parse(text_raw)

        if parse_result is not None:
            # Переименовать перемещённый файл:
            shutil.move(pdfs, f"./{NEW_FOLDER_NAME}/{now}_{parse_result}.pdf")
            # Удаление txt-файла:
            os.remove(txts)
        else:
            print(f'В файле {txts} не найдено искомое значение', file=sys.stderr)


if __name__ == '__main__':
    # generate_files(number=5)
    run()

    input('\nPress Enter to continue...')
