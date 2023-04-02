import psycopg2

conn = psycopg2.connect(dbname='postgres', user='User', password='', host='localhost')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE Abilities(
    Name VARCHAR(50) PRIMARY KEY,
    Description text);""")

cursor.execute("""CREATE TABLE Pokemons(
    ID integer,
    Name VARCHAR(50),
    Under_Name VARCHAR(50),
    Type text[],
    Total integer,
    HP integer,
    Attack integer,
    Defense integer,
    Sp_Attack integer,
    Sp_Defense integer,
    Speed integer,
    Species VARCHAR(50),
    Height  double precision,
    Weight  double precision,
    Abilities VARCHAR(50) references Abilities(Name),
    Second_Abilities VARCHAR(50) references Abilities(Name),
    Hidden_Abilities VARCHAR(50) references Abilities(Name),
    EV_yield text,
    Catch_rate integer,
    Base_Friendship integer,
    Base_Exp integer,
    Growth_Rate VARCHAR(50),
    Egg_Groups text[],
    Egg_cycles integer,
    Avatar text);""")

conn.commit()
conn.close
