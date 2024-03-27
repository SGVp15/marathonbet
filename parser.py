import os

from bs4 import BeautifulSoup
import re


def parsing_html(html):
    soup = BeautifulSoup(html, 'html.parser')
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
    # print(table_title.prettify())
    command_first_name = table_title.find_all('td', {'class': "name"})[0].find('span').text
    command_second_name = table_title.find_all('td', {'class': "name"})[1].find('span').text
    print(f'{command_first_name = }')
    print(f'{command_second_name = }')

    value_1_col_tag = table_title.find(
        'td', {"class": "price height-column-with-price first-in-main-row coupone-width-1"}
    )

    value_1_col = value_1_col_tag.find('span').text
    print(f"{value_1_col = }")

    value_2_col_tag = value_1_col_tag.find_next_siblings()[1]
    value_2_col = value_2_col_tag.find('span').text
    print(f"{value_2_col = }")
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
        match_total_first_team_value = float(
            match_total_first_team_tag.find_all('', string=re.compile(r'\s+\(1.5\)\s+'))[1]
            .find_parent()
            .find_next_sibling().text
        )
    except IndexError:
        match_total_first_team_value = ''

    print(f'{match_total_first_team_value = }')

    try:
        match_total_second_team_value = float(
            match_total_second_team_tag.find_all('', string=re.compile(r'\s+\(1.5\)\s+'))[1]
            .find_parent()
            .find_next_sibling().text
        )
    except IndexError:
        match_total_second_team_value = ''

    print(f'{match_total_second_team_value = }')

    # Голы (нет 2 первых)
    # //div[@data-preference-id="GOALS_93367529"]
    goals = (
        root_block.find('div', {'data-preference-id': re.compile(r'GOALS_\d+')})
        .find('table', {"class": "td-border"})
        .find_all('td')
    )
    goals_dict = {
        goals[0].text: goals[2].text.strip(),
        goals[3].text: goals[5].text.strip(),
    }
    print(goals_dict)


if __name__ == '__main__':
    for file in os.listdir('./data'):
        print(file)
        with open(f'./data/{file}', mode='r', encoding='utf-8') as f:
            parsing_html(f.read())
