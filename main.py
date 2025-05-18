import os.path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse

def get_ending(existence_years):
    two_last_digits = existence_years % 100
    if 5 <= two_last_digits <= 20:
        return 'лет'
    last_digit = existence_years % 10
    if last_digit == 1:
        return 'год'
    elif 2 <= last_digit <= 4:
        return 'года'
    else:
        return 'лет'


def calculate_existence_years():
    foundation_date = 1920
    existence_years = datetime.datetime.now().year-foundation_date
    existence_years = f'{existence_years} {get_ending(existence_years)}'
    return existence_years


def get_exel_data(path):
    excel_data_df = pandas.read_excel(
        path,
        sheet_name='Лист1', 
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )
    exel_drinks = excel_data_df.to_dict()
    drinks = collections.defaultdict(list)
    for drink_key in exel_drinks['Название']:
        image = exel_drinks['Картинка'][drink_key]
        drink = {
        'title' : exel_drinks['Название'][drink_key],
        'sort' : exel_drinks['Сорт'][drink_key],
        'price' : exel_drinks['Цена'][drink_key],
        'image' : os.path.join('images',image),
        'category' : exel_drinks['Категория'][drink_key],
        'sale' : exel_drinks['Акция'][drink_key]
        }
        drinks[drink['category']].append(drink)
    return drinks

def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    parser = argparse.ArgumentParser(description='python main.py --path yourpath')
    parser.add_argument(
        '--path',
        type=str,
        help='Укажите путь к файлу с ассортиментом',
        default='wine.xlsx'
    )
    args=parser.parse_args()
    template = env.get_template('template.html')
    existence_years = calculate_existence_years()
    drinks = get_exel_data(args.path)
    rendered_page = template.render(existence_years=existence_years, drinks=drinks)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
