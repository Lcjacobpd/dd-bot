import re

def group_one(match_obj):
    return match_obj.group(1)

def inline_length(msg: str):
    # Calculate in-line length.
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
        if char.isupper():   length += uppers[ord(char) - ord('A')]
        elif char.islower(): length += lowers[ord(char) - ord('a')]
        elif char == " ":    length += 2
        else:                length += 1.5

    return round(round(length) * .87)

def format_inline(msgs: list):
    # Format text for 'two-column' display.
    length = 0
    for msg in msgs:
        l = inline_length(msg)
        length = l if l > length else length

    formatted = ""
    for msg in msgs:
        formatted += msg + (" " * (length - inline_length(msg) +3)) + ":"

    return formatted