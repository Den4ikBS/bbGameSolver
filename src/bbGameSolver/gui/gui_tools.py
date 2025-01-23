import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import pywinstyles
from customtkinter import *
from tktooltip import ToolTip

from ..config import *
from .gui_widgets import *
from .gui_tools import *
from ..utils import *


class NavBar(CTkFrame):
    """Класс виджета навигационной панели"""
    def __init__(self, parent, cmd_prev, cmd_next, text_next='>', img=None, tooltips=(None, None)):
        super().__init__(parent, width=WIDTH, corner_radius=20)
        self.cmd_prev = cmd_prev
        self.cmd_next = cmd_next
        self.text_next = text_next
        self.img = img
        self.tooltips = tooltips
        self.create_navbar()

    def create_navbar(self):
        """Создание виджетов навигационной панели """
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
        """Создание подсказок при наведении курсора"""
        ToolTip(widget, msg=msg, delay=0.01, follow=True,
        parent_kwargs={"bg": TT_BORDER_COLOR, "padx": 3, "pady": 3},
        fg=TT_TEXT_COLOR, bg=TT_BG_COLOR, padx=7, pady=7, font=my_font)


class Menu(CTkFrame):
    """Класс фрейма меню"""
    def __init__(self, parent):
        super().__init__(parent, width=220, corner_radius=10)

    def add_widget(self, widget):
        """Добавление виджетов в меню"""
        widget.pack(side=TOP, anchor=NW, padx=10, pady=10)


class ResFrame(CTkScrollableFrame):
    """Класс создания окна вывода результатов расчетов"""
    def __init__(self, parent, vector1, vector2, controller):
        super().__init__(parent, orientation="horizontal", height=160)
        self.vector1 = vector1
        self.vector2 = vector2
        self.controller = controller
        self.create_res()

    def create_res(self):
        """Создание виджетов для вывода результата"""
        self.lbl_vec1 = create_label(self,
                                     text=self.vector1,
                                     )
        
        self.lbl_vec2 = create_label(self,
                                     text=self.vector2,
                                     )
        
        self.lbl1 = create_label(self,
                                 textvar=self.controller.text_vars['result_1'],
                                 )
        
        self.lbl2 = create_label(self,
                                 textvar=self.controller.text_vars['result_2'],
                                 )
        
        self.lbl1.grid(row=0, column=0, padx=10, pady=(10,5), sticky="w")
        self.lbl_vec1.grid(row=1, column=0, padx=10, pady=(5,5), sticky="w")
        self.lbl2.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.lbl_vec2.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    def update_res(self, new_s1, new_s2):
        """Обновление значений полей вывода результата"""
        self.lbl_vec1.configure(text=new_s1)
        self.lbl_vec2.configure(text=new_s2)


class MatrixTable(CTkFrame):
    """Класс создания окна ввода и редактирования матрицы"""
    def __init__(self, parent, rows, cols):
        super().__init__(parent, width=500)
        self.rows = rows
        self.cols = cols
        self.entries = []
        self.create_sb_frame()
        self.create_matrix()

    def create_sb_frame(self):
        """Создание фрейма для расположения матрицы"""
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
        """Создание виджета матрицы"""
        self.reset_matrix()
        self.mat_entries = np.empty((self.rows, self.cols), dtype=object)
        # start = time.time()
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
        # end = time.time()
        # print(f"{self.rows}x{self.cols}",end-start)

    def update_matrix_size(self, new_rows, new_cols):
        """Обновление размера матрицы"""
        self.rows = new_rows
        self.cols = new_cols
        self.create_matrix()

    def reset_matrix(self):
        """Сброс матрицы"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def get_matrix_data(self):
        """Получение введенных в матрицу данных"""
        data = np.empty((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                data[i, j] = float(self.mat_entries[i, j].get())

        return data
    
    def set_matrix_data(self, mat):
        """Запись данных в ячейки матрицы"""
        self.update_matrix_size(mat.shape[0], mat.shape[1])
        for i in range(self.rows):
            for j in range(self.cols):
                self.mat_entries[i, j].delete(0, END)
                self.mat_entries[i, j].insert(0, mat[i, j])

    def on_frame_configure(self, event=None):
        """Вспомогательная фнукция"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class ToplevelWindow(CTkToplevel):
    """Класс создания всплывающего окна"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200")


class TableFrame(CTkScrollableFrame):
    """Класс создания таблицы вывода итераций"""
    def __init__(self, parent, controller):
        super().__init__(parent, width=500, orientation="horizontal")
        self.controller = controller
        self.create_table()
    
    def create_table(self):
        """Созданиие и конфигурация таблицы"""
        self.rows = int(self.controller.frames["MatrixPage"].entry_x.get())
        self.cols = int(self.controller.frames["MatrixPage"].entry_y.get())
        columns = tuple((f"#{i}" for i in range(1, self.rows + self.cols + 1)))
        self.tree = ttk.Treeview(self, show="headings", columns=columns)
        for i in range(1, self.rows + 1):
            self.tree.heading(f"#{i}", text=f"Выигрыши \nигрока 1:{i}")

        for i in range(self.rows + 1, self.rows + self.cols + 1):
            self.tree.heading(f"#{i}", text=f"Выигрыши \nигрока 2:{i - self.rows}")

        self.tree.heading('#0', text='\n\n')

        for c in columns:
            self.tree.column(c, anchor="center")

        style = ttk.Style()
    
        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=30,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=(my_font[0], 16),
                        )
        
        style.map('Treeview', background=[('selected', '#186c44')])

        style.configure("Treeview.Heading",
                        background="#333333", #696969
                        foreground="white",
                        relief="flat",
                        font=(my_font[0], 18),
                        rowheight=30,
                        )
        
        style.map("Treeview.Heading",
                    background=[('active', '#2fa572')])      

        self.tree.pack(side=TOP, anchor=N, padx=10, pady=10, fill=BOTH, expand=1)
        # ysb.pack(side=RIGHT, fill=Y)

    def fill_table(self, data):
        """Запись данных в таблицу"""
        print(data)
        for row in data:
            self.tree.insert("", tk.END, values=tuple(row[-(self.rows + self.cols):]))

    def reset_table(self):
        """Сброс данных в таблице"""
        self.tree.destroy()
        self.create_table()