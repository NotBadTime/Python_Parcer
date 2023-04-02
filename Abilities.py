from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from typing import List, NamedTuple
import psycopg2

url = "https://pokemondb.net/ability"
request = Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)

page = urlopen(request)
page_content_bytes = page.read()
page_html = page_content_bytes.decode("utf-8")
soup = BeautifulSoup(page_html, "html.parser")

Ability = []
ability_rows = soup.find_all("table", id="abilities")[0].find_all("tbody")[0].find_all("tr")
for ability in ability_rows[0:320]:
    ability_name = ability.find_all("td")[0].find_all("a")[0].getText()
    print(ability_name)
    ability_description = ability.find_all("td", {"class": "cell-med-text"})[0].getText()
    print(ability_description)

    Ability.append((ability_name, ability_description))


    conn = psycopg2.connect(dbname='postgres', user='User', password='', host='localhost')
    cursor = conn.cursor()

    cursor.executemany("INSERT INTO abilities VALUES (%s, %s)", Ability)
    conn.commit()
    conn.close

    Ability.clear()







