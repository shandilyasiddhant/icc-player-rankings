from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from datetime import datetime


url_men_or_women = {
    "M": "https://www.icc-cricket.com/rankings/mens/player-rankings/",
    "W": "https://www.icc-cricket.com/rankings/womens/player-rankings/"
}

url_format = {
    "A": "test/",
    "B": "odi/",
    "C": "t20i/"
}

url_skill = {
    "X": "batting/",
    "Y": "bowling/",
    "Z": "all-rounder/"
}

print("Please choose one from the options below!")
men_or_women = input("\nPlease enter 'M' for mens or 'W' for womens:   ")
format_game = input("\nPlease enter 'a' for TEST, 'b' for ODI, 'c' for T20I:    ")
skill_game = input("\nPlease enter 'x' for BATTER, 'y' for BOWLER, 'z' for 'ALL-ROUNDER':    ")

complete_url = []

if men_or_women.upper() in url_men_or_women.keys():
    if format_game.upper() in url_format.keys():
        if skill_game.upper() in url_skill.keys():
            full_url = url_men_or_women[men_or_women.upper()] + \
                       url_format[format_game.upper()] + \
                       url_skill[skill_game.upper()]
            complete_url.append(full_url)
        else:
            print("skill_game value incorrect!")
    else:
        print("format_game value incorrect")
else:
    print("men_or_women value incorrect")

if complete_url[0].__contains__('womens/player-rankings/test/'):
    print("\nSORRY!!! ICC does not have player rankings for WOMEN in TESTS!!")
else:
    response = requests.get("https://www.icc-cricket.com/rankings/mens/player-rankings/t20i/batting")

    soup = bs(response.text, "html.parser")

    # top row of the table to be targeted
    table1 = soup.find('table', {'class': 'table rankings-table'})
    # table = soup.find('div', {'class': 'rankings-block__container full'})

    player = []
    team = []
    rating = []
    career_best_rating = []

    # populating list for top ranked player
    player_rowI = player.append(table1.find('div', {'class': 'rankings-block__banner--name-large'}).text)
    team_rowI = team.append(table1.find('div', {'class': 'rankings-block__banner--nationality'}).text.strip())
    rating_rowI = rating.append(bs("<div class='rankings-block__banner--rating'>911</div>", "html.parser").text)
    career_best_rating_rowI = career_best_rating.append(bs('<span class = "rankings-block__career-best-text">947 v England, 30/12/2017</span>', 'html.parser').text)

    # populating lists for all rows except rowI
    table2 = soup.find_all('tr', {'class':'table-body'})

    for item in table2:
        player.append(item.find('td', {'class':'table-body__cell rankings-table__name name'}).text.strip())
        team.append(item.find('td', {'class':'table-body__cell nationality-logo rankings-table__team'}).text.strip())
        rating.append(item.find('td', {'class': 'table-body__cell rating'}).text)
        career_best_rating.append(item.find('td', {'class': 'table-body__cell u-text-right u-hide-phablet'}).text)

    # converting different lists to set of tuples
    data_player_rating = list(zip(player, team, rating, career_best_rating))

    # creating DataFrame to be written to Excel
    d = pd.DataFrame(data_player_rating, columns=['Player', 'Team', 'Rating', 'Career-best Rating'])

    # changing header name (default: blank)
    d.index.names = ['Rank']

    # default row index starts at 0, changing row index to start at 1
    d.index += 1

    # defining sheet name
    sheet_name = "Player Ranking" + "_" + men_or_women + "_" + format_game + "_" + skill_game

    # Writing the dataframe to a new Excel file
    try:
        d.to_excel('ICC Data_Players' + datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p") + '.xlsx',
                   sheet_name=sheet_name)  # filename

    except:
        print("\nSomething went wrong! Please check your code.")  # error msg

    else:
        print("\nWeb data successfully written to Excel.")

    finally:
        print("\nQuitting the program!")