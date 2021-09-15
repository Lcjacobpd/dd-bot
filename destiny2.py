'''
Process Destiny 2 related inquiries
'''
import re
import typing
import requests

from bs4 import BeautifulSoup
from datetime import date


def todays_news(message: str) -> str:
    '''Collect today's news'''
    if message.lower() != 'd2 news':
        return ""  # Not a destiny 2 search.
    else:
        print('  > Guardians make their own fate!')

    news = lost_sectors()
    news += '\n' + ask_ada()
    news += '\n' + ask_xur()

    # Review news for mentions.
    news += notify_who(news)

    return news


def lost_sectors() -> str:
    '''Collect daily lost sectors'''
    print('  > Scouring lost sectors...')

    url = 'https://kyberscorner.com/destiny2/lost-sectors/'
    today = date.today()
    format_date = f'{today.month}/{today.day}/{today.year}'
    resp = requests.get(url)

    if resp.status_code == 200:
        # Find today's sectors
        soup = BeautifulSoup(resp.text, 'html.parser')
        row = soup.find('td', text=format_date).parent

        # Format by tiers
        msg = ''
        sectors = ['Legend', 'Master']
        for cell in row:
            tier = ""
            place = ""
            if '(' in cell.text:
                tier = sectors.pop(0)
                test = cell.text.split('(')[0]
                place = cell.text.split('(')[0]#.title().replace(' ', '')
                msg += f'> **{tier} - {place}**\n'
            if ',' in cell.text:
                txt = f'{cell.text}'.replace(',', ':', 1)
                msg += f'> {txt}\n> \n'

            # Collect sector enemies by tier
            if place != "":
                sect_notes = soup.find('strong', text="Lost Sector").parent.parent.parent.find_all_next('a')
                for s in sect_notes:
                    if s.text == place:
                        champ = list(s.parent.parent)
                        
                enemies = '> *'
                patt = r'[A-Za-z]+: x[0-9]+'

                if tier == 'Legend':
                    enemies += ' '.join(re.findall(patt, champ[1].text))+' | '
                    enemies += ' '.join(re.findall(patt, champ[2].text))+'*\n'
                    
                elif tier == 'Master':
                    enemies += ' '.join(re.findall(patt, champ[3].text))+' | '
                    enemies += ' '.join(re.findall(patt, champ[4].text))+'*\n'

                msg += enemies

        return msg[:-3]
    else:
        return ""  # Error case.


def ask_ada() -> str:
    '''Collect daily Ada sales'''
    print('  > Contacting Ada...')

    url = 'https://www.todayindestiny.com/vendors'
    resp = requests.get(url)
    tagline = 'Advanced Prototype Exo and warden of the Black Armory.'

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        sales = soup.find('div', text=tagline).find_next('div', index=1)
        labels = sales.find_all_next('p', {'class': 'modPerkLabel'})
        flavors = sales.find_all_next('p', {
            'class': 'eventCardPerkDescription'})

        item = []
        for label in labels:
            item.append(label.text)

        desc = []
        for flavor in flavors:
            desc.append(flavor.text)

        ada = f'> **Ada-1 - {item[0]}**\n'
        ada += f'> {desc[0]}\n> \n'
        ada += f'> **Ada-1 - {item[2]}**\n'
        ada += f'> {desc[2]}'

        return ada
    else:
        return ""  # Error case.


def ask_xur():
    '''Collect Xur location and Sales if present'''
    print('  > Locating Xur... (TODO)\n')
    return ""
    # TODO: impliment Xur


def save_guardians() -> None:
    '''Save guardian reminders to file'''
    with open('guardians.txt', 'w') as out_file:
        for name, marks in guardians.items():
            out_file.write(f"{name}:{marks}\n")


def fetch_guardians() -> None:
    '''Recall guardian reminders from file'''
    try:
        print('  > Listing Guardians...')
        with open('guardians.txt', 'r') as in_file:
            lines = in_file.readlines()
            for line in lines:
                name = line[:-1].split(':')[0]
                marks = line[:-1].split(':')[1]
                guardians[name] = marks
    except:
        print('  > Lost to the dark corners of time!')


def new_reminder(user: str, message: str) -> str:
    '''Adde new reminder to guardian'''
    message = message.lower()                       # Just for Yoder.
    if message.startswith("remind me:") or message.startswith("pingus:"):
        print('  > Preparing reminder...')
    else:
        return ""  # Not a D2 reminder.

    new_rem = [i.strip() for i in message.split(':')[1].split(',')]

    # Perform union if already present.
    if user in guardians.keys():
        old_rem = [j.strip() for j in guardians[user].split(',')]
        new_rem = list(set(old_rem) | set(new_rem))

    guardians[user] = ",".join(new_rem)
    save_guardians()

    return f"> *{user}'s Reminders*\n> {guardians[user]}"


def clear_notices(user: str) -> str:
    '''Remove all guardian's notices'''
    message = message.lower()
    if message.startswith("clear reminders") or message.startswith("transmat firing"):
        print('  > Purging reminders...')
        guardians.pop(user, None)
        save_guardians()
        return "Reminders cleared"

    else:
        return ""  # Not a D2 clear reminder.


def notify_who(news: str) -> str:
    """ Search news for Guardian keywords"""
    informees = []
    for name, marks in guardians.items():
        for mark in marks.split(','):
            if mark.strip().lower() in news.lower():
                informees.append(name)
                break

    # Format @ mentions.
    mentions = ''
    for person in informees:
        mentions += f"@{person} "
    return "\n" + mentions


# 'name': 'mark1, mark2, ..'
guardians: typing.Dict[str, str] = {}
fetch_guardians()
#print(todays_news("d2 news"))
