# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 19:19:03 2020

@author: Logan
"""


from pyautogui import *
import pyautogui
import time
import keyboard
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

def checkForItem(item_name, bought_flag):
    return_flag = False
    if bought_flag == False:
        #Search for the icon
        icon=pyautogui.locateOnScreen(item_name + '_icon.PNG',confidence=0.95, region = (round(resolution[0]/3), 0, round(resolution[0]*2/3), resolution[1]))
        if (icon) != None:
            #Find corresponding buy button
            pyautogui.moveTo(icon[0], icon[1])
            sleep(random.uniform(0.1, 0.4))
            decrementConfidence = 0.96
            while (return_flag == False) and (decrementConfidence > 0.9):
                for result in pyautogui.locateAllOnScreen(item_name + '_button.PNG',confidence=decrementConfidence, region = (round(resolution[0]*2/3), 0, resolution[0], resolution[1])):
                    if((result != None) and (result[1] > (icon[1] - 20)) and (result[1] < (icon[1] + 20)) and (return_flag != True)):
                        print("Buy " + item_name + ".")
                        buy=pyautogui.center(result)
                        pyautogui.click(x=buy[0], y=buy[1]+5, clicks=2, interval=0.05, button='left')
                        time.sleep(0.4)#wait for confirm button
                        if secondaryButton(item_name + '_buy.PNG') == True:
                            return_flag = True
                        else:
                            print("Could not find " + item_name + " buy button.")
                            return_flag = False
                decrementConfidence -= 0.2
    return return_flag

            # button=pyautogui.locateOnScreen(item_name + '_button.PNG',confidence=0.98, region = (round(resolution[0]*2/3), icon[1] - 5, resolution[0], icon[1] + 5))
            # decrementConfidence = 0.96
            # while (button) == None and decrementConfidence > 0.9:
            #     button=pyautogui.locateOnScreen(item_name + '_button.PNG',confidence=decrementConfidence, region = (round(resolution[0]*2/3), icon[1] - 5, resolution[0], icon[1] + 5))
            #     decrementConfidence -= 0.02
            # if button != None:
            #     print("Buy " + item_name + ".")
            #     buy=pyautogui.center(button)
            #     pyautogui.click(x=buy[0], y=buy[1]+5, clicks=2, interval=0.05, button='left')
            #     time.sleep(0.4)#wait for confirm button
            #     if secondaryButton(item_name + '_buy.PNG') == True:
            #         return_flag = True
            #     else:
            #         print("Could not find " + item_name + " buy button.")
            #         return_flag = False
            # else:
            #     print("Found " + item_name + " Icon but no button.")
            #     return_flag = False

#%%Set-up
time.sleep(5.0)
##Move to center of the screen instantly
pyautogui.moveTo(resolution[0]/2, resolution[1]/2, duration=0)
#number of visual inspections done on screen
scrolls=0
#number of coven bought
cont_coven=0
#number of mystic bought
cont_mystic=0
#number of refresh done
cont_refresh=0

run = True
coven_bought = False
mystic_bought = False

#%%Main Loop
while run == True:
    time.sleep(random.uniform(0.3, 0.6))
    if checkForItem("covenant", coven_bought) == True:
        coven_bought = True
        cont_coven += 1

    if checkForItem("mystic", mystic_bought) == True:
        mystic_bought = True
        cont_mystic += 1


#%%Finally refreshes
    if scrolls>=1 or (coven_bought == True and mystic_bought == True):
        #Search for the refresh button
        RB_pos=pyautogui.locateCenterOnScreen('refresh_button.PNG',confidence=0.90, region = (0, round(resolution[1]/2), round(resolution[0]/2), resolution[1]))
        if RB_pos != None:
            time.sleep(0.3)
            #RB_point=pyautogui.center(RB_pos)
            pyautogui.click(x=RB_pos[0] + clickOffset(), y=RB_pos[1] + clickOffset(), clicks=2, interval=0.05, button='left')

            time.sleep(0.3)#wait for confirm to appear

            if secondaryButton('confirm button.PNG') == False:
                run = False #stop running, cannot refresh
                print("Could not find refresh confirmation, exiting program.")

            scrolls=0
            coven_bought = False
            mystic_bought = False
            time.sleep(random.uniform(0.1, 0.4))
            cont_refresh+=1

            print("Covenant Summons bought=",cont_coven)
            print("Mystic Summons bought=",cont_mystic)
            print("Refresh Done=",cont_refresh)
        else:
            run = False
            print("Could not find refresh button, exiting program.")
    else:
        #%%Scroll up
        pyautogui.moveTo(resolution[0]/2 + clickOffset(), resolution[1]/2 + 150 + clickOffset(), duration=0)
        #Drag upward 300 pixels in 0.2 seconds
        pyautogui.dragTo(resolution[0]/2 + clickOffset(), resolution[1]/2-450, duration=0.3)
        scrolls += 1
        time.sleep(random.uniform(0.1, 0.4))
        

#%%Outside of the while loop
print("You exited successfuly")