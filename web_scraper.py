import requests
from bs4 import BeautifulSoup

url = requests.get('https://www.hltv.org/stats/players').text
soup = BeautifulSoup(url, 'html5lib')

player_table = soup.find("table", attrs={"class": "stats-table player-ratings-table"})
player_table_data = player_table.tbody.find_all('tr')

columns = []
teams = []

for row in player_table_data:
    columns.append(row.find('td'))

for team in player_table_data:
    teams.append(team.find('td', {'class': 'teamCol'}))

# a_tag = soup.select('.playerCol a')

# for a in a_tag:
#     print(a['href'])


# team = teams.find_all('a')

def web_scrape(i):
    player = columns[i].find('a').text
    team_from_top = teams[i].find('img').get('title')

    return (f'{player} from {team_from_top}')