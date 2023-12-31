import mysql.connector
import random

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="crime_game",
    user="root",
    password="123456",
    autocommit=True
)


# ---------------  Player class ---------------- #
def set_player_name(player_name):
    sql = f"INSERT INTO detective_game(detective_name) VALUES('{player_name}');"
    cursor = connection.cursor()
    cursor.execute(sql)
    return

def update_player_location(player_id,location):
    sql = f"UPDATE detective_game SET player_location = '{location}' WHERE id = {player_id}"
    cursor = connection.cursor()
    cursor.execute(sql)
    return

# ---------------  Game class  ---------------- #

def start_game():
    countries = []
    sql = "SELECT country_name, hint FROM hints "
    sql += "ORDER BY RAND() LIMIT 5;"
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
            country = {"name": result[0], "hint": result[1]}
            countries.append(country)
    return countries

def update_crime_location(player_id, number):
    global criminal_escaped
    global visited_locations
    countries = get_countries()
    if len(visited_locations) == number:
        criminal_escaped = True
        return
    while len(visited_locations)-1 < number:
        ran_num = random.randrange(0, number)
        if countries[ran_num] not in visited_locations:
            cursor = connection.cursor()
            visited_locations.append(countries[ran_num])
            update_query = f"UPDATE detective_game SET crime_location = '{countries[ran_num]}' WHERE id = {player_id}"
            cursor.execute(update_query)
            break

def get_available_countries():
    countries = "SELECT name, latitude_deg, longitude_deg, hints.country_name FROM airport, hints WHERE hints.iso_country = airport.iso_country GROUP BY airport.iso_country"
    cursor = connection.cursor()
    cursor.execute(countries)
    result = cursor.fetchall()
    countries = []
    for row in result:
        countries.append({"name": row[0], "lat": row[1], "long": row[2], "country": row[3]})
    return countries