import pandas as pd

from config import LISTS_TO_CONVERT_TO_KG_H
from handlers.database import DatabaseHandler


class ExcelHandler:
    def __init__(self, path_to_source):
        self.path_to_source = path_to_source
        self.all_sheets = None
        self.convert_to_kg_h = LISTS_TO_CONVERT_TO_KG_H
        self.converted_sheets = None

        self.read_excel()
        self.convert_g_s_to_kg_h()

    def read_excel(self) -> None:
        self.all_sheets = pd.read_excel(self.path_to_source, sheet_name=None)

    def convert_g_s_to_kg_h(self) -> None:
        converted_sheets = dict()
        for key, df in self.all_sheets.items():
            if key in self.convert_to_kg_h:
                if '_пар' in key:
                    df['Q_топливо, г/ч'] = df['Q_топливо, г/ч']/1000
                    df['Q_пар, г/ч'] = df['Q_пар, г/ч'] / 1000

                    df.rename(columns={
                        'Q_топливо, г/ч': 'Q_топливо, кг/ч',
                        'Q_пар, г/ч': 'Q_пар, кг/ч'}, inplace=True)
                else:
                    df['Q_топливо, г/ч'] = df['Q_топливо, г/ч'] / 1000
                    df['Q_возд_рот, г/ч'] = df['Q_возд_рот, г/ч'] / 1000

                    df.rename(columns={
                        'Q_топливо, г/ч': 'Q_топливо, кг/ч',
                        'Q_возд_рот, г/ч': 'Q_возд_рот, кг/ч'}, inplace=True)
                converted_sheets[key] = df
            else:
                converted_sheets[key] = df
        self.converted_sheets = converted_sheets

    #def save_sheets_to_bd(self):

