from bs4 import BeautifulSoup
from splinter import Browser
from time import sleep
import datetime
import csv
from config import *


all_shazams = {}


def write_csv(tops):
    filename = 'data/tracks-{}.csv'.format(datetime.datetime.today().strftime('%d-%m-%Y'))
    with open(filename, 'w+') as f:
        write = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write.writerow(['Number', 'Country', 'Title', 'Artist', 'Shazams'])
        for k, v in tops.items():
            shazams = str(v['shazams']).replace(',', '').replace('"', '')
            write.writerow([v['number'], v['country'], v['title'], v['artist'], shazams])


def get_shazams(browser, track):
    url = f'https://www.shazam.com/track/{track}'
    browser.visit(url)
    sleep(3)
    soup = BeautifulSoup(browser.html, 'lxml')
    shazams = soup.find('em', {'class': 'num'}).text
    all_shazams.update({track: shazams})


def main():
    with Browser('chrome', headless=headless, incognito=True) as browser:
        tops = {}
        c = 1
        for track in tracks:
            get_shazams(browser, track)

        for country in countries:
            print(f'------------------------ {country.upper()}')
            url = f'https://www.shazam.com/charts/top-100/{country}'
            browser.visit(url)
            sleep(3)
            try:
                browser.find_by_text('Show More').click()
                sleep(3)
            except Exception as e:
                print(e)

            soup = BeautifulSoup(browser.html, 'lxml')

            for track in tracks:
                bingo = soup.find('article', attrs={'data-track-id' : track})
                if bingo:
                    number = bingo.find('span', {'class': 'number'}).text
                    title = bingo.find('div', {'class': 'title'}).find('a').text
                    artist = bingo.find('div', {'class': 'artist'}).find('a').text
                    print(f'{number} | {title} - {artist}')
                    tops.update({c: {'number': number, 'country': country, 'title': title, 'artist': artist, 'shazams': all_shazams[track]}})
                    c += 1

        write_csv(tops)


if __name__ == '__main__':
    main()
