from tkinter import *
from optionsmenu import OptionMenu
import os

class GUI_Control:

    def __init__(self, interface):
        self.interface = interface

    def quit_app(self, event=None):
        """Closes the application window"""
        self.interface.root.destroy()

    def options_menu(self):
        OptionMenu(self.interface)

    def change_type(self, food_type, event=None):
        """Changes the current food type selected."""
        self.interface.mainTitleVar.set(food_type)
        self.clear_text()
        self.RECIPE_DIRECTORY = "Recipes/" + food_type + "/"
        self.fill_listbox()

    def open_recipe(self, recipe, event=None):
        """Opens a text file containing a recipe and inserts it in into the
        recipe frame."""
        with open(self.RECIPE_DIRECTORY + recipe + '.txt','r') as txt_file:
            if txt_file:
                self.clear_text()
                self.interface.text_area.insert(1.0, txt_file.read())

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
        listbox_index = 1
        for recipe in os.listdir(self.RECIPE_DIRECTORY):
            if recipe.endswith(".txt"):
                self.interface.recipe_lb.insert(listbox_index, recipe[0:-4])
                listbox_index += 1

    def clear_text(self, event=None):
        """Helper method to clear recipe text."""
        self.interface.text_area.delete(1.0, END)

    def clear_listbox(self, event=None):
        """Helper method to clear listbox text."""
        self.interface.recipe_lb.delete(0,END)
