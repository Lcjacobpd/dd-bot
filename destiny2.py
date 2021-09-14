import re
import requests
from bs4 import BeautifulSoup
from datetime import date

def todaysNews(message: str) -> str:
    if message.lower() != 'd2 news':
        return None  # Not a destiny 2 search.
    else:
        print('  > Guardians make their own fate!')

    news = LostSectors()
    news += '\n' + Ada()
    news += '\n' + Xur()

    # Review news for mentions.
    news += NotifyWho(news)

    return news

def LostSectors() -> str:
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
                place = cell.text.split('(')[0].replace(' ', '')
                msg += f'> **{tier} - {place}**\n'
            if ',' in cell.text:
                txt = f'{cell.text}'.replace(',', ':', 1)
                msg += f'> {txt}\n> \n'

            # Collect sector enemies by tier
            if place != "":     
                entry = soup.find_all('a', {'href': "http://kyber3000.com/LS-"+place})[-1].parent.parent
                champ = [c for c in entry]
                enemies = '> *'

                if tier == 'Legend':
                    enemies += ' '.join(re.findall(r'[A-Za-z]+: x[0-9]+', champ[1].text)) + ' | '
                    enemies += ' '.join(re.findall(r'[A-Za-z]+: x[0-9]+', champ[2].text)) + '*\n'
                elif tier == 'Master':
                    enemies += ' '.join(re.findall(r'[A-Za-z]+: x[0-9]+', champ[3].text)) + ' | '
                    enemies += ' '.join(re.findall(r'[A-Za-z]+: x[0-9]+', champ[4].text)) + '*\n'
                               
                msg += enemies

        return msg[:-3]

def Ada() -> str:
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


def Xur():
    print('  > Locating Xur... (TODO)\n')
    return ""
    # TODO: impliment Xur


def saveGuardians() -> None:
    with open('guardians.txt', 'w') as out_file:
        for name, marks in guardians.items():
            out_file.write(f"{name}:{marks}\n")
    
def fetchGuardians() -> None:
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


# 'name': 'mark1, mark2, ..'
#guardians = {}
#fetchGuardians()


def newReminder(user: str, message: str) -> str:
    """Add d2 reminder for user"""                       # Just for Yoder.
    if message.toLowerCase().startswith("remind me:") or message.toLowerCase().startswith("pingus:"):
        print('  > Preparing reminder...')
    else:
        return None # Not a D2 reminder.

    newI = [i.strip() for i in message.split(':')[1].split(',')]

    # Perform union if already present.
    if user in guardians.keys():
        oldI = [j.strip() for j in guardians[user].split(',')]
        newI = list(set(oldI) | set(newI))

    guardians[user] = ",".join(newI)
    saveGuardians()

    return f"> *{user}'s Reminders*\n> {guardians[user]}"

def clearNotice(user: str) -> None:
    """Remove guardian & all notices"""
    if message.toLowerCase().startswith("clear reminders") or message.toLowerCase().startswith("transmat firing"):
        print('  > Purging reminders...')
        guardians.pop(user, None)
        saveGuardians()
        return "Reminders cleared"
        
    else:
        return None # Not a D2 clear reminder.
    
    
    
def NotifyWho(news: str) -> str:
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

guardians = {}
print(todaysNews("d2 news"))