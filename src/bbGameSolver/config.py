"""Модуль конфигурации. Предназначен для хранения глобальных параметров проекта."""
import customtkinter 

WIDTH = 800   # начальная ширина окна
HEIGHT = 600  # начальная высота окна
# загрузка файла шрифтов
customtkinter.FontManager.load_font("../assets/fonts/RobotoMono-VariableFont_wght.ttf")
# new_font = ("Russo One", 18)
my_font = ("Roboto Mono", 18)  # используемый шрифт
TT_TEXT_COLOR = "#ffffff"      # код цвета текста
TT_BG_COLOR = "#696969"        # код цвета фона
TT_BORDER_COLOR = "#333333"    # код цвета границ

