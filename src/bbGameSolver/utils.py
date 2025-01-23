import pandas as pd
import configparser


def to_tsv(mtx, csv_path):
    """Выгрузка матрицы в файл в виде текстовой таблицы."""
    return pd.DataFrame(mtx).to_csv(csv_path, index=False, header=False, sep='\t')

def load_translations(file_path='../localization.ini'):
    """Загрузка словаря локализации из файла конфигурации .ini"""
    config = configparser.ConfigParser()
    with open(file_path, 'r', encoding='utf-8') as f:
        config.read_file(f)
    translations = {section: dict(config.items(section)) for section in config.sections()}
    return translations