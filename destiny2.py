"""
Process Destiny 2 related inquiries
"""
import re
import typing
import requests

from bs4 import BeautifulSoup
from datetime import date


def group_one(match_obj):
    """Return first group of match object"""
    return match_obj.group(1)

def inline_length(msg: str):
    """Calculate in-line length"""
    uppers = [
        4, 2.6, 3.6, 3.6, 2.6, 2.6, 3.6, 3.6, 1, 2.6,
        3, 2.6, 5.6, 3.6, 3.65, 3, 3.65, 3, 2.8, 3,
        3.6, 3.4, 5.6, 3.3, 3, 3

    ]
    lowers = [
        3, 2.6, 2.6, 3, 2.3, 1.6, 3, 2.6, 1.6, 1.6,
        2.3, 1.6, 4.3, 2.6, 3, 2.6, 3, 1, 2.3, 1.6,
        2.3, 3, 4.3, 2.3, 2.6, 2.6
    ]

    length = 0
    for char in msg:
        if char.isupper():
            length += uppers[ord(char) - ord('A')]
        elif char.islower():
            length += lowers[ord(char) - ord('a')]
        elif char == " ":
            length += 2
        else:
            length += 1.5

    return round(round(length) * .87)

def format_inline(msgs: list):
    """Format text for 'two-column' display"""
    length = 0
    for msg in msgs:
        l = inline_length(msg)
        length = l if l > length else length

    formatted = ""
    for msg in msgs:
        formatted += msg + (" " * (length - inline_length(msg) +3)) + ":"

    return formatted


