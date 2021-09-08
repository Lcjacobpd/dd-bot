from asyncio.windows_events import NULL
from os import readlink
import re
import requests
from bs4 import BeautifulSoup
from datetime import date

def today(message: str):
    if message != 'D2':
        return NULL  # Not a destiny 2 search
    else:
        print('  > Guardians make their own fate!')

    news = LostSectors()
    news += '\n'
    news += Ada()

    return news

def LostSectors():
    print('  > Scouring lost sectors...')

    url = 'https://kyberscorner.com/destiny2/lost-sectors/'
    today = date.today()
    format_date = f'{today.month}/{today.day}/{today.year}'
    resp = requests.get(url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        row = soup.find('td', text=format_date).parent

        msg = ''
        sectors = ['Legend', 'Master']
        for cell in row:
            if '(' in cell.text:
                msg += f'> **{sectors.pop(0)} - {cell.text}**\n'
            if ',' in cell.text:
                txt = f'{cell.text}'.replace(',', ':', 1)
                msg += f'> {txt}\n> \n'

        return msg[:-3]


def Ada():
    print('  > Contacting Ada...')

    url = 'https://www.todayindestiny.com/vendors'
    resp = requests.get(url)
    tagline = 'Advanced Prototype Exo and warden of the Black Armory.'

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        sales = soup.find('div', text=tagline).find_next('div', index=1)
        labels = sales.find_all_next('p', {'class': 'modPerkLabel'})
        flavor = sales.find_all_next('p', {'class': 'eventCardPerkDescription'})
        
        item = []
        for l in labels:
            item.append(l.text)

        desc = []
        for f in flavor:
            desc.append(f.text)

        ada = f'> **Ada-1 - {item[0]}**\n'
        ada += f'> {desc[0]}\n> \n'
        ada += f'> **Ada-1 - {item[2]}**\n'
        ada += f'> {desc[2]}'

        return ada


#def Xur():
