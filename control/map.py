

from control.experiment_data import ExperimentData
from control.database import DatabaseHandler


class Map:
    def __init__(self):
        self.experiment_data = ExperimentData()
        self.database = DatabaseHandler()
        self.available_variations = self.experiment_data.get_all_available_variations()

    def save_all_source_map(self):
        """
        Метод, который сохраняет результаты экспериментов в виде матрицы.
        """
        for experiment_parameters in self.available_variations:
            self.experiment_data.get_experiment_data(*experiment_parameters)
            pass
