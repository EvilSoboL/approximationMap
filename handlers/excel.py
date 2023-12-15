import pandas as pd
import numpy as np

from config import LISTS_TO_CONVERT_TO_KG_H
from handlers.database import DatabaseHandler


class ExcelHandler:
    def __init__(self, path_to_source):
        self.path_to_source = path_to_source
        self.all_sheets = None
        self.convert_to_kg_h = LISTS_TO_CONVERT_TO_KG_H
        self.converted_sheets = None
        self.cleaned_sheets = None

        self.database = DatabaseHandler()

        self.read_excel()
        self.convert_g_s_to_kg_h()
        self.clean_sheets_from_str()

        self.save_converted_sheets_to_bd()

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

    def clean_sheets_from_str(self) -> None:
        """
        Метод, который очищает str значения в df в колонках, где должны быть записаны float значения
        """
        cleaned_sheets = dict()
        for key, df in self.converted_sheets.items():
            df.replace('-', np.nan, inplace=True)
            df.replace('нестабильная подача', np.nan, inplace=True)
            cleaned_sheets[key] = df
        self.cleaned_sheets = cleaned_sheets

    def save_converted_sheets_to_bd(self) -> None:
        for key, df in self.cleaned_sheets.items():
            if key == 'дт_воздух':
                for _, row in df.iterrows():
                    if pd.isna(row['Q_топливо, кг/ч']):
                        continue
                    self.database.insert_into_experiments(
                        fuel_id=1,
                        F_fuel=row['Q_топливо, кг/ч'],
                        F_air=row['Q_возд_рот, кг/ч'],
                        F_steam=None,
                        O2=row['O2'],
                        CO=row['CO'],
                        NO=row['NO'],
                        NO2=row['NO2'],
                        NOx=row['NOX'],
                        CO2=row['СО2'],  # РУССКИЕ СИМВОЛЫ!
                        SO2=row['SO2'],
                        P_air=None,
                        P_steam=None,
                        comments=row['Эксперимент'],
                        t_wg=row['Twg, oC']
                    )
            elif key == 'дт_пар':
                for _, row in df.iterrows():
                    if pd.isna(row['Q_топливо, кг/ч']):
                        continue
                    self.database.insert_into_experiments(
                        fuel_id=1,
                        F_fuel=row['Q_топливо, кг/ч'],
                        F_air=None,
                        F_steam=row['Q_пар, кг/ч'],
                        O2=row['O2'],
                        CO=(row['CO']+row['CO (map)'])/2,
                        NO=row['NO'],
                        NO2=row['NO2'],
                        NOx=row['NOX'],
                        CO2=row['СО2'],  # РУССКИЕ СИМВОЛЫ!
                        SO2=row['SO2'],
                        P_air=None,
                        P_steam=row['P_пар, атм'],
                        comments=row['Эксперимент'],
                        t_wg=row['Twg, oC']
                    )
            elif key == 'нефть_пар':
                for _, row in df.iterrows():
                    if pd.isna(row['Q_топливо, кг/ч']):
                        continue
                    self.database.insert_into_experiments(
                        fuel_id=2,
                        F_fuel=row['Q_топливо, кг/ч'],
                        F_air=None,
                        F_steam=row['Q_пар, кг/ч'],
                        O2=row['O2, %'],
                        CO=row['CO, ppm'],
                        NO=row['NO, ppm'],
                        NO2=row['NO2, ppm'],
                        NOx=row['NOX, ppm'],
                        CO2=row['СО2, %'],
                        SO2=row['SO2, ppm'],
                        P_air=None,
                        P_steam=row['P_пар, атм'],
                        comments=row['Эксперимент'],
                        t_wg=row['T_wg, oC']
                    )
            elif key == 'мазут_пар' or key == 'Мазут_пар_2':
                for _, row in df.iterrows():
                    if pd.isna(row['Q_топливо, кг/ч']):
                        continue
                    self.database.insert_into_experiments(
                        fuel_id=3,
                        F_fuel=row['Q_топливо, кг/ч'],
                        F_air=None,
                        F_steam=row['Q_пар, кг/ч'],
                        O2=row['O2, %'],
                        CO=row['CO, ppm'],
                        NO=row['NO, ppm'],
                        NO2=row['NO2, ppm'],
                        NOx=row['NOX, ppm'],
                        CO2=row['СО2, %'],  # РУССКИЕ СИМВОЛЫ!
                        SO2=row['SO2, ppm'],
                        P_air=None,
                        P_steam=row['P_пар, атм'],
                        comments=row['Эксперимент'],
                        t_wg=row['T_wg, oC']
                    )
            elif key == 'мазут_воздух':
                for _, row in df.iterrows():
                    if pd.isna(row['Q_топливо, кг/ч']):
                        continue
                    self.database.insert_into_experiments(
                        fuel_id=3,
                        F_fuel=row['Q_топливо, кг/ч'],
                        F_air=row['Q_возд_рот, кг/ч'],
                        F_steam=None,
                        O2=row['O2'],
                        CO=row['CO'],
                        NO=row['NO'],
                        NO2=row['NO2'],
                        NOx=row['NOX'],
                        CO2=row['СО2'],  # РУССКИЕ СИМВОЛЫ!
                        SO2=row['SO2'],
                        P_air=None,
                        P_steam=None,
                        comments=row['Эксперимент'],
                        t_wg=row['Twg, oC']
                    )

            elif key == 'Керосин_пар':
                for _, row in df.iterrows():
                    if pd.isna(row['Fv, kg/h']):
                        continue
                    self.database.insert_into_experiments(
                        fuel_id=4,
                        F_fuel=row['Fv, kg/h'],
                        F_air=None,
                        F_steam=row['Ff, kg/h'],
                        O2=row['% O2'],
                        CO=row['ппм СO'],
                        NO=row['ппм NO'],
                        NO2=row['ппм NO2'],
                        NOx=row['ппм NOx'],
                        CO2=row['% CO2ИК'],
                        SO2=row['ппм SO2'],
                        P_air=None,
                        P_steam=row['P_rel, atm'],
                        comments=None,
                        t_wg=row['°C Тдг']
                    )
            elif key == 'Каросин_воздух':
                for _, row in df.iterrows():
                    if pd.isna(row['Fair, kg/h']):
                        continue
                    self.database.insert_into_experiments(
                        fuel_id=4,
                        F_fuel=row['Fair, kg/h'],
                        F_air=row['Ff, kg/h'],
                        F_steam=None,
                        O2=row['% O2'],
                        CO=row['ппм СO'],
                        NO=row['ппм NO'],
                        NO2=row['ппм NO2'],
                        NOx=row['ппм NOx'],
                        CO2=row['% CO2ИК'],
                        SO2=row['ппм SO2'],
                        P_air=row['P_rel, atm'],
                        P_steam=None,
                        comments=None,
                        t_wg=row['°C Тдг']
                    )
            elif key == 'Масло_пар':
                for _, row in df.iterrows():
                    if pd.isna(row['Fv, kg/h']):
                        continue
                    self.database.insert_into_experiments(
                        fuel_id=5,
                        F_fuel=row['Fv, kg/h'],
                        F_air=None,
                        F_steam=row['Ff, kg/h'],
                        O2=row['% O2'],
                        CO=row['ппм СO'],
                        NO=row['ппм NO'],
                        NO2=row['ппм NO2'],
                        NOx=row['ппм NOx'],
                        CO2=row['% CO2ИК'],
                        SO2=row['ппм SO2'],
                        P_air=None,
                        P_steam=row['P_rel, atm'],
                        comments=None,
                        t_wg=row['°C Тдг']
                    )
