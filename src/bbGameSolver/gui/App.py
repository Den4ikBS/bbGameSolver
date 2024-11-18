import PIL.Image
import numpy as np
import time
import PIL
import configparser
import pywinstyles
from customtkinter import *
from tktooltip import ToolTip

from ..config import *
from .gui_tools import *
from ..calc import DGame


set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

'''
esc doesn't work
add localization
load font from file
'''

class StartPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_start_page()

    def create_start_page(self):
        self.create_background()
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.lbl_hello = create_label(self.main_frame,
                                text='Это\nрешатель\nматричных\nигр',
                                )

        self.btn_start = create_button(self.main_frame,
                                    text='начать',
                                    cmd=lambda: self.controller.show_frame("MatrixPage"),
                                    )
        
    def place_widgets(self):
        self.lbl_hello.grid(row=0, column=0, padx=80, pady=5, sticky="s")
        self.btn_start.grid(row=1, column=0, padx=10, pady=5, sticky="n")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  

    def create_background(self):
        self.bg_image = CTkImage(PIL.Image.open("../assets/images/matrix.jpg"), size=(WIDTH, HEIGHT))
        self.bg_image_label = create_label(self, image=self.bg_image, text="")
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = CTkFrame(self, corner_radius=0, width=240)
        self.main_frame.pack(expand=1, fill=Y)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid(row=0, column=0, sticky="ns")


class MatrixPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_matrix_page()

    def create_matrix_page(self):
        self.create_widgets()
        
        self.entry_x.bind("<KeyRelease>", self.update_matrix_frame)
        self.entry_y.bind("<KeyRelease>", self.update_matrix_frame)
        
        for widget in [self.btn_upload, self.btn_save, self.btn_reset]:
            self.menu.add_widget(widget)

        self.place_widgets()
    
    def create_widgets(self):
        self.lbl_frame = CTkFrame(self, corner_radius=10)
        self.menu = self.add_menu()
        self.navbar = self.add_navbar()
        self.entry_x = create_entry(self.lbl_frame, width=40)
        self.entry_y = create_entry(self.lbl_frame, width=40)
        self.entry_x.delete(0, END)
        self.entry_x.insert(0, "2")
        self.entry_y.delete(0, END)
        self.entry_y.insert(0, "2")
        self.matrix_frame = self.add_matrix(int(self.entry_x.get()), int(self.entry_y.get()))

        self.lbl_shape = create_label(self.lbl_frame, 
                                      text='Размер матрицы:'
                                      )
        
        self.lbl = create_label(self.lbl_frame,
                           text='x',
                           )
        self.btn_save = create_button(self.menu,
                                      text='сохранить',
                                      cmd=self.button_save_callback,
                                      )
        
        self.btn_upload = create_button(self.menu,
                                        text='загрузить',
                                        cmd=self.button_upload_callback,
                                        )
        
        self.btn_reset = create_button(self.menu,
                                       text='сбросить',
                                       cmd=self.controller.reset,
                                       )
        
        self.btn_solve = create_button(self.menu,
                                       text='решить',
                                       cmd=self.solve,
                                       )
        
        tooltips = {self.btn_save: "сохранить матрицу в файл", 
                    self.btn_upload: "загрузить матрицу из файла",
                    self.btn_reset: "сбросить матрицу", 
                    self.btn_solve: "решить матричную игру",
                    }
        
        for k, v in tooltips.items():
            self.create_tooltip(k, v)
        
    def create_tooltip(self, widget, msg=""):
        ToolTip(widget, msg=msg, delay=0.01, follow=True,
        parent_kwargs={"bg": TT_BORDER_COLOR, "padx": 3, "pady": 3},
        fg=TT_TEXT_COLOR, bg=TT_BG_COLOR, padx=7, pady=7, font=my_font)

    def place_widgets(self):
        for widget in [self.btn_save, self.btn_upload, self.btn_reset, self.btn_solve]:
            self.menu.add_widget(widget)

        self.navbar.pack(side=BOTTOM, padx=10, pady=10, fill=X)
        self.menu.pack(side=LEFT, anchor=NW, padx=10, pady=10, fill=Y)

        self.lbl_shape.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.entry_x.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.lbl.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.entry_y.pack(side=LEFT, anchor=NW, padx=10, pady=10)

        self.lbl_frame.pack(side=TOP, anchor=NW, padx=10, pady=10, fill=X)
        self.matrix_frame.pack(side=TOP, anchor=NW, padx=10, pady=10, fill=BOTH, expand=1)      

    def add_matrix(self, rows, cols):
        # self.matrix_frame = MatrixTable(self, rows, cols)
        self.matrix_frame = MatrixTable(self, rows, cols)
        return self.matrix_frame
    
    def add_navbar(self):
        self.navbar = NavBar(self, 
                             cmd_prev=lambda: self.controller.show_frame("StartPage"), 
                             cmd_next=lambda: self.controller.show_frame("ResultPage"),
                             )
        return self.navbar
    
    def add_menu(self):
        self.menu = Menu(self)
        return self.menu

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
        self.mat = self.matrix_frame.get_matrix_data()
        g = DGame(self.mat)
        self.s1, self.s2 = g.solve(n=1000)
        self.s1 = self.s1.round(2)
        self.s2 = self.s2.round(2)
        print(self.s1)
        print(self.s2)
        # print(self.s1, self.s2)
        self.controller.frames["ResultPage"].res_frame.update_res(self.s1, self.s2)
        self.controller.show_frame("ResultPage")


class ResultPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.create_result_page()

    def create_result_page(self):
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.menu = self.add_menu() 
        self.res_frame = self.add_res()
        self.navbar = self.add_navbar() 

        self.btn_reset = create_button(self.menu,
                                       text='сбросить',
                                       cmd=self.controller.reset,
                                       )
        
        tooltips = {self.btn_reset: "сбросить матрицу"}
        
        for k, v in tooltips.items():
            self.create_tooltip(k, v)
        
    def create_tooltip(self, widget, msg=""):
        ToolTip(widget, msg=msg, delay=0.01, follow=True,
        parent_kwargs={"bg": TT_BORDER_COLOR, "padx": 3, "pady": 3},
        fg=TT_TEXT_COLOR, bg=TT_BG_COLOR, padx=7, pady=7, font=my_font)

    def place_widgets(self):
        for widget in [self.btn_reset]:
            self.menu.add_widget(widget)

        self.navbar.pack(side=BOTTOM, padx=10, pady=10, fill=X)
        self.menu.pack(side=LEFT, anchor=NW, padx=10, pady=10, fill=Y)
        self.res_frame.pack(side=RIGHT, anchor=NE, padx=10, pady=10, fill=BOTH, expand=1)
        

    def add_navbar(self):
        img = CTkImage(PIL.Image.open("../assets/images/refresh.png"), size=(14, 14))
        self.navbar = NavBar(self, 
                    cmd_prev=lambda: self.controller.show_frame("MatrixPage"), 
                    cmd_next=self.controller.reset,
                    text_next="", #↺
                    img=img,
                    tooltips=(None, "сбросить матрицу")
                    )
        return self.navbar
    
    def add_menu(self):
        self.menu = Menu(self) 
        return self.menu
    
    def add_res(self):
        self.res_frame = ResFrame(self, None, None) #self.controller.frames["MatrixPage"].s1, self.controller.frames["MatrixPage"].s2
        return self.res_frame


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
    

