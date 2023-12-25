import os
import matplotlib.pyplot as plt
import numpy as np

from control.experiment_data import ExperimentData
from control.database import DatabaseHandler
from config import PATH_TO_SOURCE_PLOT


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
            fuel_axis, additive_axis, component_matrix = self.experiment_data.get_df_in_matrix()
            fuel_axis_str = [str(np.round(value, decimals=2)) for value in fuel_axis]
            additive_axis_str = [str(np.round(value, decimals=2)) for value in additive_axis[::-1]]

            fig, ax = plt.subplots(figsize=(16, 9))

            ax.matshow(component_matrix)

            # Название графика
            if self.experiment_data.component_name == 'O2':
                plt.title(r"Source: $O_2$, vol.%")

            elif self.experiment_data.component_name == 'CO':
                plt.title(r"Source: $CO, mg/m^3$")

            elif self.experiment_data.component_name == 'NO':
                plt.title(r"Source: $NO$, ppm")

            elif self.experiment_data.component_name == 'NO2':
                plt.title(r"Source: $NO_2$, ppm")

            elif self.experiment_data.component_name == 'NOx':
                plt.title(r"Source: $NO_X, mg/m^3$")

            elif self.experiment_data.component_name == 'CO2':
                plt.title(r"Source: $CO_2$, ppm")

            elif self.experiment_data.component_name == 'SO2':
                plt.title(r"Source: $SO_2$, ppm")

            # Подписи осей
            plt.xticks(range(len(fuel_axis)), fuel_axis_str)
            plt.yticks(range(len(additive_axis)), additive_axis_str)
            ax.tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)

            if self.experiment_data.fuel_name == 'waste_oil':
                ax.set_xlabel(r"$F_{\text{waste oil}}$, kg/h")

            elif self.experiment_data.fuel_name == 'crude_oil':
                ax.set_xlabel(r"$F_{\text{crude oil}}$, kg/h")

            elif self.experiment_data.fuel_name == 'heavy_oil':
                ax.set_xlabel(r"$F_{\text{heavy oil}}$, kg/h")

            else:
                ax.set_xlabel(f"$F_{{{self.experiment_data.fuel_name}}}$, kg/h")
            ax.set_ylabel(f"$F_{{{self.experiment_data.additive_name}}}$, kg/h")

            # Нанесение подписей на ячейки матрицы
            for row in range(len(additive_axis)):
                for column in range(len(fuel_axis)):
                    value = component_matrix[row, column]
                    plt.text(column, row, str(np.round(value, decimals=2)), va='center', ha='center')

            plt.tight_layout()

            if not os.path.exists(PATH_TO_SOURCE_PLOT):
                os.mkdir(PATH_TO_SOURCE_PLOT)
            plt.savefig(
                PATH_TO_SOURCE_PLOT + f'/{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}.png'
            )
            plt.close()


