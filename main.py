from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime

def parse_wine(wine:list) -> dict:
    wine_dict = {
            'name': wine[0][10:],
            'sort':wine[1][6:],
            'price':wine[2][6:],
            'picture': wine[3][10:],
            }
    return wine_dict

wine_list = []
with open('vino.txt','r') as my_file:
    wine_data = my_file.read().split('\n')

first_index = 0
last_index = 4
while last_index < len(wine_data):
    wine = wine_data[first_index:last_index]
    first_index += 5
    last_index += 5
    wine_list.append(parse_wine(wine))


            

FOUNDATION_YEAR = 1920

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


template = env.get_template('template.html')
winery_age = datetime.now().year - FOUNDATION_YEAR
rendered_page = template.render(
        winery_age = winery_age,
        wine_list = wine_list
        )
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
