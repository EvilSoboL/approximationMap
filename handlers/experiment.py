from handlers.database import DatabaseHandler


class ExperimentData:
    def __init__(self):
        self.fuel_name = None

        self.database = DatabaseHandler()

    def experiments_info(self):
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



