#!usr/bin/python
# Recipe Book! Python and Tkinter build recipe book to be used with a raspberry
# pi and touchscreen in the kitchen!

#Author - Sean Wiley

from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import *
from PIL import Image
from PIL import ImageTk
import os
import sys

# Case description

# I. Entire program to be displayed from a 7" raspberry pi touchscreen
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

    TITLE_TEXT_SIZE = "32"
    TITLE_FONT = "Arial"
    TITLE_TYPE = "bold"

    LISTBOX_TEXT_SIZE = "24"
    LISTBOX_FONT = "Arial"
    LISTBOX_TYPE = "bold"

    menu_background_color = 'ghost white'
    recipe_frame_background_color = 'plum1'

    type_of_food = "Breakfast"
    
    @staticmethod
    def quit_app(event=None):
        root.destroy()

    def options_menu(event=None):
        print("Options menu opened!")

    def change_type(self, food_type, event=None):
        self.type_of_food = food_type
        self.main_title.set(food_type)
        self.clear_text()
        self.RECIPE_DIRECTORY = "./Recipes/" + self.type_of_food + "/"
        self.fill_listbox()

    def open_recipe(self, recipe, event=None):
        with open(self.RECIPE_DIRECTORY + recipe + '.txt','r') as txt_file:
            if txt_file:
                self.text_area.delete(1.0, END)
                self.text_area.insert(1.0, txt_file.read())

    def recipe_select(self, event=None):
        lb_widget = event.widget

        index = int(lb_widget.curselection()[0])

        self.lb_value = lb_widget.get(index)
        self.open_recipe(self.lb_value)
        print("Recipe selected " + self.lb_value)

    def fill_listbox(self, event=None):
        self.clear_listbox()
        self.listbox_index = 1
        for recipe in os.listdir(self.RECIPE_DIRECTORY):
            if recipe.endswith(".txt"):
                self.recipe_lb.insert(self.listbox_index, recipe[0:-4])
                self.listbox_index += 1

    def clear_text(self, event=None):
        self.text_area.delete(1.0, END)
                
    def clear_listbox(self, event=None):
        self.recipe_lb.delete(0,END)



    def __init__(self, root):
        # -------- Root Management -------
        root.title("Recipe Book")
        root.geometry(str(X_WIDTH) + "x" + str(Y_HEIGHT))
        
        # ------ Recipe Type List Toolbar --------
        self.recipe_toolbar = Frame(root, bd=2, relief=RAISED)
        self.recipe_toolbar.config(bg=self.menu_background_color)
        self.recipe_toolbar.pack(side=TOP, fill=X)
        
        # ----- Breakfast Button-------
        self.breakfast_img = Image.open("breakfast_icon.png")
        self.breakfast_icon = ImageTk.PhotoImage(self.breakfast_img)
        self.breakfast_button = Button(self.recipe_toolbar, image=self.breakfast_icon,
                                  command= lambda: self.change_type("Breakfast"))
        self.breakfast_button.image = self.breakfast_icon
        self.breakfast_button.pack(side=LEFT, padx=2, pady=2)

        # ----- Lunch Button --------
        self.lunch_img = Image.open("lunch_icon.png")
        self.lunch_icon = ImageTk.PhotoImage(self.lunch_img)
        self.lunch_button = Button(self.recipe_toolbar, image=self.lunch_icon,
                                  command= lambda: self.change_type("Lunch"))
        self.lunch_button.image = self.lunch_icon
        self.lunch_button.pack(side=LEFT, padx=2, pady=2)

        # ----- Dinner Button -------
        self.dinner_img = Image.open("dinner_icon.png")
        self.dinner_icon = ImageTk.PhotoImage(self.dinner_img)
        self.dinner_button = Button(self.recipe_toolbar, image=self.dinner_icon,
                                  command= lambda: self.change_type("Dinner"))
        self.dinner_button.image = self.dinner_icon
        self.dinner_button.pack(side=LEFT, padx=2, pady=2)
        
        # ----- Sides Button -------
        self.sides_img = Image.open("sides_icon.png")
        self.sides_icon = ImageTk.PhotoImage(self.sides_img)
        self.sides_button = Button(self.recipe_toolbar, image=self.sides_icon,
                                  command= lambda: self.change_type("Sides"))
        self.sides_button.image = self.sides_icon
        self.sides_button.pack(side=LEFT, padx=2, pady=2)

        # ----- Drinks Button -------
        self.drinks_img = Image.open("drinks_icon.png")
        self.drinks_icon = ImageTk.PhotoImage(self.drinks_img)
        self.drinks_button = Button(self.recipe_toolbar, image=self.drinks_icon,
                                  command= lambda: self.change_type("Drinks"))
        self.drinks_button.image = self.drinks_icon
        self.drinks_button.pack(side=LEFT, padx=2, pady=2)


        # ----- Dessert Button ------
        self.dessert_img = Image.open("dessert_icon.png")
        self.dessert_icon = ImageTk.PhotoImage(self.dessert_img)
        self.dessert_button = Button(self.recipe_toolbar, image=self.dessert_icon,
                                  command= lambda: self.change_type("Dessert"))
        self.dessert_button.image = self.dessert_icon
        self.dessert_button.pack(side=LEFT, padx=2, pady=2)

        # ---- Exit Button ------
        self.exit_img = Image.open("exit_icon.png")
        self.exit_icon = ImageTk.PhotoImage(self.exit_img)
        self.exit_button = Button(self.recipe_toolbar, image=self.exit_icon,
                                  command= self.quit_app)
        self.exit_button.image = self.exit_icon
        self.exit_button.pack(side=RIGHT, padx=2, pady=2)

        # ----- Options Button ------
        self.options_img = Image.open("options_icon.png")
        self.options_icon = ImageTk.PhotoImage(self.options_img)
        self.options_button = Button(self.recipe_toolbar, image=self.options_icon,
                                  command= self.options_menu)
        self.options_button.image = self.options_icon
        self.options_button.pack(side=RIGHT, padx=10, pady=2)

        # ------- Main Recipe Window Frame --------
        self.recipe_window = Frame(root)
        self.recipe_window.config(background=self.recipe_frame_background_color)
        self.recipe_window.pack(side=TOP, fill=BOTH)

        # ------- Main Title ---------
        
        self.main_title = StringVar()
        self.main_title_label = Label(self.recipe_window, textvariable=self.main_title,
                                      bg=self.recipe_frame_background_color,
                                      font=(self.TITLE_FONT, self.TITLE_TEXT_SIZE,self.TITLE_TYPE))
        self.main_title.set("MAIN MENU")
        self.main_title_label.grid(row=0, column=0, padx=2, pady=2, sticky=W)

        # ----- Recipe Listbox ------
        self.listbox_scrollbar = Scrollbar(self.recipe_window,width=50)        
        self.recipe_lb = Listbox(self.recipe_window,
                                 yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command=self.recipe_lb.yview)
        self.listbox_scrollbar.grid(row=1, column=1, sticky=NS)
        self.recipe_lb.config(font=(self.LISTBOX_FONT,self.LISTBOX_TEXT_SIZE, self.LISTBOX_TYPE),
                              width=19)
        self.recipe_lb.bind('<<ListboxSelect>>', self.recipe_select)
        self.recipe_lb.grid(row=1,column=0, sticky=N+S+W)

        # ----- Recipe Text -------
        
        self.recipe_scrollbar = Scrollbar(self.recipe_window, width=50)
        self.text_area = Text(self.recipe_window,wrap=WORD,bd=1,
                              yscrollcommand=self.recipe_scrollbar.set,
                              pady=10,
                              width=40)
        self.text_area.grid(row=1, column=2,sticky=N+S+W)
        self.recipe_scrollbar.config(command=self.text_area.yview)
        self.recipe_scrollbar.grid(row=1, column=3,sticky=N+S+E, rowspan=2)
                
        root.bind("<F1>", self.clear_listbox)
        root.bind("<Escape>", self.quit_app)
   
root = Tk()
X_WIDTH = root.winfo_screenwidth()
Y_HEIGHT = root.winfo_screenwidth()
root.wm_attributes('-fullscreen','true')
book = RecipeBook(root)
root.mainloop()
        

        

