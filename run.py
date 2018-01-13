#!usr/bin/python
''' Recipe Book! Python and Tkinter build recipe book to be
used with a raspberry pi and touchscreen in the kitchen!'''

#Author - Sean Wiley
#v0.2.4

########################### TODO ##########################
# Apply MVC techniques to my code to clean it up
# REFORMAT MY SPAGHETTI
# Make it somewhat readable on a bigger screen that isn't a pi

###########################################################

from tkinter import *
from gui import GUI

#ACTIVATE THIS SCRIPT TO START THE PROGRAM

if __name__ == "__main__":
    root = Tk()
    interface = GUI(root)
    root.mainloop()
