import os

DOWNLOAD_SITES = False  # Скачивать сайты

dir_html = 'data'
excel_file = './Кефы.xlsx'

os.makedirs(dir_html, exist_ok=True)

matches_pickle = os.path.join('.', 'matches.pickle')
