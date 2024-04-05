import os

from config import dir_html

def renaming_html():
    for root, dirs, files in os.walk(dir_html):
        if files:
            for file in files:
                path_source = os.path.join('.', root, file)
                path_dist = os.path.join('.', root, f'{int(file.split('.')[0]):03}.html')
                os.rename(path_source,path_dist)