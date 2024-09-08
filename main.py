from Excel import create_excel
from parser import parsing_all
from match import set_match_win
from renaming import renaming_html
from web_driver import download_page_on_links

if __name__ == '__main__':
    download_page_on_links()
    renaming_html()
    parsing_all()
    set_match_win()
    create_excel()
