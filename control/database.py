import sqlite3
import pandas as pd

from config import PATH_TO_DB, COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3


class DatabaseHandler:
    def __init__(self):
        self.path_to_db = PATH_TO_DB
        self.connection = None
        self.cursor = None

        self.connect_to_db()

    def connect_to_db(self):
        self.connection = sqlite3.connect(self.path_to_db)
        self.cursor = self.connection.cursor()

    def insert_into_experiments(
            self,
            fuel_id: int,
            F_fuel: float,
            F_air: float or None,
            F_steam: float or None,
            O2: float or None,
            CO: float or None,
            NO: float or None,
            NO2: float or None,
            NOx: float or None,
            CO2: float or None,
            SO2: float or None,
            P_air: float or None,
            P_steam: float or None,
            comments: str or None,
            t_wg: float or None
    ):
        with self.connection:
            self.cursor.execute(
                '''
                INSERT INTO "main"."experiments"
                (fuel_id,
                F_fuel,
                F_air,
                F_steam,
                O2,
                CO,
                NO,
                NO2,
                NOx,
                CO2,
                SO2,
                P_air,
                P_steam,
                comments,
                t_wg)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (fuel_id,
                 F_fuel,
                 F_air,
                 F_steam,
                 O2,
                 CO,
                 NO,
                 NO2,
                 NOx,
                 CO2,
                 SO2,
                 P_air,
                 P_steam,
                 comments,
                 t_wg)
            )

    def get_unique_fuels_in_experiments(self) -> int:
        """
        Метод, который возвращает количество уникальных fuel_id в таблице experiment.
        """
        with self.connection:
            self.cursor.execute(
                """
                SELECT COUNT(DISTINCT fuel_id) AS unique_fuels_count FROM "main"."experiments"
                """
            )
            result = self.cursor.fetchone()[0]
        return result

    def get_experiment_number(self, fuel_id: int) -> tuple[int, int]:
        """
        Метод, который возвращает для выбранного топлива количество экспериментов по воздуху и пару.

        Returns:
            tuple[int, int]: первое значения для количества экспериментов по воздуху, второе по пару.
        """
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT COUNT(F_air) AS count_F_air, COUNT(F_steam) AS count_F_steam
                FROM "main"."experiments"
                WHERE fuel_id = {fuel_id}
                """
            )
            result = self.cursor.fetchone()
        return result

    def get_fuel_id_and_names(self) -> list[tuple]:
        """
        Метод, который возвращает список из кортежей, где первое значение id топлива, второе - его наименование.
        """
        with self.connection:
            self.cursor.execute(
                """
                SELECT fuel_id, fuel_name
                FROM "main"."fuels"
                ORDER BY fuel_id;
                """
            )
            result = self.cursor.fetchall()
        return result

    def get_fuel_id_from_name(self, fuel_name: str) -> int:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT fuel_id
                FROM "main"."fuels"
                WHERE fuel_name = '{fuel_name}'
                """
            )
            result = self.cursor.fetchone()[0]
        return result

    def get_experiment_data(self, fuel_name: str, additive_name: str, component_name: str) -> pd.DataFrame:
        """
        Метод, который по значению параметров возвращает экспериментальные данные из базы данных.

        Args:
            fuel_name: наименование топлива: diesel, crude_oil, heavy_oil, kerosene, waste_oil.
            additive_name: наименование добовочного компонента: air, steam.
            component_name: наименование компонета дымовых газов: O2, CO, NO и тд.
        """
        fuel_id = self.get_fuel_id_from_name(fuel_name)
        if component_name == 'CO':
            query = (
                f"""
                SELECT F_fuel, F_{additive_name}, {component_name}, O2
                FROM "main"."experiments"
                WHERE fuel_id = {fuel_id} AND F_{additive_name} IS NOT NULL AND {component_name} IS NOT NULL
                """
            )
        elif component_name == 'NOx':
            query = (
                f"""
                SELECT F_fuel, F_{additive_name}, {component_name}, O2, NO, NO2
                FROM "main"."experiments"
                WHERE fuel_id = {fuel_id} AND F_{additive_name} IS NOT NULL AND {component_name} IS NOT NULL
                """
            )
        else:
            query = (
                f"""
                SELECT F_fuel, F_{additive_name}, {component_name}
                FROM "main"."experiments"
                WHERE fuel_id = {fuel_id} AND F_{additive_name} IS NOT NULL AND {component_name} IS NOT NULL
                """
            )
        df = pd.read_sql(query, self.connection)
        if df.empty:
            raise ValueError(
                f"Не найдено экспериментальных со следующими параметрами: {fuel_name}, {additive_name}, {component_name}"
            )

        return df

    def get_minimum_and_maximum_consumption(self) -> dict:
        """
        Метод, который возвращает словарь с минимальными и максимальными значениями расхода топлива, добавочного воздуха
        и добавочного пара.
        """
        with self.connection:
            self.cursor.execute(
                """
                SELECT MIN(F_fuel) AS min_fuel, MAX(F_fuel) AS max_fuel,
                       MIN(F_air) AS min_air, MAX(F_air) AS max_air,
                       MIN(F_steam) AS min_steam, MAX(F_steam) AS max_steam
            FROM "main"."experiments"
            """
            )
            result = self.cursor.fetchone()
            result_dict = {
                'F_fuel': (result[0], result[1]),
                'F_air': (result[2], result[3]),
                'F_steam': (result[4], result[5])
            }
        return result_dict
