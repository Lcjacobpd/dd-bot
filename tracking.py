import settings
import json
from enum import Enum
from reaction import CustomEmoji
from settings import InventoryAction




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
        icon = CustomEmoji.D2Emojis[self.item] if self.item in CustomEmoji.D2Emojis else ""
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
            icon = CustomEmoji.D2Emojis[item] if item in CustomEmoji.D2Emojis else ""
            self.response += F"> {icon} *{self.data[self.user][item]} {item}*\n"
