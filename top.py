from bs4 import BeautifulSoup
from splinter import Browser
from time import sleep
import datetime
import csv
from config import *


def lovely_soup(html):
    return BeautifulSoup(html, 'lxml')


def write_csv(tops, country):
    filename = 'data/{}-{}.csv'.format(country, datetime.datetime.today().strftime('%d-%m-%Y'))
    with open(filename, 'w+') as f:
        write = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write.writerow(['Number', 'Title', 'Artist', 'Shazams'])
        for k, v in tops.items():
            shazams = str(v['shazams']).replace(',', '').replace('"', '')
            write.writerow([k, v['title'], v['artist'], shazams])


def get_shazams(browser, link):
    browser.execute_script(f'window.open("{link}");')
    sleep(3)
    browser.windows.current = browser.windows[1]
    soup = BeautifulSoup(browser.html, 'lxml')
    shazams = soup.find('em', {'class': 'num'}).text
    browser.windows[1].close()
    browser.windows.current = browser.windows[0]
    return shazams


def main():
    with Browser('chrome', headless=headless, incognito=True) as browser:
        for country in countries:
            print(f'------------------------ {country.upper()}')
            url = f'https://www.shazam.com/charts/top-100/{country}'
            tops = {}
            browser.visit(url)
            sleep(5)
            try:
                browser.find_by_text('Show More').click()
                sleep(3)
            except Exception as e:
                print(e)
            soup = BeautifulSoup(browser.html, 'lxml')
            items = soup.findAll('li', itemprop='track')
            for item in items:
                number = item.find('span', {'class': 'number'}).text
                if int(number) >= limit + 1:
                    break
                title = item.find('div', {'class': 'title'}).find('a')
                link = title['href']
                title = title.text
                artist = item.find('div', {'class': 'artist'}).find('a').text
                shazams = get_shazams(browser, link)

                print(f'{number} | {title} - {artist} | {shazams}')
                tops.update({number: {'title': title, 'artist': artist, 'shazams': shazams}})

            write_csv(tops, country)

if __name__ == '__main__':
    main()
