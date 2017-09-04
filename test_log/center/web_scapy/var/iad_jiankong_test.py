#encoding:utf-8
import os
import sys
from bs4 import BeautifulSoup





def handle_html():
    with open('index.txt', 'r') as e:
        html_doc = ''.join(e.readlines())

    soup = BeautifulSoup(IAD_var,"html.parser")
    print soup.prettify()
    print soup.find('span').find('text')
    # print soup.title.name
    # lst_a = soup.find_all('span')
    # lst_a = soup.find('span').find('text')
    lst_a = soup.find_all(class_="text")

    with open ('zhibiao.txt','w') as e:
        li = []
        for i in lst_a:
            li.append(i.string)
            print i.string
            # e.write(i.string)
        # e.write(li)
def main():
    handle_html()


if __name__ == '__main__':
    main()