import sqlite3

from config import PATH_TO_DB


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
