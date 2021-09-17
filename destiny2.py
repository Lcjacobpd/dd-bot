"""
Process Destiny 2 related inquiries
"""
import re
import typing
import requests

from bs4 import BeautifulSoup
from datetime import date


class Destiny:
    def __init__(self, author: str, message: str):
        self.user: str = author
        self.message: str = message.lower().strip()
        self.guardians: typing.Dict[str, str] = {}

        if self.message.startswith("d2"):
            self.fetch_guardians()

    def check(self) -> str:
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
            # Find today"s sectors
            soup = BeautifulSoup(resp.text, "html.parser")
            row = soup.find("td", text=format_date).parent

            # Format by tiers
            msg = ""
            sectors = ["Legend", "Master"]
            for cell in row:
                tier = ""
                place = ""
                if "(" in cell.text:
                    tier = sectors.pop(0)
                    test = cell.text.split("(")[0]
                    place = cell.text.split("(")[0]#.title().replace(" ", "")
                    msg += f"> **{tier} - {place}**\n"
                if "," in cell.text:
                    txt = f"{cell.text}".replace(",", ":", 1)
                    msg += f"> {txt}\n> \n"

                # Collect sector enemies by tier
                try:
                    if place != "":
                        sect_notes = soup.find("strong", text="Lost Sector").parent.parent.parent.find_all_next("a")
                        for s in sect_notes:
                            if s.text == place:
                                champ = list(s.parent.parent)
                                
                        enemies = "> *"
                        patt = r"[A-Za-z]+: x[0-9]+"

                        if tier == "Legend":
                            enemies += " ".join(re.findall(patt, champ[1].text))+" | "
                            enemies += " ".join(re.findall(patt, champ[2].text))+"*\n"
                            
                        elif tier == "Master":
                            enemies += " ".join(re.findall(patt, champ[3].text))+" | "
                            enemies += " ".join(re.findall(patt, champ[4].text))+"*\n"

                        msg += enemies
                except:
                    print("  > Champions hidden...")

            return "\n" + msg[:-3]
        else:
            return ""  # Error case.

    def ask_ada(self, resp) -> str:
        """Collect daily Ada sales"""
        print("  > Contacting Ada...")
        tagline = "Advanced Prototype Exo and warden of the Black Armory."

        if resp.status_code == 200:
            # Parse page for Ada"s storefront.
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
            return ""  # Error case: page unreachable.

    def ask_xur(self, resp):
        """Collect Xur location and Sales if present"""
        print("  > Locating Xur... (TODO)\n")
        return ""
        # TODO: impliment Xur

    def new_bookmarks(self) -> str:
        """Adde new reminder to guardian"""
        print("  > Preparing reminder...")
        msg = self.message
        gdns = self.guardians
        new_mark = [m.strip() for m in msg.split(":")[1].split(",")]

        # Perform union if guardian already present.
        if self.user in self.guardians.keys():
            old_mark = [g.strip() for g in gdns[user].split(",")]
            new_mark = list(set(old_mark) | set(new_mark))

        self.guardians[self.user] = ",".join(new_mark)
        self.save_guardians()

        return f"> *{self.user}'s Reminders*\n> {self.guardians[self.user]}"

    def clear_bookmarks(self) -> str:
        """Remove all a guardian's bookmarks"""
        print(f"  > Purging {self.user}'s bookmarks...")
        self.guardians.pop(user, None)
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


d2 = Destiny("Jake", "d2 my marks")
print(d2.check())
