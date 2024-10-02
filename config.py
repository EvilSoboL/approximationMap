import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_RES_DIR = os.path.join(BASE_DIR, "data_results")
PLOT_DIR = os.path.join(BASE_DIR, "plot")

PATH_TO_EXCEL = os.path.join(DATA_DIR, "GUR_general_data.xlsx")
PATH_TO_DB = os.path.join(DATA_DIR, "experiments.db")

PATH_TO_SOURCE_PLOT = os.path.join(PLOT_DIR, "source")
PATH_TO_RBF_PLOT = os.path.join(PLOT_DIR, "Rbf(linear)+med.filter(20)+non negative")
PATH_TO_CO_MIN_PLOT = os.path.join(PLOT_DIR, "CO_minimum")
PATH_TO_O2_MIN_PLOT = os.path.join(PLOT_DIR, "O2_minimum")

PATH_TO_EXCEL_RESULT = os.path.join(BASE_DIR, "excel_results")

LISTS_TO_CONVERT_TO_KG_H = ['дт_воздух', 'дт_пар', 'нефть_пар', 'мазут_пар', 'Мазут_пар_2', 'мазут_воздух']
COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3 = ['CO', 'NOx']
STANDARD_O2 = 3

ADDITIVES = ['air', 'steam']
MEASURING_COMPONENTS = ['O2', 'CO', 'NO', 'NO2', 'NOx', 'CO2', 'SO2']

# Компоненты которые измеряются в процентах
PROCENT_COMPONENT = ['CO2', 'O2']
