from requests import get
from csv import writer
from sys import exit
from bs4 import BeautifulSoup, Tag

response = get('https://www.moneycontrol.com/stocks/marketstats/nse_vshockers/index.php')

if response.status_code != 200:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser').select_one('#mc_content')
rows = []

cols = [col.text.strip() for col in soup.select('div.bsr_table > table th:not(.PR)')]
rows.append(cols)


def is_valid_td(tag: Tag):
    return (
        tag.name == 'td' and
        (not tag.has_attr('class') or
         {'PR', 'green', 'red'} & set(tag.get('class')))
    )


for row in soup.select('div.bsr_table > table > tbody > tr'):
    cols = []
    for col in row.find_all(is_valid_td, recursive=False):
        if isinstance(col.h3, Tag):
            cols.append(col.h3.a.text.strip())
        else:
            cols.append(col.text.strip())
    rows.append(cols)

with open('output.csv', 'w', newline='') as csvfile:
    csv_writer = writer(csvfile)
    csv_writer.writerows(rows)
