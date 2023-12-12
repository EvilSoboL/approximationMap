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
            fuel_id,
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
            t_wg
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

db = DatabaseHandler()
db.insert_into_experiments(
    1,
    100,
    100,
    20,
    None,
    20,
    20,
    20,
    20,
    20,
    20,
    20,
    20,
    't'
)