class Destiny:
    """Wrapper for Destiny 2 interactions"""
    def __init__(self, author, message: str):
        self.user: str = f"{author}#{author.id}"
        self.name: str = author.name
        self.message: str = message.lower().strip()
        self.guardians: typing.Dict[str, list] = {}

        if self.message.startswith("d2"):
            self.fetch_guardians()

    def check(self) -> str:
        """Return inquiry results"""
        msg = self.message
        # News case.
        if msg.lower() == "d2 news":
            return self.todays_news()

        # Add bookmark(s) case.
        if msg.startswith("d2 bookmark:"):
            return self.new_bookmarks()

        # Remove bookmarks case.
        if msg.startswith("d2 clear"):
            items = re.sub("d2 clear:*", "", msg).strip()
            items = [i.strip() for i in items.split(",")] if len(items) > 0 else []
            return self.clear_bookmarks(items)

        # Display active bookmarks.
        if msg.startswith("d2 my marks"):
            return self.show_bookmarks()

        # Display command list/functions.
        if msg.startswith("d2 help"):
            return self.about_me()

        return ""  # Default/error case.

    def fetch_guardians(self) -> None:
        """Recall guardian bookmarks from file"""
        try:
            print("  > Fetching guardians...")
            with open("guardians.txt", "r") as in_file:
                lines = in_file.readlines()
                for line in lines:
                    name = line[:-1].split(":")[0]
                    marks = line[:-1].split(":")[1].split(",")
                    self.guardians[name] = marks
        except:
            print("  > Lost to the dark corners of time!")

    def save_guardians(self) -> None:
        """Save guardian bookmarks to file"""
        with open("guardians.txt", "w") as out_file:
            for name, marks in self.guardians.items():
                out_file.write(f"{name}:{','.join(marks)}\n")

    def todays_news(self) -> str:
        """Collect today"s news"""
        print("  > Guardians make their own fate!")
        today = date.today()
        format_date = f"{today.month}/{today.day}/{today.year}"
        doth = today.strftime("%A")

        news: str = self.lost_sectors(format_date)

        # Check for Trials news if available.
        if doth in ["Friday", "Saturday", "Sunday", "Monday"]:
            news += self.trials()
        else:
            print("  > Skipping Trials...")


        # Fetch vendors page only once.
        url = "https://www.todayindestiny.com/vendors"
        resp = requests.get(url)

        news += self.ask_ada(resp)
        news += self.ask_spider(resp)

        # Grab Xur if weekend.
        if doth in ["Friday", "Saturday", "Sunday"]:
            news += self.ask_xur(resp)
        else:
            print("  > Skipping Xur")

        # Review news for bookmarks.
        news += self.notify_who(news)

        return news

    def lost_sectors(self, format_date) -> str:
        """Collect daily lost sectors"""
        print("  > Scouring lost sectors...")

        url = "https://kyberscorner.com/destiny2/lost-sectors/"
        resp = requests.get(url)
        
        if resp.status_code == 200:
            # Find today's sectors.
            soup = BeautifulSoup(resp.text, "html.parser")
            row = soup.find("td", text=format_date).parent.find_all_next("td")[0:7]

            # Format by tiers.
            msg = ""
            sectors = ["Legend", "Master"]
            cells_text = [c.text for c in row]

            for n, cell in enumerate(cells_text):             
                tier = ""
                place = ""

                # Sector name
                if n == 1 or n == 4:
                    tier = sectors.pop(0)
                    place = re.sub(
                        r"([A-Za-z 0-9]+)(\({0,1}[A-Z]{1}[a-z]+\){0,1})",
                        group_one,
                        cell
                    ).strip()
                    msg += f"> **{tier} - {place}**\n"
                
                # Sector rewards
                elif "," in cell:
                    msg += f"> {cell.replace(',', ':', 1)}\n> \n"

                # Try for additional details.
                msg += self.sector_enemies(soup, place, tier)

            return "\n" + msg[:-3]
        else:
            return ""  # Error case: page unreachable.

    def sector_enemies(self, soup, place, tier):
        """Try to collect champion details if known"""
        msg = ""
        try:
            if place != "":
                sect_notes = soup.find("strong", text="Lost Sector")
                sect_notes = sect_notes.parent.parent.parent
                sect_notes = sect_notes.find_all_next("a")
                for note in sect_notes:
                    if note.text == place:
                        champ = list(note.parent.parent)

                enemies = "> *"
                patt = r"[A-Za-z:]+ x[0-9]+"

                # Collect sector enemies by tier.
                if tier == "Legend":
                    enemies += " ".join(re.findall(patt, champ[1].text))+" | "
                    enemies += " ".join(re.findall(patt, champ[2].text))+"*\n"

                elif tier == "Master":
                    enemies += " ".join(re.findall(patt, champ[3].text))+" | "
                    enemies += " ".join(re.findall(patt, champ[4].text))+"*\n"

                msg += enemies
        except:
            print("  > Champions hidden...")
            msg = "> *Champions unknown | Shields unknown*\n"

        return msg

    def trials(self) -> str:
        """Collect Trials of Osiris news"""
        url = "https://kyberscorner.com/destiny2/trialsofosiris/"
        resp = requests.get(url)
        

        if resp.status_code == 200:
            # Find today's sectors.
            soup = BeautifulSoup(resp.text, "html.parser")
            trial = soup.find_all("strong", text="Map: ")[0].parent
            map = " ".join(trial.text.split(" ")[1:]).strip()
            reward = trial.find_all_next("strong")[1].find_next("a").text

            osiris = "> **Trials of Osiris**\n"
            osiris += f"> *{map}*\n"
            osiris += f"> Flawless Reward: {reward}\n"

        return "\n" + osiris

    def ask_ada(self, resp) -> str:
        """Collect daily Ada sales"""
        print("  > Contacting Ada...")
        tagline = "Advanced Prototype Exo and warden of the Black Armory."

        if resp.status_code == 200:
            # Parse page for Ada's storefront.
            soup = BeautifulSoup(resp.text, "html.parser")
            sales = soup.find("div", text=tagline).find_next("div", index=1)
            labels = sales.find_all_next("p", {"class": "modPerkLabel"})
            flavors = sales.find_all_next("p", {
                "class": "eventCardPerkDescription"})

            # Collect item names and descriptions.
            item = []
            for label in labels:
                item.append(label.text)

            desc = []
            for flavor in flavors:
                desc.append(flavor.text)

            ada = f"> **Ada-1 - {item[0]}**\n"
            ada += f"> {desc[0]}\n> \n"
            ada += f"> **Ada-1 - {item[2]}**\n"
            ada += f"> {desc[2]}"

            return "\n" + ada
        else:
            print("  > Vendor unavailable...")
            return ""  # Error case: page unreachable.

    def ask_spider(self, resp):
        """Collect Spider's glimmer trade"""
        print("  > Bribing Spider...")
        tagline = "Unlike his Fallen brethren, the clever Spider prefers to negotiate instead of fight."

        if resp.status_code == 200:
            # Parse page for Spider's storefront.
            soup = BeautifulSoup(resp.text, "html.parser")
            sales = soup.find("div", text=tagline).find_next("div", index=3)
            currency = sales.find_all_next("p", {"class": "tooltipCostName"})
            cost = sales.find_all_next("p", {"class": "tooltipCostQuantity"})

            spider = "\n> **Spider - Glimmer Trade**\n"
            spider += f"> {cost[5].text} {currency[5].text}\n"

            return "\n" + spider
        else:
            print("  > Vendor unavailable...")
            return ""  # Error case: page unreachable.

    def ask_xur(self, resp):
        """Collect Xur location and Sales if present"""
        print("  > Locating Xur...")
        tagline = "A peddler of strange curios, Xûr's motives are not his own. He bows to his distant masters, the Nine."

        if resp.status_code == 200:
            # Parse page for Xur's storefront.
            soup = BeautifulSoup(resp.text, "html.parser")
            sales = soup.find("div", text=tagline)

            # Xur may not be available.
            try:
                # Gather exotics and legendary weapons.
                exotics = sales.find_next("div", index=0).find_all_next("p", {
                    "class": "itemTooltip_itemName"})[2:10:2]
                legends = sales.find_next("div", index=2).find_all_next("p", {
                    "class": "itemTooltip_itemName"})[0:14:2]
            except:
                print("  > Vendor unavailable...")
                return ""

            xur = "> **Xur - Exotics**\n"
            for ex in exotics:
                desc = ex.find_next("p", {"class": "eventCardPerkDescription"}).text
                xur += f"> {ex.text}: *{desc}*\n"

            # Process legendary weapons & their mods.
            xur += "> \n > ** Xur - Legendaries**\n"
            items = []
            tags = []
            for leg in legends:
                perks = leg.find_all_next("div", {"class": "eventCardPerkItemContainer"})[1:3]
                items.append(leg.text) #
                tags.append("*"+ perks[0].text +", "+ perks[1].text +"*")

            lines = format_inline(items).split(":")[:-1]
            for i, line in enumerate(lines):
                xur += f"> {line}" + tags[i] + "\n"

            return "\n" + xur

        print("  > Vendor unavailable...")
        return ""

    def new_bookmarks(self) -> str:
        """Add new reminder to guardian"""
        print("  > Preparing reminder...")
        msg = self.message
        gdns = self.guardians
        new_mark = [m.strip() for m in msg.split(":")[1].split(",")]

        # Perform union if guardian already present.
        if str(self.user) in self.guardians.keys():
            old_mark = gdns[str(self.user)]
            new_mark = list(set(old_mark) | set(new_mark))

        self.guardians[str(self.user)] = new_mark
        self.save_guardians()

        #user = self.user.split('#')[0]
        return self.show_bookmarks() #f"> *{user}'s bookmarks:*\n> {self.guardians[str(self.user)]}"

    def clear_bookmarks(self, items:list = []) -> str:
        """Remove all/select guardian's bookmarks"""
        if self.user in self.guardians.keys():
            if items != []:
                for i in items:
                    if i in self.guardians[str(self.user)]:
                        self.guardians[str(self.user)].remove(i)

                self.save_guardians()
                return self.show_bookmarks()

            #else
            print(f"  > Purging {self.name}'s bookmarks...")
            self.guardians.pop(str(self.user), None)
            self.save_guardians()
            return f"{self.name}'s reminders cleared"
        else:
            return "Already done"

    def show_bookmarks(self) -> str:
        """Show a guardian's bookmarks"""
        print(f"  > Displaying {self.name}'s bookmarks...")

        if str(self.user) in self.guardians.keys():            
            items = self.guardians[str(self.user)]
            return f"> *{self.name}'s bookmarks:*\n> {', '.join(items)}"
        else:
            return f"> No bookmarks found for {self.name}"

    def notify_who(self, news: str) -> str:
        """Search news for Guardian keywords"""
        informees = []
        for name, marks in self.guardians.items():
            for mark in marks:
                if mark.strip().lower() in news.lower():
                    informees.append(name)
                    break

        # Format @ mentions.
        mentions = ""
        for person in informees:
            mentions += f"<@!{person.split('#')[2]}> "
        return "\n" + mentions

    def about_me(self):
        """Commmands list"""
        about  = "> ```D2 COMMANDS:\n"
        about += "> ============\n"
        about += "> d2 news              -  Show current daily items\n"
        about += "> d2 bookmark: a, b..  -  Add new bookmark(s)\n"
        about += "> d2 my marks          -  Show my current bookmarks\n"
        about += "> d2 clear             -  Clear all bookmarks\n"
        about += "> d2 clear: a, b..     -  Clear specific bookmarks```"

        return about
