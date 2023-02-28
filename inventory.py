import re
import json
from enum import Enum
from reaction import CustomEmoji


"""
GLOBAL INVENTORY COMMAND RECOGNITION PATTERNS
Base:
- The '#' symbol followed by
- The command name
Optional:
- An integer quantity and
- The name of the record to update
"""
LISTCOMMAND = r"#loot|#stuff"
ADDCOMMAND  = r"#add[\d]+(?:gl|van|cru|cry)"
SUBCOMMAND  = r"#(?:remove|sub)[\d]+(?:gl|van|cru|cry)"
PATTERN = f"(?:{LISTCOMMAND})|(?:{ADDCOMMAND})|(?:{SUBCOMMAND})"


"""
FULL NAME MAPPINGS
- Map abbreviations to full name
"""
FULLNAMES = {
    'gl' : 'Glimmer',
    'van': 'VanguardToken',
    'cru': 'CrucibleToken',
    'cry': 'CryptarchToken',
}


class RequestType(Enum):
    List = 1
    Add = 2
    Subtract = 3


class InventoryCommand:
    def __init__(self, rawCommand: str):
        requestType = RequestType.Add if re.match(ADDCOMMAND, rawCommand) else RequestType.Subtract if re.match(SUBCOMMAND, rawCommand) else RequestType.List 
        key = re.findall(r"\d+([a-z]+)", rawCommand)
        quantity = re.findall(r"\d+", rawCommand)

        self.ItemKey = None if len(key) == 0 else FULLNAMES[key[0]] if key[0] in FULLNAMES else key[0]
        self.Quantity = None if len(quantity) == 0 else quantity[0]
        self.Type = requestType


"""
INVENTORY HANDLER
Number tracking system for various items that would otherwise be tedious
- Allows you to view, add or subtract from a specific counter
"""
class InventoryHandler:
    def __init__(self, user: str, message: str):
        self.Author = str(user)
        self.Message = message.lower().replace(r" ", "")
        self.Commands = re.findall(PATTERN, self.Message)
        self.Data = {}
        self.Response = self.check()

    def check(self) -> str:
        # No inventory commands recognized, bail early
        if len(self.Commands) == 0:
            return None
        
        print("  > Decoding inventory commands... \t" + str(self.Commands))        
        response = ""
        for rawCommand in self.Commands:
            # Fetch inventory data from file
            file = open('data.json')
            self.Data = json.load(file)

            command = InventoryCommand(rawCommand)
            if command.Type == RequestType.List:
                response = self.ListInventory()
            
            elif command.Type == RequestType.Add:
                response = self.AddInventory(command)

            elif command.Type == RequestType.Subtract:
                response = self.SubInventory(command)

        return response
    
    def InformEmpty(self):
        print("  > None found...")
        response = F"@{self.Author}\n"
        response += "> *No inventory found...*\n > *To begin, use:*  `#add <quantity> <item>`"
        return response
    
    def GenerateReceipt(self, command: "InventoryCommand"):
        receipt = F"@{self.Author}\n"
        receipt += F"> *{'+' if command.Type == RequestType.Add else '-'}{command.Quantity}*\n"
        receipt += F"> {CustomEmoji.D2Emojis[command.ItemKey]} " if command.ItemKey in CustomEmoji.D2Emojis else "> "
        receipt += F"{self.Data[self.Author][command.ItemKey]} {command.ItemKey}"
        return receipt
    
    def WriteToFile(self):
        jsonFile = open("data.json", "w")
        jsonFile.write(json.dumps(self.Data))
        jsonFile.close()
    
    def ListInventory(self):
        # No inventory found, bail early
        if self.Author not in list(self.Data.keys()):
            return self.InformEmpty()

        print(F"  > Fetching inventory for {self.Author}...")
        response = F"@{self.Author}\n"
        for item in self.Data[self.Author]:
            response += F"> {CustomEmoji.D2Emojis[item]} " if item in CustomEmoji.D2Emojis else "> "
            response += F"*{self.Data[self.Author][item]} {item}*\n"

        return response

    def AddInventory(self, command: "InventoryCommand"):
        # Add user record if not already existing and default count to zero
        if self.Author not in list(self.Data.keys()):
            print(F"  > Adding {self.Author}...")
            self.Data[self.Author] = {}
            self.Data[self.Author][command.ItemKey] = 0

        print(F"  > Adding {command.ItemKey} for {self.Author}...")
        self.Data[self.Author][command.ItemKey] += int(command.Quantity)
        response = self.GenerateReceipt(command)
        self.WriteToFile()

        return response

    def SubInventory(self, command: "InventoryCommand"):
        # No record found to deduct, bail early
        if self.Author not in list(self.Data.keys()) or command.ItemKey not in list(self.Data[self.Author]):
            return self.InformEmpty()

        print(F"  > Subtracting {command.ItemKey} for {self.Author}...")
        
        # Negative balance check, inform user and bail early
        if self.Data[self.Author][command.ItemKey] - int(command.Quantity) < 0:
            print("  > Negative balance detected...")
            response += F"@{self.Author}\n"
            response += "> :warning: *Overdraw detected... Cancelling transaction!*\n"
            response += F"> {CustomEmoji.D2Emojis[command.ItemKey]} " if command.ItemKey in CustomEmoji.D2Emojis else "> "
            response += F"{self.Data[self.Author][command.ItemKey]} {command.ItemKey}"
            return response

        self.Data[self.Author][command.ItemKey] -= int(command.Quantity)
        response = self.GenerateReceipt(command)        
        self.WriteToFile()

        return response
    

# DEBUG
# r = InventoryHandler("jake", "#sub 1 cry")
# print(r.Response)