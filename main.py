from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime


FOUNDATION_YEAR = 1920


def parse_product(product: list) -> dict:
    parsed_product = {
            'name': product[0][10:],
            'sort': product[1][6:],
            'price': product[2][6:] + ' р.',
            'picture': product[3][10:],
            'offer': bool(product[4]),
            }
    return parsed_product


def get_products_render_data(products_description):
    products = dict()
    current_index = 0
    index_delta = 5
    while current_index+index_delta <= len(products_description):
        try:
            first_symbol = products_description[current_index][0]
        except IndexError:
            current_index += 1
            continue
        if first_symbol == "#":
            category_name = products_description[current_index][2:]
            products[category_name] = []
            current_index += 3
        else:
            product = parse_product(
                    products_description[current_index:current_index+index_delta]
                    )
            if product['offer']:
                current_index += index_delta + 1
            else:
                current_index += index_delta
            products[category_name].append(product)
    return products


def render_index(env, products_dict):
    template = env.get_template('template.html')
    winery_age = datetime.now().year - FOUNDATION_YEAR
    rendered_page = template.render(
            winery_age=winery_age,
            products_dict=products_dict
            )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )  
    with open('products.txt', 'r') as my_file:
        products_description_lines = my_file.read().split('\n')
    products = get_products_render_data(products_description_lines)

    render_index(env, products)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
