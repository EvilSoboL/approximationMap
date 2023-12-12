import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PATH_TO_EXCEL = os.path.join(DATA_DIR, "GUR_general_data.xlsx")
PATH_TO_DB = os.path.join(DATA_DIR, "experiments.db")

LISTS_TO_CONVERT_TO_KG_H = ['дт_воздух', 'дт_пар', 'нефть_пар', 'мазут_пар', 'Мазут_пар_2', 'мазут_воздух']