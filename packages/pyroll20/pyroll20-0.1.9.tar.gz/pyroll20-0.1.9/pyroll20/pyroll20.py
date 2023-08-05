from heapq import nlargest, nsmallest
from random import randint
import re

#dice_regex = re.compile(r"^(\d*)d(\d*)([hmle+t-]|\.[+-])?(\d*)?\ ?((adv)|(disadv))?$")


dice_regex = re.compile(r"^(\d*)d(\d*)([hmle+t-]|\.[+-])?(\d*)?$")


#            'h',  # Highest Roll
#            'l',  # Lowest Roll
#            '+',  # Add to total
#            '-',  # Remove from total
#            '.+', # Add to every individual
#            '.-', # Remove from every individual
#            'e',  # Exploding dice
#            't',  # Total

def roll(user_input: str = None):
    result = dice_regex.search(user_input)

    try:
        repeats = int(result.group(1))
    except AttributeError:  # In case a non integer was passed as a repeating argument
        raise ValueError("Invalid entry")
    except ValueError:  # if Nothing was provided, default to 1
        repeats = 1
    try:
        sides = int(result.group(2))  # assign the sides of the die
    except ValueError:  # In case a non integer was passed as a repeating argument
        raise ValueError("Invalid entry")

    try:
        modifier = result.group(3)
    except ValueError:
        modifier = None
    try:
        mod_value = int(result.group(4))
    except ValueError:
        mod_value = None

    if (int(sides) or int(repeats)) < 1:
        return "Invalid Parameter."

    if isinstance(modifier, str):  # Checking for a modifier present
        rolls = []
        for i in range(repeats):
            rolls.append(randint(1, sides))
        rolls = moder(sides=sides, rolls=rolls, modifier=modifier, mod_value=mod_value)
        return rolls
    else:
        rolls = []
        for i in range(repeats):
            rolls.append(randint(1, sides))
        return rolls


def moder(sides: int, rolls: list, modifier: str, mod_value: int):
    if modifier[0] == 'e':
        return explode(sides=sides, rolls=rolls)  # Return exploded dice rolls along with one that were neutral
    if modifier[0] == 'h':  # Return highest
        return nlargest(mod_value, rolls)
    if modifier[0] == 'l':  # Return lowest
        return nsmallest(mod_value, rolls)
    if modifier[0] == '+':  # Add to sum of rolls
        return sum(rolls) + mod_value
    if modifier[0] == '-':  # Subtract from sum of rolls
        return sum(rolls) - mod_value
    if modifier[0] == '.-':  # Subtract from each roll
        for i in range(0, len(rolls)):
            rolls[i] = rolls[i] - mod_value
        return rolls
    if modifier[0] == '.+':  # Add to each roll
        for i in range(0, len(rolls)):
            rolls[i] = rolls[i] + mod_value
        return rolls
    if modifier[0] == 't':  # Sum of rolls
        return sum(rolls)


# The exploding dice function
def explode(sides: int, rolls: list):
    for i in range(0, len(rolls)):
        counter = 0
        loop = True
        if rolls[i] == sides:
            while loop:
                counter += 1
                temp = randint(1, sides)
                rolls[i] += temp
                if temp != sides:
                    loop = False
    return rolls

