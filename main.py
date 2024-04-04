import datetime
import os
import re

from Excel import add_to_excel_file
from config import dir_html
from parser import parsing_html
from web_driver import WebDriver
from links import links
from match import Match
import pickle


def download_page_on_links():
    driver = WebDriver()
    for link in links:
        print(link)
        driver.run_scraping(link)
    driver.close()


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
                    (
                        command_first_name, command_second_name, value_1_col, value_2_col,
                        match_total_first_team_1p5_value,
                        match_total_second_team_1p5_value, goals_dict) = parsing_html(
                        f.read())
                    try:
                        matches.append(Match(
                            country=country,
                            championship=championship,
                            command_first_name=command_first_name,
                            command_second_name=command_second_name,
                            value_1_col=value_1_col,
                            value_2_col=value_2_col,
                            match_total_first_team_1p5_value=match_total_first_team_1p5_value,
                            match_total_second_team_1p5_value=match_total_second_team_1p5_value,
                            goals_dict=goals_dict,
                            date=datetime.datetime.now().strftime('%Y.%m.%d')
                            )
                        )
                        print(f'[OK]\t{path}')
                    except Exception as e:
                        print(f'[ERROR]\t{path}')

    with open(f'./matches.pickle', 'wb') as handle:
        pickle.dump(matches, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return matches


def create_excel():
    with open(f'./matches.pickle', 'rb') as handle:
        matches = pickle.load(handle)
        add_to_excel_file(matches)


if __name__ == '__main__':
    download_page_on_links()
    # parsing_all()
    # create_excel()
