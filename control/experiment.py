import pandas as pd

from control.database import DatabaseHandler
from config import COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3, STANDARD_O2


class ExperimentData:
    def __init__(self):
        self.fuel_name = None
        self.fuel_id = None
        self.additive_name = None
        self.component_name = None
        self.df = None
        self.component_to_convert = COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3

        self.database = DatabaseHandler()

    def experiments_info(self) -> None:
        """
        Метод, который возвращает информацию о том, результаты каких экспериментов есть в базе данных.
        """
        unique_fuels = self.database.get_unique_fuels_in_experiments()
        print(f'Количество уникальных топлив в базе данных: {unique_fuels}')
        print('---')
        fuels_list = self.database.get_fuel_id_and_names()
        for fuel_info in fuels_list:
            fuel_id, fuel_name = fuel_info
            print(f'Количество экспериментов для {fuel_name}')
            experiments = self.database.get_experiment_number(fuel_id)
            print(f'По воздуху: {experiments[0]}, по пару: {experiments[1]}')
            print('---')

    def get_experiment_data(self, fuel_name: str, additive_name: str, component_name: str) -> None:
        """
        Метод, который присваивает атрибутам класса значения, указанные в параметрах атрибута и находит df со значениями
        экспериментов, если в базе данных нет проведенных экспериментов с данными параметрами вызывает Warning.

        Args:
            fuel_name: наименование топлива: diesel, crude_oil, heavy_oil, kerosene, waste_oil.
            additive_name: наименование добовочного компонента: air, steam.
            component_name: наименование компонета дымовых газов: O2, CO, NO и тд.
        """
        self.fuel_name = fuel_name
        fuel_id = self.database.get_fuel_id_from_name(fuel_name)
        self.fuel_id = fuel_id
        self.additive_name = additive_name
        self.component_name = component_name
        self.df = self.database.get_experiment_data(fuel_name, additive_name, component_name)

        if component_name in COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3:
            self.df = self.conversion_from_ppm_to_mg_m3(self.df)

    def conversion_from_ppm_to_mg_m3(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Метод, который переводит компоненты CO и NOx из ppm в мг/м3 по формуле:
            CO(мг/м3) = ((21 - эталон.О2)/(21 - О2))*CO(ppm)*1.25
            NOx(мг/м3) = ((21 - эталон.О2)/(21 - О2))*2.05*(NO(ppm) + NO2(ppm))
        """
        if 'CO' in list(self.df.columns):
            df['CO'] = ((21 - STANDARD_O2)/(21 - df['O2']))*df['CO']*1.25
            # Замена NaN значений кислорода на 750 мг/м3
            df.loc[df['O2'].isna(), 'CO'] = 750
            df.drop('O2', axis=1, inplace=True)

            return df
        else:
            # TODO Что делать с NaN значениями?
            df['NOx'] = ((21 - STANDARD_O2)/(21 - df['O2']))*2.05*(df['NO'] + df['NO2'])
            df.drop(['O2', 'NO', 'NO2'], axis=1, inplace=True)

            return df
