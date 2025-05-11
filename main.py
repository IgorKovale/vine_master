from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
import collections

def ending(existence_years):
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


def existence_years():
    foundation_date = 1920
    existence_years = datetime.datetime.now().year-foundation_date
    existence_years = f'{existence_years} {ending(existence_years)}'
    return existence_years


def get_exel_data(filename):
    excel_data_df = pandas.read_excel(
        f'{filename}',
        sheet_name='Лист1', 
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )
    exel_drinks_dict = excel_data_df.to_dict()
    drinks_dict = collections.defaultdict(list)
    for drink_key in exel_drinks_dict['Название']:
        image = exel_drinks_dict['Картинка'][drink_key]
        drink = {
        'title' : exel_drinks_dict['Название'][drink_key],
        'sort' : exel_drinks_dict['Сорт'][drink_key],
        'price' : exel_drinks_dict['Цена'][drink_key],
        'image' : f'images/{image}',
        'category' : exel_drinks_dict['Категория'][drink_key],
        'sale' : exel_drinks_dict['Акция'][drink_key]
        }
        drinks_dict[drink['category']].append(drink)        
    return drinks_dict


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')
existence_years = existence_years()
drinks_dict = get_exel_data('wine.xlsx')
rendered_page = template.render(existence_years=existence_years, drinks_dict=drinks_dict)

with open('index.html', 'w', encoding="utf8") as file:
     file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()