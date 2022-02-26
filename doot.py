import re
import typing
import requests

from datetime import date
from bs4 import BeautifulSoup

from guardian import Guardian
from response import Response, ResponseCodes
from utils import inline_length, format_inline


#region Emojis
lost_sector = '<:d2_lsec:908482349916909628>'
ada_icon    = '<:d2_ada:908482465360924753>'
xur_icon    = '<:d2_xur:908482481353810001>'
trials_icon = '<:d2_osi:908482512387448862>'
spider_icon = '<:d2_spi:908482383546822686>'

unstoppable = '<:d2_ust:908456357076799538>'
barrier     = '<:d2_bar:908455916234502245>'
overload    = '<:d2_ovl:908456149702029313>'

solar = '<:d2_solar:908458507735547954>'
void  = '<:d2_void:908458519550898197>'
arc   = '<:d2_arc:908458495983091743>'

clr = '<:clear:920007120513024030>'
#endregion


class Doot():
    Message: str
    Discord: str
    Name: str
    Guardians: typing.Dict[str, Guardian]

    # Constructor
    def __init__(self, author, message: str) -> None:
        self.Discord   = f"{author}#{author.id}"
        self.Name      = author.name
        self.Message   = message.lower().strip()
        self.Guardians = {}

        # Collect guardian details
        if self.Message.startswith("d2"):
            self.FetchGuardians()

    def Check(self) -> "Response":
        message = self.Message.lower()

        if message == "d2 news":
            return self.TodaysNews()

        if message.startswith("d2 bookmark:"):
            return self.NewBookmark()

        if message.startswith("d2 clear"):
            return self.ClearBookmarks()

        if message == "d2 my marks":
            return self.ShowBookmarks()

        if message == "d2 help":
            return self.AboutMe()

        # Default, error case.
        return Response(responseCode=ResponseCodes.error)

    def AboutMe(self) -> "Response":
        # d2 help command list.
        about  = "```\nD2 COMMANDS:\n"
        about += "============\n"
        about += "d2 news             -  Show daily news    \n"
        about += "d2 bookmark: a, b.. -  Add new bookmark(s)\n"
        about += "d2 my marks         -  Show all bookmarks \n"
        about += "d2 clear            -  Clear all bookmarks\n"
        about += "d2 clear: a, b..    -  Clear mark(s)      \n```"

        return Response(message=about)

    #region News
    def TodaysNews(self) -> "Response":
        # Collect today's news.
        print("  > Decrypting Engrams...")
        today = date.today()
        format_date = f"{today.month}/{today.day}/{today.year}"
        dotw = today.strftime("%A")

        # Fetch vendors page.
        url  = "https://www.todayindestiny.com/vendors"
        resp = requests.get(url)
        vendors  = self.AskAda(resp)

        # Grab Xur if it's weekend.
        if dotw in ["Friday", "Saturday", "Sunday", "Monday"]:
            vendors += self.AskXur(resp)
        else: print("  > Skipping Xur...")

        news = self.NotifyWho(vendors)
        return Response(news)

    def NotifyWho(self, news: str) -> str:
        #Search news for Guardian keywords.
        informees = []
        for name, newlight in self.Guardians.items():
            for mark in newlight.Bookmarks:
                if mark.strip().lower() in news.lower():
                    news = re.sub(f"_?_?{mark}_?_?", f"__{mark}__", news)
                    informees.append(name)

        # Format @ mentions.
        mentions = "\n"
        for person in informees:
            mentions += f"<@!{person.split('#')[2]}> "
        return news + mentions
    #endregion

    #region Vendors
    def AskAda(self, resp) -> str:
        # Collect daily Ada-1 sales.
        print("  > Contacting Ada...")
        tagline = "Advanced Prototype Exo and warden of the Black Armory."

        if resp.status_code == 200:
            # Parse page for Ada's storefront.
            soup  = BeautifulSoup(resp.text, "html.parser")
            sales = soup.find("div", text=tagline).find_next("div", index=2)
            labels  = sales.find_all_next("p", {"class": "modPerkLabel"})
            flavors = sales.find_all_next("p", {
                "class": "eventCardPerkDescription"})

            # Collect item names and descriptions.
            item = []
            for label in labels:
                item.append(label.text)

            desc = []
            for flavor in flavors:
                desc.append(flavor.text)

            ada =  f"> {ada_icon} **Ada-1 - {item[0]}**\n"
            ada += f"> {desc[0]}\n> \n"
            ada += f"> {ada_icon} **Ada-1 - {item[2]}**\n"
            ada += f"> {desc[2]}\n> \n"
            ada += f"> {ada_icon} **Ada-1 - {item[4]}**\n"
            ada += f"> {desc[4]}\n> \n"
            ada += f"> {ada_icon} **Ada-1 - {item[6]}**\n"
            ada += f"> {desc[6]}"

            return f"\n{ada}"
        else:
            print("  > Vendor unavailable...")
            return f"> {ada_icon} **Ada-1 - Unavailable"

    def AskXur(self, resp):
        # Collect Xur location and Sales if present.
        print("  > Locating Xur...")
        tagline = "A peddler of strange curios, Xûr's motives are not his own. He bows to his distant masters, the Nine."

        if resp.status_code == 200:
            # Parse page for Xur's storefront.
            soup = BeautifulSoup(resp.text, "html.parser")
            sales = soup.find("p", text="Xûr")

            # Xur may not be available.
            try:
                # Fetch location.
                location = sales.findNext("div", {"class": "eventCardDescription"}).text
                location = re.findall(r"Location:?[ ]+(.+)", location, re.IGNORECASE)[0]

                # Gather exotics and legendary weapons.
                exotics = sales.find_next("div", index=0).find_all_next("p", {
                    "class": "itemTooltip_itemName"})[2:10:2]
                legends = sales.find_next("div", index=2).find_all_next("p", {
                    "class": "itemTooltip_itemName"})[0:14:2]
            except:
                print("  > Vendor unavailable...")
                return ""

            xur = f"> {xur_icon} **Xur - Exotics ({location})**\n"
            for ex in exotics:
                desc = ex.find_next("p", {"class": "eventCardPerkDescription"}).text
                xur += f"> {ex.text}: *{desc}*\n"

            # Process legendary weapons & their mods.
            xur += f"> \n > {xur_icon} ** Xur - Legendaries ({location})**\n"
            items = []
            tags = []
            for leg in legends:
                perks = leg.find_all_next("div", {"class": "eventCardPerkItemContainer"})[1:3]
                items.append(leg.text) #
                tags.append("*"+ perks[0].text +", "+ perks[1].text +"*")

            lines = format_inline(items).split(":")[:-1]
            for i, line in enumerate(lines):
                xur += f"> {line}" + tags[i] + "\n"

            return "\n\n" + xur

        print("  > Vendor unavailable...")
        return f"> {xur_icon} **Xur - Unavailable**\n"
    #endregion

    #region Bookmarks
    def ShowBookmarks(self) -> "Response":
        # Show a guardian's bookmarks
        print(f"  > Displaying {self.Name}'s bookmarks...")

        if len(self.Guardians) == 0: return Response("> **ERROR** - Lost to the dark corners of time!")

        if self.Discord in self.Guardians.keys():            
            newlight = ', '.join(self.Guardians[self.Discord].Bookmarks)
            return Response(f"> *{self.Name}'s bookmarks:*\n> {newlight}")
        else:
            return Response(f"> No bookmarks found for {self.Name}")

    def ClearBookmarks(self) -> "Response":
        # Remove all/select guardian's bookmarks.
        items = re.sub(r"d2 clear:*", "", self.Message).strip()
        items = [i.strip() for i in items.split(",")] if len(items) > 0 else []

        if self.Discord in self.Guardians.keys():
            if items != []:
                for i in items:
                    if i in self.Guardians[self.Discord].Bookmarks:
                        self.Guardians[self.Discord].Bookmarks.remove(i)

                self.SaveGuardians()
                return self.ShowBookmarks()

            #else
            print(f"  > Purging {self.Name}'s bookmarks...")
            self.Guardians.pop(self.Discord, None)
            self.SaveGuardians()
            return Response(f"{self.Name}'s reminders cleared")
        else:
            return Response("Already done")

    def NewBookmark(self) -> "Response":
        # Add new bookmark for guardian
        print("  > Bookmarking page...")
        msg = self.Message
        newlights = self.Guardians
        new_marks = [m.strip() for m in msg.split(":")[1].split(",")]

        # Perform union if guardian already present.
        if str(self.Discord) in self.Guardians.keys():
            old_marks = newlights[self.Discord].Bookmarks
            new_marks = list(set(old_marks) | set(new_marks))

        self.Guardians[str(self.Discord)] = Guardian(F"{self.Discord}:{','.join(new_marks)}\n")
        self.SaveGuardians()
        return self.ShowBookmarks()
    #endregion
        
    #region Guardian Operations
    def FetchGuardians(self) -> None:
        # Read details from file.
        try:
            self.Guardians = {}
            print("  > Fetching guardians...")
            with open("./guardians.txt", "r") as in_file:
                lines = in_file.readlines()
                for line in lines:
                    discord = line.split(":")[0]
                    self.Guardians[discord] = Guardian(line)
            print("  > Guardians make their own fate!")

        except:
            # No guardians found for one reason or another.
            print("  > Lost to the dark corners of time!")

    def SaveGuardians(self) -> None:
        # Save details to file.
        with open("./guardians.txt", "wt") as out_file:
            for name, newlight in self.Guardians.items():
                out_file.write(f"{name}:{','.join(newlight.Bookmarks)}\n")
    #endregion
