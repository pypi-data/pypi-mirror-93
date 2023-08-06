"""Random testing"""

from generallibrary.time import sleep

from generalgui import App, Page, Button, Label, OptionMenu, Checkbutton, Entry, LabelCheckbutton, LabelEntry, Spreadsheet

import tkinter as tk
import inspect

import pandas as pd


df = pd.DataFrame({"a": [0, 1]})
df.index = ["hi", "there"]
print(df)
print(df.shape)

def x():
    page.app.widget.after(2000, spreadsheet.remove)
def y():
    page.app.widget.after(2000, lambda: print(5))
    # page.app.widget.after(2000, spreadsheet.hide)
def z():
    page.app.widget.after(2000, spreadsheet.app.remove)


page = Page(App())
Button(page, "Remove in 2 seconds", x)
Button(page, "Hide in 2 seconds", y)
Button(page, "Quit in 2 seconds", z)
Button(page, "Show", lambda: spreadsheet.show())

spreadsheet = Spreadsheet(page)
spreadsheet.dataFrame = pd.DataFrame(index=[x for x in range(20)], columns=["hi", "there"])
spreadsheet.loadDataFrame()

# button.widget.after(1000, button.click)

# page.app.rainbow()

page.show()





# page.show(mainloop=False)
# page.app.remove()


