
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import psycopg2


url = "https://pokemondb.net/pokedex/all"
request = Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)

page = urlopen(request)
page_content_bytes = page.read()
page_html = page_content_bytes.decode("utf-8")

soup = BeautifulSoup(page_html, "html.parser")
pokemon_rows = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")

Pokemons = []
for pokemon in pokemon_rows[0:101]:
    pokemon_data = pokemon.find_all("td")

    id = pokemon_data[0]['data-sort-value']

    avatar = pokemon_data[0].find_all("span")[0].find_all("img")[0]['src']
    name = pokemon_data[1].find_all("a")[0].getText()
    try:
     u_name = pokemon_data[1].find_all("small")[0].getText()
    except:
     u_name = ""
    details_uri = pokemon_data[1].find_all("a")[0]['href']



    types = []
    for pokemon_type in pokemon_data[2].find_all("a"):
        types.append(pokemon_type.getText())

    total = pokemon_data[3].getText()
    hp = pokemon_data[4].getText()
    attack = pokemon_data[5].getText()
    defence = pokemon_data[6].getText()
    sp_attack = pokemon_data[7].getText()
    sp_defence = pokemon_data[8].getText()
    speed = pokemon_data[9].getText()

    entry_url = f'https://pokemondb.net{details_uri}'
    request = Request(
        entry_url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    entry_page_html = urlopen(request).read().decode("utf-8")
    entry_soup = BeautifulSoup(entry_page_html, "html.parser")

    species = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-row"})[0].find_all("tr")[2].find_all("td")[0].getText()

    heigth_s = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-row"})[0].find_all("tr")[3].find_all("td")[0].getText()
    height_s = heigth_s.split("m", 1)[0]
    height_s = height_s.replace("\xa0", "")

    weight_s = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-row"})[0].find_all("tr")[4].find_all("td")[0].getText()
    weight_s = weight_s.split("kg", 1)[0]
    weight_s = weight_s.replace("\xa0", "")

    abilities = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-row"})[0].find_all("tr")[5].find_all("span")[0].getText()
    abilities = abilities[3:]
    try:
        abilities_2 = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-row"})[0].find_all("tr")[5].find_all("span")[1].getText()
        abilities_2 = abilities_2[3:]
    except:
        abilities_2 = "None"

    h_abilities = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-row"})[0].find_all("tr")[5].find_all("a")[0].getText()
    h_abilities = h_abilities.split("(", 1)[0]

    ev_yield = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-col span-md-12 span-lg-4"})[0].find_all("tr")[0].find_all("td")[0].getText()
    catch_rate = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-col span-md-12 span-lg-4"})[0].find_all("tr")[1].find_all("td")[0].getText()
    friendship = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-col span-md-12 span-lg-4"})[0].find_all("tr")[2].find_all("td")[0].getText()
    base_exp = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-col span-md-12 span-lg-4"})[0].find_all("tr")[3].find_all("td")[0].getText()
    growth_rate = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-col span-md-12 span-lg-4"})[0].find_all("tr")[4].find_all("td")[0].getText()
    catch_rate = catch_rate.split("(", 1)[0]
    friendship = friendship.split("(", 1)[0]

    eggs_gr = []
    for eggs_groups in entry_soup.find_all("main")[0].find_all("div", {"class": "grid-col span-md-6 span-lg-12"})[1].find_all("tr")[0].find_all("td")[0].find_all("a"):
      eggs_gr.append(eggs_groups.getText())

    egg_cycles = entry_soup.find_all("main")[0].find_all("div", {"class": "grid-col span-md-6 span-lg-12"})[1].find_all("tr")[2].find_all("td")[0].getText()
    egg_cycles = egg_cycles.split("(", 1)[0]
    print(egg_cycles)




    Pokemons.append((id, name, u_name, types, total, hp, attack, defence, sp_attack, sp_defence, speed, species, height_s,
    weight_s, abilities, abilities_2, h_abilities, ev_yield, catch_rate, friendship, base_exp, growth_rate, eggs_gr, egg_cycles, avatar))
    print(Pokemons)

    conn = psycopg2.connect(dbname='postgres', user='User', password='', host='localhost')
    cursor = conn.cursor()

    cursor.executemany("INSERT INTO pokemons VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)", Pokemons)
    conn.commit()
    conn.close

    Pokemons.clear()



