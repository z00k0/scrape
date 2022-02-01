import codecs
import fnmatch
import os

import pandas as pd
from bs4 import BeautifulSoup


def list_of_tbx():
    file_list = os.listdir()
    list_of_tbx = []
    pattern = '*.tbx'
    for item in file_list:
        if fnmatch.fnmatch(item, pattern):
            list_of_tbx.append(item)
    return list_of_tbx

def tbx_parser(file_name):
    with codecs.open(file_name, 'r', 'utf-8') as file:
        soup = BeautifulSoup(file.read(), 'xml')
    d = []
    for item in soup.body('termEntry'):
        ids = item['id']
        term = item.term.string
        try:
            note = item.note.string
        except AttributeError:
            note = ''
        except Exception as e:
            print(type(e))
        descrip = item.descrip.string
        d.append({
            'ID': ids,
            'Term': term,
            'Note': note,
            'Description': descrip
        })
    df = pd.DataFrame(d)
    out_file = file_name + '.xlsx'
    df.to_excel(out_file, sheet_name=file_name)

if __name__ == '__main__':
    files_to_parse = list_of_tbx()
    count = 0
    for item in files_to_parse:
        tbx_parser(item)
        count += 1
    print(f'Converted {count} file(s)')
