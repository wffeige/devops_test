#encoding:utf-8
import os
import sys
from bs4 import BeautifulSoup





def handle_html():
    with open('html.txt', 'r') as e:
        html_doc = ''.join(e.readlines())




    soup = BeautifulSoup(html_doc,"html.parser")
    # print soup.prettify()
    # print soup.find('span').find('text')
    # print soup.title.name
    # lst_a = soup.find('tr')
    # lst_a = soup.find('span').find('text')
    lst_a = soup.find_all(style="width: 75px; ")
    lst_b = soup.find_all(style = "width: 100px; ")




    with open ('web_info_timestamp.txt','w') as e:
        li = []
        for i in lst_a:
            line = i.string
            line = str(line)
            print line
            e.write(line+'\n')
        e.close()
def main():
    handle_html()


if __name__ == '__main__':
    main()