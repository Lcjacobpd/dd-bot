import re
import json


# Command patterns
listCmd = r"#loot|#stuff"
addCmd = r"#add[\d]+(?:gl|van|cru|cry)"
subCmd = r"#(?:remove|sub)[\d]+(?:gl|van|cru|cry)"

# Icon library
icons = {
    'Glimmer': '<:d2_material_glimmer:1042134639969566750>',
    'Vanguard Tokens' : '<:d2_faction_vanguard:1042948486875856949>',
    'Crucible Tokens' : '<:d2_faction_crucible:1042948478134923407>',
    'Cryptarch Tokens' : '<:d2_faction_cryptarch:1042948479686819930>'
}

# Item name library
fullNames = {
    'gl': 'Glimmer',
    'van': 'Vanguard Tokens',
    'cru': 'Crucible Tokens',
    'cry': 'Cryptarch Tokens',
}

class Inventory:
    """Wrapper for inventory command"""
    def __init__(self, user: str, message: str):
        

        self.user = str(user)
        self.message = message.lower().replace(r" ", "")
        self.cmds = re.findall(listCmd, self.message) + re.findall(addCmd, self.message) + re.findall(subCmd, self.message)
        self.data = {}

    def check(self) -> str:
        """Return command results"""
        if len(self.cmds) > 0:
            return self.decode(self.cmds)
        else:
            return ""

    def decode(self, commands) -> str:
        """Get inventory commands details"""
        print("  > Decoding inventory commands... \t" + str(self.cmds))
        
        msg = ""
        for command in commands:
            # Fetch inventory data from file
            file = open('data.json')
            data = json.load(file)

            if re.match(listCmd, command):
                msg = self.listInventory(data)
            
            elif re.match(addCmd, command):
                msg = self.addInventory(data, command)

            elif re.match(subCmd, command):
                msg = self.subInventory(data, command)

        return msg

    def listInventory(self, data):
        """Print current inventory, if available"""
        stuff = ""
        if self.user in list(data.keys()):
            print(F"  > Fetching inventory for {self.user}...")
            stuff += F"@{self.user}\n"
            for item in data[self.user]:
                stuff += F"> {icons[item]} " if item in icons else "> "
                stuff += F"*{data[self.user][item]} {item}*\n"

        # Else inform empty
        else:
            print("  > None found...")
            stuff += F"@{self.user}\n"
            stuff += "> *No inventory found...*\n > *To begin, use:*  `#add <quantity> <item>`"

        return stuff

    def addInventory(self, data, command):
        """Increase specified inventory by quantity"""
        total = ""

        # Isolate item name, map to full name if applicable
        itemName = str(re.findall(r"\d+([a-z]+)", command)[0])
        itemName = fullNames[itemName] if itemName in fullNames else itemName

        # Get quantity
        quantity = re.findall(r"\d+", command)[0]
        
        # Existing user
        if self.user in list(data.keys()):
            if itemName in data[self.user]:
                print(F"  > Updating {itemName} for {self.user}...")
                data[self.user][itemName] += int(quantity)

            else:
                print(F"  > Adding {itemName} for {self.user}...")
                data[self.user][itemName] = int(quantity)

        # New user
        else:
            print(F"  > Adding {self.user}...")
            print(F"  > Adding {itemName} for {self.user}...")
            data[self.user] = {}
            data[self.user][itemName] = int(quantity)

        # Generate receipt
        total += F"@{self.user}\n"
        total += F"> *+{quantity}*\n"
        total += F"> {icons[itemName]} " if itemName in icons else "> "
        total += F"{data[self.user][itemName]} {itemName}"
        
        # Write back to file
        jsonFile = open("data.json", "w")
        jsonFile.write(json.dumps(data))
        jsonFile.close()

        return total

    def subInventory(self, data, command):
        """Subtract specified inventory by quantity"""
        total = ""

        # Isolate item name, map to full name if applicable
        itemName = str(re.findall(r"\d+([a-z]+)", command)[0])
        itemName = fullNames[itemName] if itemName in fullNames else itemName

        # Get quantity
        quantity = re.findall(r"\d+", command)[0]
        
        # Existing user
        if self.user in list(data.keys()):
            if itemName in data[self.user]:
                print(F"  > Updating {itemName} for {self.user}...")

                # Negative balance check
                if data[self.user][itemName] - int(quantity) < 0:
                    print("  > Negative balance detected...")
                    total += F"@{self.user}\n"
                    total += "> :warning: *Overdraw detected... Cancelling transaction!*\n"
                    total += F"> {icons[itemName]} " if itemName in icons else "> "
                    total += F"{data[self.user][itemName]} {itemName}"
                    return total

                data[self.user][itemName] -= int(quantity)

        # Inform subtract from empty
        else:
            print("  > No quantity found...")
            total += F"@{self.user}\n"
            total += "> *No inventory found to subtract...*\n > *To begin, use:*  `#add <quantity> <item>`"
            return total

        # Generate receipt
        total += F"@{self.user}\n"
        total += F"> *-{quantity}*\n"
        total += F"> {icons[itemName]} " if itemName in icons else "> "
        total += F"{data[self.user][itemName]} {itemName}"
        
        # Write back to file
        jsonFile = open("data.json", "w")
        jsonFile.write(json.dumps(data))
        jsonFile.close()

        return total

