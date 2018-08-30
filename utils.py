import time
import random
from termcolor import colored, cprint
import platform
import math
import uuid

def enableVTWindows():
    if platform.system().lower() == 'windows':
        from ctypes import windll, c_int, byref
        stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
        mode = c_int(0)
        windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
        mode = c_int(mode.value | 4)
        windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)

def message(string, color='white', highlight=None, attributes=[], returnFormatted=False):
    if color not in ['white', 'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan']:
        color = 'white'
    if highlight not in [None, 'on_grey', 'on_white', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan']:
        highlight = None
    usedAttributes = []
    for attr in attributes:
        if attr in ['bold', 'dark', 'underline', 'blink', 'reverse', 'concealed']:
            usedAttributes.append(attr)

    if returnFormatted:
        return colored(string, color, highlight, usedAttributes)
    else:
        cprint(colored(string, color, highlight, usedAttributes))

def messageDirect(*argv):
    for arg in argv:
        print(arg)

def calcPercentage(small, big):
    percentage = (small / big) * 10
    return round(percentage, -1)

def colorByPercentage(percentage):
    #colors = green, cyan, magenta, yellow, red

    if percentage in [100, 90]:
        return 'green'
    elif percentage in [80, 70]:
        return 'cyan'
    elif percentage in [60, 50]:
        return 'magenta'
    elif percentage in [40, 30]:
        return 'yellow'
    elif percentage in [20, 10, 0]:
        return 'red'
    else:
        return 'white'

def formatHPString(current_hp, max_hp):
    percentage = calcPercentage(current_hp, max_hp)
    current_color = colorByPercentage(percentage)
    formatted = message(str(current_hp) + '/' + str(max_hp), current_color, 'on_grey', returnFormatted=True)
    return formatted

def generateUID():
    return str(uuid.uuid1())

def boolPrompt(promptMessage):
    message(promptMessage, 'blue')
    answer = input('Type Y/N: ')
    if answer.lower() in ['y', 'ye', 'yes', 'true', 'accept']:
        return True
    else:
        return False

def stringPrompt(promptMessage, inputType):
    message(promptMessage, 'blue')
    answer = input('Enter ' + inputType + ' : ')
    return answer

def characterLeveler(character, desiredLvl):
    #call character.lvlUp until the character has reached desired lvl
    if desiredLvl > character.lvl:
        while character.lvl < desiredLvl:
            character.lvlUp()