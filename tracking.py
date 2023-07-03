import settings
import json
from enum import Enum
from reaction import CustomEmoji
from settings import InventoryAction
from settings import MoteAction


class item_handler:
    data = {}
    response = ""

    def __init__(self, user:str, action: InventoryAction, quantity: int=0, item: str=""):
        self.user     = str(user)
        self.action   = InventoryAction(action)
        self.quantity = int(quantity)
        self.item     = str(item)
        self.ReadFromFile()

        if action is InventoryAction.Add:
            self.AddAmount()
        elif action is InventoryAction.Subtract:
            self.SubtractAmount()
        elif action is InventoryAction.Total:
            self.DisplayAmounts()

    #region FileCommands

    def ReadFromFile(self):
        file = open(settings.DATA_FILE)
        self.data = json.load(file)
        
    def WriteToFile(self):
        jsonFile = open(settings.DATA_FILE, "w")
        jsonFile.write(json.dumps(self.data))
        jsonFile.close()

    #endregion
    
    #region Responses

    def InformEmpty(self):
        print("  > None found...")
        self.response = "> *No inventory found...*\n > *Try:* `/add <quantity> <item>`"

    def GenerateReceipt(self):
        sign = "+" if self.action == InventoryAction.Add else "-"
        icon = CustomEmoji.d2_emojis[self.item] if self.item in CustomEmoji.d2_emojis else ""
        newTotal = self.data[self.user][self.item]

        receipt = F"> *{sign}{self.quantity}* {icon}\n"
        receipt += F"> {newTotal} {self.item}"
        self.response = receipt

    #endregion

    def AddAmount(self):
        if self.user not in list(self.data.keys()):
            print(F"  > Adding {self.user}...")
            self.data[self.user] = {}
            self.data[self.user][self.item] = 0
        if self.item not in list(self.data[self.user].keys()):
            self.data[self.user][self.item] = 0

        print(F"  > Adding {self.item} for {self.user}...")
        self.data[self.user][self.item] += self.quantity
        self.GenerateReceipt()
        self.WriteToFile()

    def SubtractAmount(self):
        if self.user not in list(self.data.keys()):
            self.InformEmpty()
            return
        
        # Catch overdraw
        if self.data[self.user][self.item] < self.quantity:
            print("  > Overdraw detected...")
            self.response = "> *Negative balance detenced... Cancelling*"
            return

        print(F"  > Subtracting {self.item} for {self.user}...")
        self.data[self.user][self.item] -= self.quantity
        self.GenerateReceipt()
        self.WriteToFile()

    def DisplayAmounts(self):
        # No inventory found, bail early
        if self.user not in list(self.data.keys()):
            self.InformEmpty()
            return

        print(F"  > Fetching inventory for {self.user}...")
        for item in self.data[self.user]:
            icon = CustomEmoji.d2_emojis[item] if item in CustomEmoji.d2_emojis else ""
            self.response += F"> {icon} *{self.data[self.user][item]} {item}*\n"


class mote_handler:
    data = {}
    response = ""

    def __init__(self, action: MoteAction, owner: str="", quantity: int=""):
        self.owner    = str(owner)
        self.quantity = 0
        self.action   = MoteAction(action)
        self.ReadFromFile()

        if action is MoteAction.Collect:
            self.quantity = int(quantity)
            self.Collect()
        elif action is MoteAction.Deposit:
            self.Deposit()
        elif action is MoteAction.Reset:
            self.Reset()

    #region FileCommands

    def ReadFromFile(self):
        file = open(settings.MOTES_FILE)
        self.data = json.load(file)
        
    def WriteToFile(self):
        jsonFile = open(settings.MOTES_FILE, "w")
        jsonFile.write(json.dumps(self.data))
        jsonFile.close()

    #endregion

    #region Responses

    def InformEmpty(self):
        print("  > None found...")
        self.response = "> *Nice try, go collect some motes first...*"

    def GenerateReceipt(self):
        receipt = ""
        if self.action == MoteAction.Collect:
            receipt = F"*You're full up on motes, go deposit them!*\n" if self.data[self.owner] == 15 else "*Collecting motes...*\n"
        elif self.action == MoteAction.Deposit:
            if   self.data[self.owner] == 15: receipt = "*Large blocker going to the other side!*\n"
            elif self.data[self.owner] >= 10: receipt = "*Medium blocker going to the other side!*\n"
            elif self.data[self.owner] >= 5:  receipt = "*Small block going to the other side!*\n"
            else: receipt = "*Depositing motes...*\n"

            # Remove deposited motes
            self.data[self.owner] = 0
        else:
            receipt = "*Mote bank reset...*\n"
            self.response = receipt
            return

        receipt += F"> **Mote Bank:** \n"
        for owner in self.data.keys():
            receipt += F"> {CustomEmoji.d2_mote} {self.data[owner]: >2}\t{owner}\n"
        self.response = receipt

    #endregion

    def Collect(self):
        if self.owner not in list(self.data.keys()):
            print(F"  > Adding {self.owner}...")
            self.data[self.owner] = 0

        print(F"  > Adding {self.quantity} motes for {self.owner}...")
        self.data[self.owner] += self.quantity
        if self.data[self.owner] > 15: self.data[self.owner] = 15
        self.GenerateReceipt()
        self.WriteToFile()

    def Deposit(self):
        if self.owner not in list(self.data.keys()) or self.data[self.owner] == 0:
            self.InformEmpty()
            return

        print(F"  > Depositing {self.data[self.owner]} motes from {self.owner}...")
        self.GenerateReceipt()
        self.data[self.owner] = 0
        self.WriteToFile()

    def Reset(self):
        for owner in self.data.keys():
            self.data = {}
        self.GenerateReceipt()
        self.WriteToFile()
