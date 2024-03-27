import re

from bs4 import BeautifulSoup


def parsing_html(html):
    # soup = BeautifulSoup(html, 'html.parser')
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
    # print(table_title.prettify())
    command_first_name = table_title.find_all('td', {'class': "name"})[0].find('span').text
    command_second_name = table_title.find_all('td', {'class': "name"})[1].find('span').text
    # print(f'{command_first_name = }')
    # print(f'{command_second_name = }')

    value_1_col_tag = table_title.find(
        'td', {"class": "price height-column-with-price first-in-main-row coupone-width-1"}
    )

    value_1_col = float(value_1_col_tag.find('span').text)
    # print(f"{value_1_col = }")

    value_2_col_tag = value_1_col_tag.find_next_siblings()[1]
    value_2_col = float(value_2_col_tag.find('span').text)
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
        match_total_first_team_1p5_value = float(
            match_total_first_team_tag.find_all('', string=re.compile(r'\s+\(1.5\)\s+'))[1]
            .find_parent()
            .find_next_sibling().text
        )
    except IndexError:
        match_total_first_team_1p5_value = ''

    # print(f'{match_total_first_team_value = }')

    try:
        match_total_second_team_1p5_value = float(
            match_total_second_team_tag.find_all('', string=re.compile(r'\s+\(1.5\)\s+'))[1]
            .find_parent()
            .find_next_sibling().text
        )
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
        player_1: float(goals[5].text.strip()),
        player_2: float(goals[2].text.strip()),
    }
    # print(goals_dict)

    return (
        command_first_name,
        command_second_name,
        value_1_col,
        value_2_col,
        match_total_first_team_1p5_value,
        match_total_second_team_1p5_value,
        goals_dict
    )
