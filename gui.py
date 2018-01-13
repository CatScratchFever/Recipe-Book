from tkinter import *
from tkinter import ttk
import configparser

from menubuttons import MenuButton
from optionsmenu import OptionMenu
from gui_control import GUI_Control
import os
import sys

class GUI:

    # ---- STATIC VARIABLES -----
    TITLE_TEXT_SIZE = "24"
    TITLE_FONT = "Arial"
    TITLE_TYPE = "bold"

    LISTBOX_TEXT_SIZE = "24"
    LISTBOX_FONT = "Arial"
    LISTBOX_TYPE = "bold"

    ### failsafe variables for config file in case of corruption or deletion ###
    #TODO: write function to recreate config file in case of corruption/deletion
    TOOLBAR_COLOR = '#ff00ff' #default
    RECIPE_FRAME_COLOR = '#ff00ff' #default
    mainTitleVar_Color = '#ff00ff' #default

    Config = configparser.ConfigParser()
    Config.read('./config.ini')
    #print(Config.sections())
    TOOLBAR_COLOR = Config['colors'].get('TOOLBAR_COLOR')
    RECIPE_FRAME_COLOR = Config['colors'].get('RECIPE_FRAME_COLOR')
    mainTitleVar_Color = Config['colors'].get('mainTitleVar_Color')

    def __init__(self, root):
        """Initializes the root window."""
        # -------- Root Management -------
        self.root = root
        root.title("Recipe Book")
        X_WIDTH = root.winfo_screenwidth()
        Y_HEIGHT = root.winfo_screenwidth()
        root.geometry(str(X_WIDTH) + "x" + str(Y_HEIGHT))
        root.wm_attributes('-fullscreen','true')

        self.gui_control = GUI_Control(self) #creates a GUI_control object

        # ------ Recipe Type List Toolbar --------
        self.recipe_toolbar = Frame(root, bd=1, relief=RAISED)
        self.recipe_toolbar.config(bg=self.TOOLBAR_COLOR)
        self.recipe_toolbar.pack(side=TOP, fill=X)

        # ----- Breakfast Button-------
        self.breakfast_button = MenuButton(self.recipe_toolbar, "breakfast", LEFT,
                                            lambda: self.gui_control.change_type("Breakfast"))

        # ----- Lunch Button --------
        self.lunch_button = MenuButton(self.recipe_toolbar, "lunch", LEFT,
                                        lambda: self.gui_control.change_type("Lunch"))

        # ----- Dinner Button -------
        self.dinner_button = MenuButton(self.recipe_toolbar, "dinner", LEFT,
                                        lambda: self.gui_control.change_type("Dinner"))

        # ----- Sides Button -------
        self.sides_button = MenuButton(self.recipe_toolbar, "sides", LEFT,
                                        lambda: self.gui_control.change_type("Sides"))

        # ----- Drinks Button -------
        self.drinks_button = MenuButton(self.recipe_toolbar, "drinks", LEFT,
                                        lambda: self.gui_control.change_type("Drinks"))

        # ----- Dessert Button ------
        self.dessert_button = MenuButton(self.recipe_toolbar, "dessert", LEFT,
                                        lambda: self.gui_control.change_type("Dessert"))

        # ---- Exit Button ------
        self.exit_button = MenuButton(self.recipe_toolbar, "exit", RIGHT,
                                      self.gui_control.quit_app)

        # ----- Options Button ------
        self.options_button = MenuButton(self.recipe_toolbar, "options", RIGHT,
                                         self.gui_control.options_menu)

        # ------- Main Recipe Window Frame --------
        self.recipe_window = Frame(root)
        self.recipe_window.config(background=self.RECIPE_FRAME_COLOR,
                                    pady=15)
        self.recipe_window.pack(side=TOP, fill=X)

        # ------- Main Title ---------

        self.mainTitleVar = StringVar()
        self.mainTitleVar_label = Label(self.recipe_toolbar,
                                        textvariable=self.mainTitleVar,
                                        bg=self.TOOLBAR_COLOR,
                                        fg=self.mainTitleVar_Color,
                                        font=(self.TITLE_FONT,
                                              self.TITLE_TEXT_SIZE,
                                              self.TITLE_TYPE)
                                       )
        self.mainTitleVar.set("MAIN MENU")
        self.mainTitleVar_label.pack(side=LEFT, padx=20, pady=5)

        # ----- Recipe Listbox ------
        self.lb_scrollbar = Scrollbar(self.recipe_window, width=40)

        self.lb_scrollbar.grid(row=1, column=1, sticky=NS)

        self.recipe_lb = Listbox(self.recipe_window,
                                 yscrollcommand=self.lb_scrollbar.set)
        self.lb_scrollbar.config(command=self.recipe_lb.yview)
        self.recipe_lb.config(font=(self.LISTBOX_FONT,
                                    self.LISTBOX_TEXT_SIZE,
                                    self.LISTBOX_TYPE),
                                    width=19)
        self.recipe_lb.bind('<<ListboxSelect>>', self.gui_control.recipe_select)
        self.recipe_lb.grid(row=1, column=0, sticky=N+S+W)

        # ------Seperator----------
        self.seperator = Frame(self.recipe_window, width=8, bg=self.RECIPE_FRAME_COLOR)
        self.seperator.grid(row=1, column=2,sticky=N+S)

        # ----- Recipe Text -------
        self.recipe_scrollbar = Scrollbar(self.recipe_window, width=40)
        self.text_area = Text(self.recipe_window,wrap=WORD,
                              yscrollcommand=self.recipe_scrollbar.set,
                              width=40)

        self.text_area.grid(row=1, column=3,sticky=N+S+E)
        self.recipe_scrollbar.config(command=self.text_area.yview)
        self.recipe_scrollbar.grid(row=1, column=4,sticky=N+S+E)

        root.bind("<F1>", self.gui_control.clear_listbox)
        root.bind("<Escape>", self.gui_control.quit_app)
