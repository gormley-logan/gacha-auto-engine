from pyautogui import *
import pyautogui
import time
import keyboard
from PIL import Image
import pytesseract
import numpy as np

#%%Fail-Safes
##After each pyautogui instruction waits for 0.25 seconds
pyautogui.PAUSE = 0.3
##If you drag your mouse to the upper left will abort program
pyautogui.FAILSAFE = True

#%%Main
