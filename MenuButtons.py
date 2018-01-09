from tkinter import *
from tkinter import Button
from PIL import Image
from PIL import ImageTk

class MenuButton:

    """Creates a menu button inside a frame using Pillow and tkinter button object."""
    def __init__(self, frame, type, side, command=""):
        IMAGE_DIRECTORY = r"./Icons/"
        reference = type + '_icon.png'
        self.image = Image.open(IMAGE_DIRECTORY + type + '_icon.png')
        self.icon = ImageTk.PhotoImage(self.image)
        self.button = Button(frame, image=self.icon, command=command)
        self.button.image = self.icon
        self.button.pack(side=side, padx=2, pady=2)
