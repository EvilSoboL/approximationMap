import pandas as pd
import numpy as np
from scipy.interpolate import RBFInterpolator
from scipy.ndimage import median_filter

from control.database import DatabaseHandler
from config import COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3, STANDARD_O2, MEASURING_COMPONENTS, ADDITIVES


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

        self.averaging_duplicate_data()

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
            df['NOx'] = ((21 - STANDARD_O2)/(21 - df['O2']))*2.05*(df['NO'] + df['NO2'])
            df.dropna(subset=['NOx'], inplace=True)  # Удаление отрицательных значений
            df.drop(['O2', 'NO', 'NO2'], axis=1, inplace=True)

            return df

    def get_all_available_variations(self) -> list[tuple]:
        """
        Метод, который возвращает все доступные комбинации топлива, добавочного компонента и компонента дымовых газов,
        по которым можно построить карты режимов (имеются экспериментальные данные).
        """
        fuel_names = [fuel[1] for fuel in self.database.get_fuel_id_and_names()]
        all_variants = [
            (fuel_name, additive, component)
            for fuel_name in fuel_names
            for additive in ADDITIVES
            for component in MEASURING_COMPONENTS
        ]
        available_variants = list()
        for variant in all_variants:
            try:
                self.get_experiment_data(*variant)
                available_variants.append(variant)
            except ValueError:
                continue
        return available_variants

    def averaging_duplicate_data(self):
        """
        Метод, который усредняет повторяющиеся значения экспериментальных данных, например:
        [[Q_fuel, Q_air, CO]
        [100, 100, 50],
        [100, 100, 48]] ->
        [[Q_fuel, Q_air, CO]
        [100, 100, 49]]
        """
        df = self.df
        df = df.groupby(["F_fuel", f"F_{self.additive_name}"])[f"{self.component_name}"].mean().reset_index()
        self.df = df

    def get_df_in_matrix(self) -> tuple[list[float], list[float], np.array]:
        """
        Метод, который df переводит в матричный вид.
        Например:
        F_fuel F_additive Component
        0 0 3
        0 1 1
        1 0 4
        1 1 2 ->
        [[1, 2], [3, 4]]
        Returns:
            tuple[list[float], list[float], np.array]: значения оси расхода топлива, добавочного компонента, и матрица
            компонентов дымовых газов.
        """
        df = self.df
        # Множество (set) для исключения из списка повторов
        fuel_set = sorted(set(list(df["F_fuel"])))
        additive_set = sorted(set(list(df[f"F_{self.additive_name}"])))

        arr = np.empty((len(additive_set), len(fuel_set)))
        arr[:] = np.nan

        # Создаем словарь для того, чтобы запомнить положение элемента расхода (F_fuel, F_air/F_steam)
        fuel_positions = dict()
        for index, element in enumerate(fuel_set):
            fuel_positions[element] = index

        additive_positions = dict()
        for index, element in enumerate(additive_set):
            additive_positions[element] = index

        for row in df.itertuples():
            fuel_value = row[1]
            add_value = row[2]
            component_value = row[3]
            # Узнаем из словаря порядок значения в списке для заполнения массива
            arr_fuel_pos = fuel_positions[fuel_value]
            arr_add_pos = additive_positions[add_value]

            arr[arr_add_pos][arr_fuel_pos] = component_value

        arr = np.flipud(arr)

        return fuel_set, additive_set, arr

    def get_rbf_data(self) -> tuple[np.array, np.array, np.array]:
        """
        Метод, который используется для получения аппроксимированной поверхности с помощью класса scipy.RbfInterpolator
        с разрешением 100 единиц, применением медианного фильтра и удалением отрицательных значений.

        Returns:
            fuel_axis_extended.ravel() - значения оси расхода топлива увеличенные на число разрешения,
            additive_axis_extended.ravel() - значения оси расхода добавочного компонента увеличенные на число разрешения,
            approximated_component_surface - аппроксимированная поверхность добавочного компонента.
        """
        df = self.df

        fuel_axis = np.array(df["F_fuel"])
        additive_axis = np.array(df[f"F_{self.additive_name}"])
        component_axis = np.array(df[f"{self.component_name}"])

        fuel_axis = fuel_axis.reshape(len(fuel_axis), 1)
        additive_axis = additive_axis.reshape(len(additive_axis), 1)

        fuel_additive_axis = np.concatenate((fuel_axis, additive_axis), axis=1)

        rbfi = RBFInterpolator(fuel_additive_axis, component_axis, kernel='linear')

        min_max_dict = self.get_minimum_and_maximum_consumption()

        fuel_step = (min_max_dict['F_fuel'][1] - min_max_dict['F_fuel'][0]) / 100
        additive_step = (min_max_dict['F_additive'][1] - min_max_dict['F_additive'][0]) / 100

        fuel_axis_extended = np.arange(min_max_dict['F_fuel'][0], min_max_dict['F_fuel'][1], fuel_step)
        additive_axis_extended = np.arange(min_max_dict['F_additive'][0], min_max_dict['F_additive'][1], additive_step)

        fuel_grid, additive_grid = np.meshgrid(fuel_axis_extended, additive_axis_extended)

        fuel_additive_grid = np.stack([fuel_grid.ravel(), additive_grid.ravel()], -1)

        approximated_component_surface = rbfi(fuel_additive_grid).reshape(fuel_grid.shape)

        # Переворачиваем массив с ног на голову
        approximated_component_surface = np.flipud(approximated_component_surface)
        additive_axis_extended = additive_axis_extended.ravel()[::-1]  # Переворачиваем ось y с ног на голову

        # Удаление отрицательных значений из интерполяционной поверхности
        approximated_component_surface[approximated_component_surface < 0] = 0

        # Применение медианного фильтра
        approximated_component_surface = median_filter(approximated_component_surface, size=20)

        return fuel_axis_extended.ravel(), additive_axis_extended.ravel(), approximated_component_surface

    def convert_approximated_surface_to_df(
            self,
            fuel_axis: np.array,
            additive_axis: np.array,
            approximated_surface: np.array
    ) -> pd.DataFrame:
        """
        Метод, который на вход принимает интерполяционную поверхность и возвращает её в виде таблицы со
        значениями Q_fuel, Q_additive, component

        Args:
            fuel_axis - значения оси расхода топлива,
            additive_axis - значения оси расхода добавочного компонента,
            approximated_surface - аппроксимированная поверхность добавочного компонента.
        """
        approximated_surface_flat = approximated_surface.flatten()  # Плоское представление матрицы z_interp

        fuel_axis_flat = list()
        additive_axis_flat = list()
        approximated_surface_flat = list(approximated_surface_flat)

        for additive_value in additive_axis:
            for fuel_value in fuel_axis:
                fuel_axis_flat.append(fuel_value), additive_axis_flat.append(additive_value)

        converted_df = pd.DataFrame(
            {"F_fuel": fuel_axis_flat,
             f"F_{self.additive_name}": additive_axis_flat,
             f"{self.component_name}": approximated_surface_flat})

        return converted_df

    def get_minimum_and_maximum_consumption(self) -> dict:
        """
        Метод, который возвращает словарь минимальных и максимальных значений для расхода топлива и добавочных компонентов.
        """
        min_max_dict = self.database.get_minimum_and_maximum_consumption()
        f_air_values = min_max_dict['F_air']
        f_steam_values = min_max_dict['F_steam']

        min_additive_value = min(f_air_values[0], f_steam_values[0])
        max_additive_value = max(f_air_values[1], f_steam_values[1])

        min_max_dict['F_additive'] = (min_additive_value, max_additive_value)

        min_max_dict.pop('F_air')
        min_max_dict.pop('F_steam')

        return min_max_dict
