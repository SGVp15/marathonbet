import datetime
import os
import pickle
import re

from bs4 import BeautifulSoup

from config import dir_html, matches_pickle
from match import Match


def parsing_html(html) -> Match:
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.prettify())

    # Ищем div с текстом "Все выборы" и забираем "RootBlock"
    root_block = (
        soup.find('div', string=re.compile(r'Все выборы.*'))
        .find_parent('div', {'data-mutable-id': "RootBlock"})
    )

    # print(root_block)
    # 1 и 2 в шапке
    # //td[@class="price height-column-with-price first-in-main-row coupone-width-1"]/span
    # //td[@class="price height-column-with-price first-in-main-row coupone-width-1"]/../td[@class="price height-column-with-price coupone-width-1"][2]/span
    table_title = (
        root_block.find_parent('div', {'class': "bg coupon-row"})
        .find('table', {'class': "coupon-row-item"})
    )
    # if table_title:
    # print(f'{table_title} OK')
    # print(table_title.prettify())
    try:
        block_name_area = table_title.find_all(name='td', attrs={'class': "first member-area"})[0]
        command_first_name = block_name_area.find_all('span')[0].text
        print(command_first_name)
        date_short = block_name_area.find_all_next(name='div', attrs={'class': "date date-short"})[0].find_next('div',
                                                                                                                attrs={
                                                                                                                    'class': "date-wrapper"}).text
        command_second_name = block_name_area.find_all('span')[1].text
        print(command_second_name)
    except IndexError:
        try:
            command_first_name = table_title.find_all(name='td', attrs={'class': "today-name"})[0].find('span').text
            command_second_name = table_title.find_all(name='td', attrs={'class': "today-name"})[1].find('span').text
        except IndexError:
            print('39')
            # print(f'{command_first_name = }')
            # print(f'{command_second_name = }')

    value_1_col_tag = table_title.find(
        'td', {"class": "price height-column-with-price first-in-main-row coupone-width-1"}
    )

    value_1_col = str(value_1_col_tag.find('span').text).strip().replace('.', ',')
    # print(f"{value_1_col = }")

    value_2_col_tag = value_1_col_tag.find_next_siblings()[1]
    value_2_col = str(value_2_col_tag.find('span').text).strip().replace('.', ',')
    # print(f"{value_2_col = }")
    # (1.5)
    # MATCH_TOTAL_FIRST_TEAM_
    # MATCH_TOTAL_SECOND_TEAM_
    match_total_first_team_tag = root_block.find(
        'div', {'data-preference-id': re.compile(r'MATCH_TOTAL_FIRST_TEAM_\d+')}
    )
    match_total_second_team_tag = root_block.find(
        'div', {'data-preference-id': re.compile(r'MATCH_TOTAL_SECOND_TEAM_\d+')}
    )

    try:
        match_total_first_team_1p5_value = str(
            match_total_first_team_tag.find_all('', string=re.compile(r'\s+\(1.5\)\s+'))[1]
            .find_parent()
            .find_next_sibling().text
        ).strip().replace('.', ',')
    except IndexError:
        match_total_first_team_1p5_value = ''

    # print(f'{match_total_first_team_value = }')

    try:
        match_total_second_team_1p5_value = str(
            match_total_second_team_tag.find_all('', string=re.compile(r'\s+\(1.5\)\s+'))[1]
            .find_parent()
            .find_next_sibling().text
        ).strip().replace('.', ',')
    except IndexError:
        match_total_second_team_1p5_value = ''

    # print(f'{match_total_second_team_value = }')

    # Голы (нет 2 первых)
    # //div[@data-preference-id="GOALS_93367529"]
    goals = (
        root_block.find('div', {'data-preference-id': re.compile(r'GOALS_\d+')})
        .find('table', {"class": "td-border"})
        .find_all('td')
    )
    player_1 = goals[0].text.strip()
    player_2 = goals[3].text.strip()

    player_1 = re.sub('забьет', '', player_1).strip()
    player_2 = re.sub('забьет', '', player_2).strip()
    # Меняем местами 1 и 2 игрока
    goals_dict = {
        player_1: str(goals[5].text.strip().replace('.', ',')),
        player_2: str(goals[2].text.strip().replace('.', ',')),
    }
    # print(goals_dict)

    return Match(
        command_first_name=command_first_name,
        command_second_name=command_second_name,
        date_short=date_short,
        value_1_col=value_1_col,
        value_2_col=value_2_col,
        match_total_first_team_1p5_value=match_total_first_team_1p5_value,
        match_total_second_team_1p5_value=match_total_second_team_1p5_value,
        goals_dict=goals_dict

    )


def parsing_all() -> [Match]:
    matches = []
    for root, dirs, files in os.walk(dir_html):

        if files:
            country = root.split('\\')[-2]
            country = re.sub(r'[^\w]+', ' ', country).strip()
            championship = root.split('\\')[-1]
            championship = re.sub(r'[^\w]+', ' ', championship).strip()

            for file in files:
                path = os.path.join('.', root, file)
                with (open(path, encoding='utf-8', mode='r') as f):
                    try:
                        match = parsing_html(f.read())

                        match.country = country
                        match.championship = championship
                        match.date = datetime.datetime.now().strftime('%Y.%m.%d')

                        matches.append(match)
                        print(f'[OK]\t{path}')
                    except TypeError as e:
                        print(f'[ERROR]\t{e}\n{path}')

    with open(matches_pickle, 'wb') as handle:
        pickle.dump(matches, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return matches
