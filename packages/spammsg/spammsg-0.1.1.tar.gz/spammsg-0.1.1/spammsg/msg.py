import pyautogui
from time import sleep

def message():
    messages=input("ENTER MESSAGE YOU WANT TO SEND: ")
    times=input("HOW MANY TIMES YOU WANT TO SPAM IT: ")
    print("You'll be given 10 seconds time to open the message box")
    sleep(10)
    for i in range(int(times)):
        pyautogui.typewrite(messages)
        pyautogui.typewrite("\n")
        