class NavBar(CTkFrame):
    def __init__(self, parent, cmd_prev, cmd_next, text_next='>', img=None, tooltips=(None, None)):
        super().__init__(parent, width=WIDTH, corner_radius=20)
        self.cmd_prev = cmd_prev
        self.cmd_next = cmd_next
        self.text_next = text_next
        self.img = img
        self.tooltips = tooltips
        self.create_navbar()

    def create_navbar(self):
        btn_next = create_button(self,
                                 text=self.text_next,
                                 cmd=self.cmd_next,
                                 width=36,
                                 height=36,
                                 bg_color="#000001",
                                 image=self.img,
                                 )
        
        btn_prev = create_button(self,
                                 text='<',
                                 cmd=self.cmd_prev,
                                 width=36,
                                 height=36,
                                 bg_color="#000001",
                                 )
        
        pywinstyles.set_opacity(btn_prev, color="#000001")
        pywinstyles.set_opacity(btn_next, color="#000001")

        if self.tooltips[0]:
            self.create_tooltip(btn_prev, self.tooltips[0])
        if self.tooltips[1]:
            self.create_tooltip(btn_next, self.tooltips[1])
        
        btn_prev.pack(side="left")
        btn_next.pack(side="right")

    def create_tooltip(self, widget, msg=""):
        ToolTip(widget, msg=msg, delay=0.01, follow=True,
        parent_kwargs={"bg": TT_BORDER_COLOR, "padx": 3, "pady": 3},
        fg=TT_TEXT_COLOR, bg=TT_BG_COLOR, padx=7, pady=7, font=my_font)


class Menu(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=220, corner_radius=10)
        self.rows = 0
        self.grid_columnconfigure(0, weight=1)

    def add_widget(self, widget):
        widget.grid(row=self.rows, column=0, sticky="ew", padx=8, pady=10)
        self.rows += 1


class ResFrame(CTkScrollableFrame):
    def __init__(self, parent, vector1, vector2):
        super().__init__(parent, orientation="horizontal", width=500)
        self.vector1 = vector1
        self.vector2 = vector2
        self.create_res()

    def create_res(self):
        self.lbl_vec1 = create_label(self,
                                     text=self.vector1,
                                     )
        
        self.lbl_vec2 = create_label(self,
                                     text=self.vector2,
                                     )
        
        self.lbl1 = create_label(self,
                                 text='Результат 1:',
                                 )
        
        self.lbl2 = create_label(self,
                                 text='Результат 2:',
                                 )
        
        self.lbl1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.lbl_vec1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.lbl2.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.lbl_vec2.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    def update_res(self, new_s1, new_s2):
        self.lbl_vec1.configure(text=new_s1)
        self.lbl_vec2.configure(text=new_s2)


class MatrixTable(CTkFrame):
    def __init__(self, parent, rows, cols):
        super().__init__(parent, width=500)
        self.rows = rows
        self.cols = cols
        self.entries = []
        self.create_sb_frame()
        self.create_matrix()

    def create_sb_frame(self):
        self.canvas = CTkCanvas(self, bg="gray17", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scrollbar = CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar = CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.scrollable_frame = CTkFrame(self.canvas, fg_color="transparent")
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_matrix(self):
        self.reset_matrix()
        self.mat_entries = np.empty((self.rows, self.cols), dtype=object)
        start = time.time()
        for i in range(self.rows):
            for j in range(self.cols):
                entry = create_entry(self.scrollable_frame,
                                     width=54,
                                     height=30,
                                     )
                # entry = tk.Entry(self.scrollable_frame)
                lbl_r = create_label(self.scrollable_frame, text=f"{i}")
                lbl_c = create_label(self.scrollable_frame, text=f"{j}")
                lbl_r.grid(row=i + 1, column=0, sticky="w", padx=10)
                lbl_c.grid(row=0, column=j + 1, sticky="n")
                entry.grid(row=i + 1, column=j + 1, padx=2, pady=2, sticky="w")
                self.mat_entries[i, j] = entry
        end = time.time()
        # print(f"{self.rows}x{self.cols}",end-start)

    def update_matrix_size(self, new_rows, new_cols):
        self.rows = new_rows
        self.cols = new_cols
        self.create_matrix()

    def reset_matrix(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def get_matrix_data(self):
        data = np.empty((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                data[i, j] = float(self.mat_entries[i, j].get())

        return data
    
    def set_matrix_data(self, mat):
        self.update_matrix_size(mat.shape[0], mat.shape[1])
        for i in range(self.rows):
            for j in range(self.cols):
                self.mat_entries[i, j].delete(0, END)
                self.mat_entries[i, j].insert(0, mat[i, j])

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class ToplevelWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200")


if __name__ == "__main__":
    app = App()
    app.mainloop()