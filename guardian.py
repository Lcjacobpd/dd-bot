class Guardian:
    # Properties
    Name: str
    Discord: str
    Bookmarks: str

    # Constructor
    def __init__(self, line: str) -> None:
        line = line[:-1]
        details = line.split(":")

        self.Discord = details[0]
        self.Name = details[0].split("#")[0]
        self.Bookmarks = details[1].split(",")

    def __str__(self) -> str:
        return F"{self.Name}: {self.Bookmarks}"