import pandas as pd
import os

from control.experiment_data import ExperimentData
from control.database import DatabaseHandler
from config import DATA_RES_DIR


class ApproximatedMapUploader:
    """Класс, необходимый для получения данных с аппроксимированных карт"""
    def __init__(self):
        self.experiment_data = ExperimentData()

    def get_approximated_surfaces(self) -> dict[str: pd.DataFrame]:
        fuel_variations = self.experiment_data.get_all_available_variations()
        surfaces_dict = dict()
        for experiment_parameters in fuel_variations:
            fuel_name, additive_name, component = experiment_parameters
            self.experiment_data.get_experiment_data(fuel_name, additive_name, component)
            approx_df = self.experiment_data.get_approx_surface_in_tableview()
            key = f'{fuel_name}_{additive_name}'
            if key not in surfaces_dict:
                surfaces_dict[key] = approx_df
            else:
                surfaces_dict[key] = pd.merge(surfaces_dict[key], approx_df, on=['F_fuel', f'F_{additive_name}'])
        return surfaces_dict

    def save_to_csv(self):
        surfaces_dict = self.get_approximated_surfaces()
        for key, value in surfaces_dict.items():
            path_to_save = os.path.join(DATA_RES_DIR, f'{key}.csv')
            value.to_csv(path_to_save, index=False)


class FlameHeightUploader:
    """Класс для получения csv файла со значениями высот пламени"""
    def __init__(self):
        self.database = DatabaseHandler()

    def save_to_csv(self, path_to_save: str) -> None:
        df = self.database.get_flame_height_data()
        df.to_csv(path_to_save, index=False)


class GetExperimentData:
    """Класс для получения csv файла со результатами экспериментальных данных"""
    def __init__(self):
        self.database = DatabaseHandler()

    def save_experiment_data_to_csv(self, path_to_save: str, fuel_type: int, additive_type: str) -> None:
        df = self.database.get_gas_analysis(fuel_type, additive_type)
        df.to_csv(path_to_save, index=False)
