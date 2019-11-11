from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime


def parse_wine(wine: list) -> dict:
    wine_dict = {
            'name': wine[0][10:],
            'sort': wine[1][6:],
            'price': wine[2][6:] + ' р.',
            'picture': wine[3][10:],
            'offer': False,
            }
    if wine[4]:
        wine_dict['offer'] = True
    return wine_dict


def get_raw_wine_data(filename: str) -> list:
    with open(filename, 'r') as my_file:
        wine_data = my_file.read().split('\n')
    return wine_data


def get_products_render_data():
    products_dict = dict()
    wine_data = get_raw_wine_data('products.txt')
    current_index = 0
    index_delta = 5
    while current_index+index_delta <= len(wine_data):
        try:
            first_symbol = wine_data[current_index][0]
        except IndexError:
            current_index += 1
            continue
        if first_symbol == "#":
            category_name = wine_data[current_index][2:]
            products_dict[category_name] = []
            current_index += 3
        else:
            wine = parse_wine(wine_data[current_index:current_index+index_delta])
            if wine['offer']:
                current_index += index_delta + 1
            else:
                current_index += index_delta
            products_dict[category_name].append(wine)
    return products_dict


FOUNDATION_YEAR = 1920

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

products_dict = get_products_render_data()

template = env.get_template('template.html')
winery_age = datetime.now().year - FOUNDATION_YEAR
rendered_page = template.render(
        winery_age=winery_age,
        products_dict=products_dict
        )

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
