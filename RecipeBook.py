#!usr/bin/python
''' Recipe Book! Python and Tkinter build recipe book to be
used with a raspberry pi and touchscreen in the kitchen!'''

#Author - Sean Wiley
#v0.5.1

########################### TODO ##########################
# Apply MVC techniques to my code to clean it up
# REFORMAT MY SPAGHETTI

###########################################################

from tkinter import *
from tkinter import ttk
import configparser

from MenuButtons import MenuButton
from OptionsMenu import OptionMenu
import os
import sys

# Case description

# I. Entire program to be displayed from a 7" raspberry pi touchscreen
#   - RESOLUTION OF THE SCREEN IS 800x480
#   - program will be tested in a windows format, then revised for linux
#       -file storage and saving should be the only changes in this regard
#   - the resolution for the screen is 800x480, so design with this in mind
#       -less empty space the better
#   - Use root.wm_attributes('-fullscreen','true') to apply a kiosk look
#       -MAKE SURE PROPER EXIT BUTTON IS IN PLACE FIRST

# II. User presses a button for the food type (breakfast, lunch, dinner, etc.)

#   -Menu bar will be placed at the top containing touch screen friendly
#    buttons
#   -Button will control type_of_food value, the title, and recipes shown

# III. Recipes are stored in text files and a listbox containing the
#      names of them
#      -Text files will be titled in all caps and spaced to show accordingly
#           -Will possibly use regex for this, unsure, might leave up to user
#      -Needs to check for a mouse-1 press aka a touch screen press

#
# IV. Buttons will be added to add and delete recipes
#    - For now will only pull from files using an integrated file manager
#    - Make sure delete button has a warning window to confirm deletion
#    - After initial add feature creation and testing, will devise
#       alternate solution using a custom recipe insertion function
#           - Will read text files and output them into a listbox for selection
#           thus allowing some extra UI functionality
#           [https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory]

# V. A text box will contain the recipe itself, along with ingredients
#   - If space allows, ingredients in a seperate text box.


class RecipeBook:

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

    type_of_food = "Breakfast"

    def __init__(self, root):
        """Initializes the root window."""
        # -------- Root Management -------
        self.root = root
        root.title("Recipe Book")
        X_WIDTH = root.winfo_screenwidth()
        Y_HEIGHT = root.winfo_screenwidth()
        root.geometry(str(X_WIDTH) + "x" + str(Y_HEIGHT))
        root.wm_attributes('-fullscreen','true')

        # ------ Recipe Type List Toolbar --------
        self.recipe_toolbar = Frame(root, bd=1, relief=RAISED)
        self.recipe_toolbar.config(bg=self.TOOLBAR_COLOR)
        self.recipe_toolbar.pack(side=TOP, fill=X)

        # ----- Breakfast Button-------
        self.breakfast_button = MenuButton(self.recipe_toolbar, "breakfast", LEFT,
                                            lambda: self.change_type("Breakfast"))

        # ----- Lunch Button --------
        self.lunch_button = MenuButton(self.recipe_toolbar, "lunch", LEFT,
                                        lambda: self.change_type("Lunch"))

        # ----- Dinner Button -------
        self.dinner_button = MenuButton(self.recipe_toolbar, "dinner", LEFT,
                                        lambda: self.change_type("Dinner"))

        # ----- Sides Button -------
        self.sides_button = MenuButton(self.recipe_toolbar, "sides", LEFT,
                                        lambda: self.change_type("Sides"))

        # ----- Drinks Button -------
        self.drinks_button = MenuButton(self.recipe_toolbar, "drinks", LEFT,
                                        lambda: self.change_type("Drinks"))

        # ----- Dessert Button ------
        self.dessert_button = MenuButton(self.recipe_toolbar, "dessert", LEFT,
                                        lambda: self.change_type("Dessert"))

        # ---- Exit Button ------
        self.exit_button = MenuButton(self.recipe_toolbar, "exit", RIGHT,
                                      self.quit_app)

        # ----- Options Button ------
        self.options_button = MenuButton(self.recipe_toolbar, "options", RIGHT,
                                         self.options_menu)

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
        self.recipe_lb.bind('<<ListboxSelect>>', self.recipe_select)
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

        root.bind("<F1>", self.clear_listbox)
        root.bind("<Escape>", self.quit_app)

    @staticmethod
    def quit_app(event=None):
        """Closes the application window"""
        root.destroy()

    def options_menu(self):
        OptionMenu(self)

    ################ RECIPE BOXES ################

    def change_type(self, food_type, event=None):
        """Changes the current food type selected."""
        self.type_of_food = food_type
        self.mainTitleVar.set(food_type)
        self.clear_text()
        self.RECIPE_DIRECTORY = "Recipes/" + self.type_of_food + "/"
        self.fill_listbox()

    def open_recipe(self, recipe, event=None):
        """Opens a text file containing a recipe and inserts it in into the
        recipe frame."""
        with open(self.RECIPE_DIRECTORY + recipe + '.txt','r') as txt_file:
            if txt_file:
                self.text_area.delete(1.0, END)
                self.text_area.insert(1.0, txt_file.read())



    def recipe_select(self, event=None):
        """Method to call open_recipe to open a user selected recipe from the listbox."""
        lb_widget = event.widget

        index = int(lb_widget.curselection()[0])

        self.lb_value = lb_widget.get(index)
        self.open_recipe(self.lb_value)
        print("Recipe selected " + self.lb_value)

    def fill_listbox(self, event=None):
        """Fills listbox of recipes from chosen category button."""
        self.clear_listbox()
        self.listbox_index = 1
        for recipe in os.listdir(self.RECIPE_DIRECTORY):
            if recipe.endswith(".txt"):
                self.recipe_lb.insert(self.listbox_index, recipe[0:-4])
                self.listbox_index += 1

    def clear_text(self, event=None):
        """Helper method to clear recipe text."""
        self.text_area.delete(1.0, END)

    def clear_listbox(self, event=None):
        """Helper method to clear listbox text."""
        self.recipe_lb.delete(0,END)

root = Tk()
RecipeBook(root)
root.mainloop()
