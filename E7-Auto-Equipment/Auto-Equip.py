#https://github.com/meowyih/meowyih.github.io/blob/9600a490c45e87b426bd1e68b1aa0f83bc472166/epic7-gear/gear.js#L182
from pyautogui import *
import pyautogui
import time
import keyboard
from PIL import Image
import pytesseract
import numpy as np
from enum import IntEnum

#%%Fail-Safes
##After each pyautogui instruction waits for 0.25 seconds
pyautogui.PAUSE = 0.3
##If you drag your mouse to the upper left will abort program
pyautogui.FAILSAFE = True

#%%Constants
minMaxDict = {'percent': (4,8), 'critC': (3,5), 'critD': (3,7), 'flatAtk': (30,46), 'flatDef': (25,33), 'flatHp':(147,202), 'speed':(1,4)}

statNames = ['Attack', 'Defense', 'Health', 'Effectiveness', 'Effect Resistance', 'Speed', 'Critical Hit Damage', 'Critical Hit Chance']

class EquipmentType(IntEnum):
    Weapon = 1
    Helmet = 2
    Armor = 3
    Necklace = 4
    Ring = 5
    Boots = 6

class Rarity(IntEnum):
    Normal = 0
    Good = 1
    Rare = 2
    Heroic = 3
    Epic = 4

class Results(IntEnum):
    Keep = 0
    Sell_substats = 1
    Sell_mainstat = 2
    Sell_rarity = 3

#%%Test list
testList = [['percent', 4], ['flatDef', 29], ['percent', 7]]
#%% Gear Score Functions
# substat score = STAT - stat_min * gear_type *(100/(stat_max-stat_min))
#gear_type: 3 if heroic, 4 if epic, sell if neither
# if flat stat, score = score/2
def calculateSubScore(stat):
    score = (stat[1] - minMaxDict[stat[0]][0])*(100/(minMaxDict[stat[0]][1]- minMaxDict[stat[0]][0]))
    if(stat[1] > 8):
        score = score / 2
    return score
    

def calculateTotalScore(substats):
    score = 0
    for x in substats:
        score += calculateSubScore(x)
    return score

#%% Text Parsing Functions
def parseValue(string):
    x = string.split()
    string = x[-1]
    if string.endswith('%'):
        x = string.split('%')
        value = int(x[0])
    else:
        value = int(string)
    return value

def parseStat(string):
    if(string == ''):
        return None
    x = string.split()
    firstWord = str(x[0])
    if string.endswith('%'):
        match firstWord:
            case 'Critical':
                if x[2] == 'Damage':
                    return ['critD', parseValue(string)]
                else:#Critical Hit Chance
                    return ['critC', parseValue(string)]
            case 'Health' | 'Defense' | 'Attack' | 'Effectiveness' | 'Effect':
                return ['percent', parseValue(string)]
            case _:
                return None
    else:
        match firstWord:
            case 'Health':
                return ['flatHp', parseValue(string)]
            case 'Defense':
                return ['flatDef', parseValue(string)]
            case 'Attack':
                return ['flatAtk', parseValue(string)]
            case 'Speed':
                return ['speed', parseValue(string)]
            case _:
                return None

def getScore(list):
    statsList = []
    for x in list:
        stat = parseStat(x)
        if stat != None:
            #print(stat)
            statsList.append(stat)
            #list.remove(x)
    print(statsList)
    score = calculateTotalScore(statsList)
    return (score)

def parseRarity(string):
    rarity = -1
    if(string.find('Epic') != -1):
        rarity = Rarity.Epic
    elif (string.find('Heroic') != -1):
        rarity = Rarity.Heroic
    elif (string.find('Rare') != -1):
        rarity = Rarity.Rare
    elif (string.find('Good') != -1):
        rarity = Rarity.Good
    elif (string.find('Normal') != -1):
        rarity = Rarity.Normal
    print(rarity)
    return rarity

def parseEquipType(string):
    equipType = -1
    if(string.find('Weapon') != -1):
        equipType = EquipmentType.Weapon
    elif (string.find('Helmet') != -1):
        equipType = EquipmentType.Helmet
    elif (string.find('Armor') != -1):
        equipType = EquipmentType.Armor
    elif (string.find('Necklace') != -1):
        equipType = EquipmentType.Necklace
    elif (string.find('Ring') != -1):
        equipType = EquipmentType.Ring
    elif (string.find('Boots') != -1):
        equipType = EquipmentType.Boots
    print(equipType)
    return equipType

def parseMainStat(string):
    mainStat = next((x for x in statNames if x in string), False)
    startIndex = string.find(mainStat)
    cutString = string[startIndex:]
    endIndex = cutString.find('\n')
    cleanString = cutString[:endIndex]
    mainStat = parseStat(cleanString)
    print(mainStat)
    return mainStat

def checkMainStat(mainStat, equipmentType):
    flag = False
    match equipmentType:
        case EquipmentType.Weapon | EquipmentType.Helmet | EquipmentType.Armor:
            flag = True
        case EquipmentType.Necklace:
            match mainStat[0]:
                case 'percent' | 'critC' | 'critD':
                    flag = True
                case _:
                    flag = False
        case EquipmentType.Ring:
            match mainStat[0]:
                case 'percent':
                    flag = True
                case _:
                    flag = False
        case EquipmentType.Boots:
            match mainStat[0]:
                case 'percent' | 'speed':
                    flag = True
                case _:
                    flag = False
        case _:
            flag = False
    return flag

def parseImageInfo(rawText):
    result = -1
    equipmentType = parseEquipType(rawText)
    rarity = parseRarity(rawText)
    mainStat = parseMainStat(rawText)
    if (rarity == Rarity.Heroic or rarity == Rarity.Epic):
        if(equipmentType != -1):
            if(checkMainStat(mainStat, equipmentType)):
                print('Checking substats')
                textAsList = rawText.split('\n')
                score = getScore(textAsList)
                scoreAsString = str(score)
                maxScore = 100 * rarity
                maxScoreAsString = str(maxScore)
                print('Gear Score: ' + scoreAsString + ' / ' + maxScoreAsString)
                if(score / maxScore) >= 0.7:
                    result = Results.Keep
                else:
                    result = Results.Sell_substats
            else:
                result = Results.Sell_mainstat
        else:
            print('Could not determine equipment type')
    elif (rarity == Rarity.Rare or rarity == Rarity.Good or rarity == Rarity.Normal):
        result = Results.Sell_rarity
    else:
        print('Could not determine rarity')
    return result

#%%Main
kept = 0
sold_substat = 0
sold_mainstat = 0
sold_rarity = 0

filename = 'E7EquipmentFullGrey.png'
#filename = 'WholePageGrey.png'
image = np.array(Image.open(filename))
text = pytesseract.image_to_string(image)
#print(text)


match parseImageInfo(text):
    case Results.Keep:
        print('Keep')
        kept += 1
    case Results.Sell_rarity:
        print('Sell: Bad rarity')
        sold_rarity += 1
    case Results.Sell_mainstat:
        print('Sell: Bad main stat')
        sold_mainstat += 1
    case Results.Sell_substats:
        print('Sell: Bad substats')
        sold_substat += 1
    case _:
        print('Retry')



# print(calculateTotalScore(testList))

print(parseStat('Health 4%'))
print(parseStat('Speed 4'))
print(parseStat('Defense 29'))
print(parseStat('Critical Hit Chance 4%'))
print(parseStat('Effectiveness 7%'))
print(parseStat('Critical Hit Damage 6%'))
print(parseStat('Effect Resistance 6%'))


