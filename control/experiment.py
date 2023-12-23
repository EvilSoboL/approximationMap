from control.database import DatabaseHandler


class ExperimentData:
    def __init__(self):
        self.fuel_name = None
        self.fuel_id = None
        self.additive_name = None
        self.component_name = None
        self.df = None

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
