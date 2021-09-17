"""
Process Destiny 2 related inquiries
"""
import re
import typing
import requests

from bs4 import BeautifulSoup
from datetime import date


class Destiny:
    """Wrapper for Destiny 2 interactions"""
    def __init__(self, author: str, message: str):
        self.user: str = author
        self.message: str = message.lower().strip()
        self.guardians: typing.Dict[str, str] = {}

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
            return self.clear_bookmarks()

        # Display active bookmarks.
        if msg.startswith("d2 my marks"):
            return self.show_bookmarks()

        return ""  # Default/error case.

    def fetch_guardians(self) -> None:
        """Recall guardian bookmarks from file"""
        try:  # File may not exist.
            print("  > Fetching guardians...")
            with open("guardians.txt", "r") as in_file:
                lines = in_file.readlines()
                for line in lines:
                    name = line[:-1].split(":")[0]
                    marks = line[:-1].split(":")[1]
                    self.guardians[name] = marks
        except:
            print("  > Lost to the dark corners of time!")

    def save_guardians(self) -> None:
        """Save guardian bookmarks to file"""
        with open("guardians.txt", "w") as out_file:
            for name, marks in self.guardians.items():
                out_file.write(f"{name}:{marks}\n")

    def todays_news(self) -> str:
        """Collect today"s news"""
        print("  > Guardians make their own fate!")

        news: str = self.lost_sectors()

        # Fetch vendors page only once.
        url = "https://www.todayindestiny.com/vendors"
        resp = requests.get(url)

        news += self.ask_ada(resp)
        news += self.ask_spider(resp)
        news += self.ask_xur(resp)

        # Review news for bookmarks.
        news += self.notify_who(news)

        return news

    def lost_sectors(self) -> str:
        """Collect daily lost sectors"""
        print("  > Scouring lost sectors...")

        url = "https://kyberscorner.com/destiny2/lost-sectors/"
        resp = requests.get(url)
        today = date.today()
        format_date = f"{today.month}/{today.day}/{today.year}"

        if resp.status_code == 200:
            # Find today's sectors.
            soup = BeautifulSoup(resp.text, "html.parser")
            row = soup.find("td", text=format_date).parent

            # Format by tiers.
            msg = ""
            sectors = ["Legend", "Master"]
            for cell in row:
                tier = ""
                place = ""
                if "(" in cell.text:
                    tier = sectors.pop(0)
                    place = cell.text.split("(")[0]
                    msg += f"> **{tier} - {place}**\n"
                if "," in cell.text:
                    msg += f"> {cell.text.replace(',', ':', 1)}\n> \n"

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
                patt = r"[A-Za-z]+: x[0-9]+"

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

            xur = "\n> **Xur - Exotics**\n"
            for ex in exotics:
                desc = ex.find_next("p", {"class": "eventCardPerkDescription"}).text
                xur += f"> {ex.text}: *{desc}*\n"

            # Process legendary weapons & their mods.
            xur += ">\n> ** Xur - Legendaries**\n"
            for leg in legends:
                perks = leg.find_all_next("div", {"class": "eventCardPerkItemContainer"})[1:3]
                xur += f"> {leg.text}: *"
                for perk in perks:
                    xur += perk.text + " | "

                xur = xur[:-3]
                xur += "*\n"

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
        if self.user in self.guardians.keys():
            old_mark = [g.strip() for g in gdns[self.user].split(",")]
            new_mark = list(set(old_mark) | set(new_mark))

        self.guardians[self.user] = ",".join(new_mark)
        self.save_guardians()

        return f"> *{self.user}'s Reminders*\n> {self.guardians[self.user]}"

    def clear_bookmarks(self) -> str:
        """Remove all a guardian's bookmarks"""
        print(f"  > Purging {self.user}'s bookmarks...")
        self.guardians.pop(self.user, None)
        self.save_guardians()

        return f"@{self.user} Reminders cleared"

    def show_bookmarks(self) -> str:
        """Show a guardian's bookmarks"""
        print(f"  > Displaying {self.user}'s bookmarks...")
        marks = self.guardians[self.user].split(",")
        msg = f"@{self.user} has bookmarked:"

        for mark in marks:
            msg += f"\n> {mark}"

        return msg

    def notify_who(self, news: str) -> str:
        """ Search news for Guardian keywords"""
        informees = []
        for name, marks in self.guardians.items():
            for mark in marks.split(","):
                if mark.strip().lower() in news.lower():
                    informees.append(name)
                    break

        # Format @ mentions.
        mentions = ""
        for person in informees:
            mentions += f"@{person} "
        return "\n" + mentions


# d2 = Destiny("Jake", "d2 news")
# print(d2.check())
# print()
# d2 = Destiny("Yoder", "d2 my marks")
# print(d2.check())
