# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:19:03 2024

@author: Logan
"""


from pyautogui import *
import pyautogui
import time
import random 


#pyautogui.scroll(amount_to_scroll, x=moveToX, y=moveToY)
#Scroll at semi random place
#Aprox place X: 1263 Y:  590
##Get screen res
resolution=pyautogui.size()
########
#%%Fail-Safes
##After each pyautogui instruction waits for 0.25 seconds
pyautogui.PAUSE = 0.3
##If you drag your mouse to the upper left will abort program
pyautogui.FAILSAFE = True
#keyboard.hook_key('q', lambda e: sys.exit("q was pressed, exiting program"))
#%%Functions
def clickOffset():
    return random.randint(-20, 20)

def pauseForAnimation():
    time.sleep(random.uniform(1.5, 1.8))

def secondaryButton(img):
    img_pos=pyautogui.locateCenterOnScreen(img, confidence = 0.95, region = (round(resolution[0]/3), round(resolution[1]/2), round(resolution[0]*2/3), resolution[1]))
    attempts = 1
    while img_pos == None and attempts < 4:
        time.sleep(0.2)#wait for confirm to appear
        img_pos=pyautogui.locateCenterOnScreen(img, confidence = 0.95, region = (round(resolution[0]/3), round(resolution[1]/2), round(resolution[0]*2/3), resolution[1]))
        attempts +=1

    if attempts < 4:
        # img_point=pyautogui.center(img_pos)
        pyautogui.click(x=img_pos[0] + clickOffset(), y=img_pos[1] + clickOffset(), clicks=2, interval=0.05, button='left')
        return True
    else:
        print("Could not find secondary button")
        return False

def checkForImage(image_name):
    return_flag = False
    try:
        img = pyautogui.locateOnScreen(image_name + '.PNG', confidence=0.90)
        pyautogui.moveTo(img[0], img[1])
        print("Found " + image_name)
        return_flag = True
    finally:
        return return_flag
    
def checkForUR(image_name):
    return_flag = False
    try:
        img = pyautogui.locateOnScreen(image_name + '.PNG',confidence=0.95)
        pyautogui.moveTo(img[0], img[1])
        try:
            ur = pyautogui.locateOnScreen('UR.PNG', confidence=0.95, region = img)
            pyautogui.moveTo(ur[0], ur[1])
            return_flag = True
            print("Found " + image_name)
        except:
            return_flag = False
    finally:
        return return_flag

def clickImage(image_name):
    return_flag = False
    try:
        img_pos=pyautogui.locateCenterOnScreen(image_name + '.PNG', confidence = 0.90)
        pyautogui.click(x=img_pos[0] + clickOffset(), y=img_pos[1] + clickOffset(), clicks=1, interval=0.05, button='left')
        return_flag = True
    except:
        print("Could not find " + image_name)
    finally:
        return return_flag
    
def clickReroll():
    return_flag = False
    try:
        img_pos=pyautogui.locateCenterOnScreen('Reroll.PNG', confidence = 0.88, region = (round(resolution[0]*2/3), round(resolution[1]*2/3), round(resolution[0]/3), round(resolution[1]/3)))
        pyautogui.click(x=img_pos[0] + clickOffset(), y=img_pos[1] + clickOffset(), clicks=1, interval=0.05, button='left')
        return_flag = True
    except:
        print("Could not find Draw Again")
    finally:
        return return_flag
    

#%%Set-up
time.sleep(5.0)
##Move to center of the screen instantly
pyautogui.moveTo(resolution[0]/2, resolution[1]/2, duration=0)

pri_target = "KryUR"
sec_targets = ["Eleaneer", "Gray", "Elise", "Justia"]
ter_targets = [item + "SR" for item in sec_targets]
#number of refresh done
refresh=0
pri_hits=[False, 0]
sec_hits=[False, 0]
ter_hits=[False, 0]
complete_set = False

run = True

# checkForUR("KryUR")
#checkForImage("Elise")

# %%Main Loop
while run == True:
    if(clickImage("Skip")):
        refresh = refresh + 1
        pauseForAnimation()
        pyautogui.moveTo(resolution[0]-20, resolution[1]/2, duration=0)
        if checkForUR(pri_target):
            pri_hits[0] = True
            pri_hits[1] = pri_hits[1] + 1
            ter_name = None
            for name in sec_targets:
                if(checkForImage(name)):
                    ter_name = name + "SR"
                    sec_hits[0] = True
                    sec_hits[1] = sec_hits[1] + 1
                    break
            for name in ter_targets:
                if(checkForImage(name)):
                    ter_hits[0] = True
                    ter_hits[1] = ter_hits[1] + 1
                    if name is ter_name:
                        complete_set = True
                    break
    else: 
        run = False

    if(pri_hits[0] and sec_hits[0] and ter_hits[0] and complete_set is True):
        run = False
    else:
        pri_hits[0] = False
        sec_hits[0] = False
        ter_hits[0] = False
        ter_name = None

    if run:
        run = clickReroll()
        if run:
            time.sleep(1)
            run = clickImage("Confirm")
            pauseForAnimation()

print("You exited successfuly")
print("Number of rerolls: " + str(refresh))
print("Number of primary hits: " + str(pri_hits[1]))
print("Number of secondary hits: " + str(sec_hits[1]))
print("Number of tertiary hits: " + str(ter_hits[1]))