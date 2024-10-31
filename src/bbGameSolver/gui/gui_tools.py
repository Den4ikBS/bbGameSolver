import pandas as pd
from customtkinter import *

from ..config import my_font


def clear_page(master):
    for i in master.winfo_children():
        i.destroy()  

def create_entry(master, width=24, height=24, fg_color="transparent"):
        entry = CTkEntry(master=master,
                         width=width,
                         height=height,
                         corner_radius=20,
                         fg_color=fg_color,
                         font=(my_font[0], 14),
                         )
        entry.insert(0, 0)  
        return entry

def create_label(master, text='', image=None):
    label = CTkLabel(master=master,
                     text=text,
                     image=image,
                     font=my_font,
                     )
    return label

def create_button(master, text='', cmd=None, width=200, height=34, corner_radius=20, bg_color="transparent", image=None):
    button = CTkButton(master=master,
                       text=text,
                       command=cmd,
                       width=width,
                       height=height,
                       corner_radius=corner_radius,
                       border_width=None,
                       border_spacing=2,
                       bg_color=bg_color,
                       fg_color=None,
                       hover_color=None,
                       border_color=None,
                       text_color_disabled=None,
                       background_corner_colors=None,
                       image=image,  
                       font=my_font,                      
                       )
    return button

def create_optionmenu(master, vals, cmd=None):
    optionmenu_var = StringVar(value=vals[0])
    optionmenu = CTkOptionMenu(master=master,
                               width=80,
                               values=vals,
                               command=cmd,
                               variable=optionmenu_var,
                               corner_radius=20,
                               font=my_font,
                               )
    
    return optionmenu

def optionmenu_map_callback(choice):    
    return choice

def to_tsv(mtx, csv_path):
    return pd.DataFrame(mtx).to_csv(csv_path, index=False, header=False, sep='\t')