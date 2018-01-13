from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import *
import configparser

class OptionMenu:

    def __init__(self, main):
        """Creates an options menu object window, pass main program window during
        initialization"""
        self.main = main
        self.top = Toplevel()
        self.top.overrideredirect(1)
        self.top.geometry("+10+10")

        frame = Frame(self.top, bd=5, bg='black')
        frame.pack()
        header_frame = Frame(frame, bg="white")
        header_frame.pack(side=TOP, fill=X)
        header = Label(header_frame, text="Options")
        header.config(font=("Arial", "32", "bold"),bg="white")
        header.pack(side=TOP)

        options_frame = Frame(frame,
                                pady=5,
                                padx=5,
                                bg="white")
        options_frame.pack(fill=BOTH)
        bg_color_label = Label(options_frame,
                               text="Toolbar Color",
                               font=("Arial", "12", "bold"),
                               bg="white",
                               pady=5)
        bg_color_label.grid(row=0, column=0, sticky=W)

        self.bg_color_button = Button(options_frame,
                                 bg=self.main.TOOLBAR_COLOR,
                                 width=10,
                                 command=lambda: self.update_color('toolbar',
                                                   self.main.recipe_toolbar,
                                                   self.bg_color_button,
                                                   self.main.mainTitleVar_label))
        self.bg_color_button.grid(row=0, column=1, sticky=W+E)

        recipe_color_label = Label(options_frame,
                               text="Background Color",
                               font=("Arial", "12", "bold"),
                               bg="white",
                               pady=5)
        recipe_color_label.grid(row=1, column=0, sticky=W)

        self.recipe_color_button = Button(options_frame,
                                 bg=self.main.RECIPE_FRAME_COLOR,
                                 width=10,
                                 command=lambda: self.update_color('recipe',
                                                   self.main.recipe_window,
                                                   self.recipe_color_button,
                                                   self.main.seperator))
        self.recipe_color_button.grid(row=1, column=1, sticky=W+E)

        options_close_button = Button(options_frame,
                                      width=10,
                                      text="Close",
                                      font="bold",
                                      padx=5,
                                      command=lambda: self.close_option_menu())
        options_close_button.grid(row=2, column=2, sticky=SW)

        print("Options menu opened!")

    def get_Color(self):
        """Returns an RGB value and a hexadecimal value for the selected color.
        ex. ((R,G,B), #000000)"""
        color = askcolor()
        if color[1] == None:
            return None
        else:
            return color[0], color[1]

    def luminosity(self, tup):
        """Module that returns result of RGB tuple passed through the luminosity formula.
        Result will either be #ffffff if Lum <= .30, or #000000"""
        color = tup
        R1 = color[0]/255
        G1 = color[1]/255
        B1 = color[2]/255
        RGB = [R1, G1, B1]
        Cmax = max(RGB)
        Cmin = min(RGB)
        lum = (Cmax + Cmin) / 2
        if lum <= .30:
            return '#ffffff'
        else:
            return '#000000'
        print(lum)

    def update_color(self, frame, *args):
        """Updates a GUI object's color."""
        try:
            RGB, color = self.get_Color()

            if frame == 'toolbar':
                #print("toolbar is being configured")
                #self.main.TOOLBAR_COLOR = str(color)
                for widget in args:
                    widget.config(bg=color)
                    widget.update()
                self.config_update(color, 'TOOLBAR_COLOR')

                Lcolor = self.luminosity(RGB)
                self.main.mainTitleVar_label.config(fg = Lcolor)
                self.main.mainTitleVar_label.update()
                self.config_update(Lcolor, 'mainTitleVar_Color')

            if frame == 'recipe':
                #print("recipe window is being configured")
                for widget in args:
                    widget.config(bg=color)
                    widget.update()
                self.config_update(color, 'RECIPE_FRAME_COLOR')
        except:
            pass
        self.top.lift()


    def config_update(self, color, widget):
        """Updates config colors in the config.ini file."""
        f = open('config.ini', 'w')
        self.main.Config.set('colors', widget, str(color))
        self.main.Config.write(f)
        f.close()

    def close_option_menu(self):
        """Command to close the options menu."""
        #self.options_button.button['state'] = 'active'
        self.top.destroy()
