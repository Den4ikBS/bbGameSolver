import PIL.Image
import numpy as np
import time
import tkinter as tk
import tkinter.ttk as ttk
import PIL
import pywinstyles
from customtkinter import *
from tktooltip import ToolTip

from ..config import *
from .gui_widgets import *
from .gui_tools import *
from ..utils import *
from ..calc import DGame


set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

'''
esc doesn't work
scrollbar for logs table doesn't work
'''

class StartPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_background()
        self.create_widgets()
        self.place_widgets()        

    def create_widgets(self):
        self.lbl_hello = create_label(self.main_frame,
                                      textvar=self.controller.text_vars['welcome_message']
                                      )

        self.btn_start = create_button(self.main_frame,
                                       textvar=self.controller.text_vars['start'],
                                       cmd=lambda: self.controller.show_frame("MatrixPage"),
                                       )
        
        self.translate_img = CTkImage(PIL.Image.open("../assets/images/translate.png"), size=(22, 22))
        self.btn_lang = create_button(self.main_frame,
                                      width=36,
                                      height=36,
                                      image=self.translate_img,
                                      cmd=self.controller.switch_language,
                                      )
        
    def place_widgets(self): 
        self.lbl_hello.pack(side=TOP, anchor=CENTER, padx=10, pady=(HEIGHT//2-100,5))
        self.btn_start.pack(side=TOP, anchor=CENTER, padx=10, pady=5)
        self.btn_lang.pack(side=TOP, anchor=CENTER, padx=10, pady=5)

    def create_background(self):
        self.bg_image = CTkImage(PIL.Image.open("../assets/images/neon-green-matrix.jpg"), size=(WIDTH, HEIGHT))
        self.bg_image_label = create_label(self, image=self.bg_image, text="")
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.main_frame = CTkFrame(self, corner_radius=0, width=240, height=HEIGHT)
        self.main_frame.pack(expand=1, fill=Y, ipady=100)


class MatrixPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.place_widgets()
    
    def create_widgets(self):
        self.lbl_frame = CTkFrame(self, corner_radius=10)
        self.iter_frame = CTkFrame(self, corner_radius=10)
        self.menu = Menu(self)
        self.navbar = self.add_navbar()
        self.entry_x = create_entry(self.lbl_frame, width=40)
        self.entry_y = create_entry(self.lbl_frame, width=40)
        self.entry_x.delete(0, END)
        self.entry_x.insert(0, "2")
        self.entry_y.delete(0, END)
        self.entry_y.insert(0, "2")
        self.entry_x.bind("<KeyRelease>", self.update_matrix_frame)
        self.entry_y.bind("<KeyRelease>", self.update_matrix_frame)
        self.matrix_frame = MatrixTable(self, int(self.entry_x.get()), int(self.entry_y.get()))

        self.lbl_shape = create_label(self.lbl_frame, 
                                      textvar=self.controller.text_vars['matrix_shape']
                                      )
        
        self.lbl = create_label(self.lbl_frame,
                                text='x',
                                )
        
        self.lbl_iter = create_label(self.iter_frame,
                                     textvar=self.controller.text_vars['num_iter']
                                     )
        
        self.cb_iter = create_combobox(self.iter_frame,
                                       vals=["20", "100", "1000"],
                                       cmd=self.get_iter
                                       )
        
        
        self.btn_save = create_button(self.menu,
                                      textvar=self.controller.text_vars['save'],
                                      cmd=self.button_save_callback,
                                      )
        
        self.btn_upload = create_button(self.menu,
                                        textvar=self.controller.text_vars['upload'],
                                        cmd=self.button_upload_callback,
                                        )
        
        self.btn_reset = create_button(self.menu,
                                       textvar=self.controller.text_vars['reset'],
                                       cmd=self.controller.reset,
                                       )
        
        self.btn_solve = create_button(self.menu,
                                       textvar=self.controller.text_vars['solve'],
                                       cmd=self.solve,
                                       )
        
        self.translate_img = CTkImage(PIL.Image.open("../assets/images/translate.png"), size=(22, 22))
        self.btn_lang = create_button(self.menu,
                                      image=self.translate_img,
                                      width=36, 
                                      height=36,
                                      cmd=self.controller.switch_language,
                                      )

        tooltips = {self.btn_save: lambda: self.controller.text_vars['tooltip_save'].get(),
                    self.btn_upload: lambda: self.controller.text_vars['tooltip_upload'].get(),
                    self.btn_reset: lambda: self.controller.text_vars['tooltip_reset'].get(),
                    self.btn_solve: lambda: self.controller.text_vars['tooltip_solve'].get(),
                    }
        
        for widget, msg_func in tooltips.items():
            self.create_tooltip(widget, msg_func)

    def place_widgets(self):
        for widget in [self.btn_lang, self.btn_save, self.btn_upload, self.btn_reset, self.btn_solve]:
            self.menu.add_widget(widget)

        self.navbar.pack(side=BOTTOM, padx=10, pady=(5,10), fill=X)
        self.menu.pack(side=LEFT, anchor=NW, padx=10, pady=10, fill=Y)

        self.lbl_shape.pack(side=LEFT, anchor=CENTER, padx=10, pady=10)
        self.entry_x.pack(side=LEFT, anchor=CENTER, padx=(10, 5), pady=10)
        self.lbl.pack(side=LEFT, anchor=CENTER, padx=0, pady=10)
        self.entry_y.pack(side=LEFT, anchor=CENTER, padx=(5, 10), pady=10)
        self.lbl_iter.pack(side=LEFT, anchor=CENTER, padx=(10, 10), pady=10)
        self.cb_iter.pack(side=LEFT, anchor=CENTER, padx=0, pady=10)

        self.lbl_frame.pack(side=TOP, anchor=NW, padx=10, pady=(10, 5), fill=X)
        self.iter_frame.pack(side=TOP, anchor=NW, padx=10, pady=(5, 5), fill=X)
        self.matrix_frame.pack(side=TOP, anchor=NW, padx=10, pady=(5, 10), fill=BOTH, expand=1)      

    
    def add_navbar(self):
        self.navbar = NavBar(self, 
                             cmd_prev=lambda: self.controller.show_frame("StartPage"), 
                             cmd_next=lambda: self.controller.show_frame("ResultPage"),
                             )
        return self.navbar

    def update_matrix_frame(self, event=None):
        try:
            rows = int(self.entry_x.get())
            cols = int(self.entry_y.get())
            self.matrix_frame.update_matrix_size(rows, cols)
        except ValueError:
            pass
        
    def button_upload_callback(self):
        file_path = filedialog.askopenfilename(title='Select a file', initialdir="../data/")
        g = DGame.from_tsv(file_path)
        self.mat = g.mtx
        self.entry_x.delete(0, END)
        self.entry_x.insert(0, self.mat.shape[0])
        self.entry_y.delete(0, END)
        self.entry_y.insert(0, self.mat.shape[1])
        self.matrix_frame.set_matrix_data(self.mat)

    def button_save_callback(self):
        mat = self.matrix_frame.get_matrix_data() 
        print(mat)
        file_path = filedialog.asksaveasfile(initialdir='../data',
                                             initialfile = 'Untitled.tsv',
                                             defaultextension=".tsv",
                                             )  
                
        to_tsv(mat, file_path)

    def solve(self):
        self.n_iter = int(self.cb_iter.get())
        self.mat = self.matrix_frame.get_matrix_data()
        g = DGame(self.mat)
        self.s1, self.s2 = g.solve(self.n_iter)
        self.controller.frames["ResultPage"].res_frame.update_res(self.s1.round(2), self.s2.round(2))
        self.controller.frames["ResultPage"].table_frame.reset_table()
        self.controller.frames["ResultPage"].table_frame.fill_table(g.log)
        self.controller.show_frame("ResultPage")

    def get_iter(self, choice):
        self.n_iter = int(self.cb_iter.get())
        
    def create_tooltip(self, widget, msg=""):
        ToolTip(widget, msg=msg, delay=0.01, follow=True,
        parent_kwargs={"bg": TT_BORDER_COLOR, "padx": 3, "pady": 3},
        fg=TT_TEXT_COLOR, bg=TT_BG_COLOR, padx=7, pady=7, font=my_font)


class ResultPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.table_frame = TableFrame(self, self.controller)
        self.menu = Menu(self)
        self.res_frame = ResFrame(self, None, None, self.controller)
        self.navbar = self.add_navbar() 

        self.btn_reset = create_button(self.menu,
                                       textvar=self.controller.text_vars['reset'],
                                       cmd=self.controller.reset,
                                       )
        
        self.translate_img = CTkImage(PIL.Image.open("../assets/images/translate.png"), size=(22, 22))
        self.btn_lang = create_button(self.menu,
                                      image=self.translate_img,
                                      width=36, 
                                      height=36,
                                      cmd=self.controller.switch_language,
                                      )
        
        tooltips = {self.btn_reset: lambda: self.controller.text_vars['reset'].get()}
        
        for k, v in tooltips.items():
            self.create_tooltip(k, v)
        
    def create_tooltip(self, widget, msg=""):
        ToolTip(widget, msg=msg, delay=0.01, follow=True,
        parent_kwargs={"bg": TT_BORDER_COLOR, "padx": 3, "pady": 3},
        fg=TT_TEXT_COLOR, bg=TT_BG_COLOR, padx=7, pady=7, font=my_font)

    def place_widgets(self):
        for widget in [self.btn_lang, self.btn_reset]:
            self.menu.add_widget(widget)

        self.navbar.pack(side=BOTTOM, padx=10, pady=(5, 10), fill=X)
        self.menu.pack(side=LEFT, anchor=NW, padx=10, pady=10, fill=Y)
        self.res_frame.pack(side=TOP, anchor=NE, padx=10, pady=(10,5), fill=X)
        self.table_frame.pack(side=RIGHT, anchor=NE, padx=10, pady=(5,10), fill=BOTH, expand=1)
        

    def add_navbar(self):
        img = CTkImage(PIL.Image.open("../assets/images/refresh.png"), size=(14, 14))
        self.navbar = NavBar(self, 
                             cmd_prev=lambda: self.controller.show_frame("MatrixPage"), 
                             cmd_next=self.controller.reset,
                             text_next="", #↺
                             img=img,
                             tooltips=(None, lambda: self.controller.text_vars['reset'].get())
                             )
        return self.navbar


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f'{WIDTH}x{HEIGHT}')
        self.container = CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.title('Matrix games')
        self.frames = {}
        self.popup_window = None
        self.bind("<F1>", self.open_popup)
        self.bind("<Escape>", self.close_popup)
        self.translations = load_translations()
        self.current_language = 'ru'
        self.text_vars = {
            'welcome_message': StringVar(),
            'start': StringVar(),
            'save': StringVar(),
            'upload': StringVar(),
            'reset': StringVar(),
            'solve': StringVar(),
            'matrix_shape': StringVar(),
            'result_1': StringVar(),
            'result_2': StringVar(),
            'tooltip_save': StringVar(),
            'tooltip_upload': StringVar(),
            'tooltip_reset': StringVar(),
            'tooltip_solve': StringVar(),
            'table_heading1': StringVar(),
            'table_heading2': StringVar(),
            'table_heading3': StringVar(),
            'table_heading4': StringVar(),
            'num_iter': StringVar(),
            }
        self.set_language(self.current_language)
        self.create_pages()
        self.show_frame("StartPage")
    
    def create_pages(self):
        for F in (StartPage, MatrixPage, ResultPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.container.grid_rowconfigure(0, weight=1)
            self.container.grid_columnconfigure(0, weight=1)
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def reset(self):
        matrix_page = self.frames["MatrixPage"]
        matrix_page.matrix_frame.reset_matrix()
        matrix_page.matrix_frame.update_matrix_size(2, 2)
        matrix_page.entry_x.delete(0, END)
        matrix_page.entry_x.insert(0, "2")
        matrix_page.entry_y.delete(0, END)
        matrix_page.entry_y.insert(0, "2")
        res_page = self.frames["ResultPage"]
        res_page.res_frame.lbl_vec1.configure(text="")
        res_page.res_frame.lbl_vec2.configure(text="")
        res_page.table_frame.reset_table()
    
    def open_popup(self, event=None):
        if self.popup_window is None or not self.popup_window.winfo_exists(): 
            self.popup_window = ToplevelWindow(self)        
            label = CTkLabel(self.popup_window, text="Хелпы")
            label.pack(pady=20)
            self.popup_window.title("Help")
            close_button = CTkButton(self.popup_window, text="close", command=self.close_popup)
            close_button.pack(pady=10)
            self.popup_window.focus_set()
            self.popup_window.grab_set()

    def close_popup(self, event=None):
        if self.popup_window is not None and self.popup_window.winfo_exists():
            self.popup_window.destroy()
            self.popup_window = None

    def set_language(self, language):
        for key, var in self.text_vars.items():
            translated_text = self.translations[language].get(key, f"[{key}]")
            var.set(translated_text)

    def switch_language(self):
        self.current_language = 'ru' if self.current_language == 'en' else 'en'
        self.set_language(self.current_language)


if __name__ == "__main__":
    app = App()
    app.mainloop()