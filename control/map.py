import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from control.experiment_data import ExperimentData
from control.database import DatabaseHandler
from config import (PATH_TO_SOURCE_PLOT,
                    PATH_TO_EXCEL_RESULT,
                    COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3,
                    PATH_TO_RBF_PLOT)


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
            plt.rcParams.update({'font.size': 18})

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
                PATH_TO_SOURCE_PLOT + f"/{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}.png"
            )
            plt.close()

    def save_all_source_map_to_excel(self):
        """
        Метод, который сохраняет результаты экспериментов в виде матрицы в excel.
        """
        if not os.path.exists(PATH_TO_EXCEL_RESULT):
            os.mkdir(PATH_TO_EXCEL_RESULT)
        with pd.ExcelWriter(PATH_TO_EXCEL_RESULT + "/source.xlsx") as writer:
            for experiment_parameters in self.available_variations:
                self.experiment_data.get_experiment_data(*experiment_parameters)
                fuel_axis, additive_axis, component_matrix = self.experiment_data.get_df_in_matrix()

                df_component_matrix = pd.DataFrame(component_matrix, columns=fuel_axis, index=additive_axis[::-1])

                sheet_name = f"{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}"

                self.experiment_data.df.to_excel(writer, sheet_name=sheet_name)
                df_component_matrix.to_excel(writer, sheet_name=sheet_name, startcol=6)

    def save_all_rbf_map(self):
        """
        Метод, который сохраняет аппроксимативные карты, созданные с помощью RbfInterpolator(linear), с удаленными
        отрицательными значениями и применением медианного фильтра.
        """
        # Сохранение карт в ppm
        for experiment_parameters in self.available_variations:
            break
            self.experiment_data.get_experiment_data(*experiment_parameters)
            fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()

            fig, ax = plt.subplots(figsize=(16, 9))
            plt.rcParams.update({'font.size': 18})
            ax.tick_params(axis='both', which='both', labelsize=18)

            plt.contourf(fuel_axis, additive_axis, approximated_component_surface)

            # Название графика
            if self.experiment_data.component_name == 'O2':
                plt.title(r"Rbf(linear)+med.filter+non negative: $O_2$")

            elif self.experiment_data.component_name == 'CO':
                plt.title(r"Rbf(linear)+med.filter+non negative: $CO$")

            elif self.experiment_data.component_name == 'NO':
                plt.title(r"Rbf(linear)+med.filter+non negative: $NO$")

            elif self.experiment_data.component_name == 'NO2':
                plt.title(r"Rbf(linear)+med.filter+non negative: $NO_2$")

            elif self.experiment_data.component_name == 'NOx':
                plt.title(r"Rbf(linear)+med.filter+non negative: $NO_X$")

            elif self.experiment_data.component_name == 'CO2':
                plt.title(r"Rbf(linear)+med.filter+non negative: $CO_2$")

            elif self.experiment_data.component_name == 'SO2':
                plt.title(r"Rbf(linear)+med.filter+non negative: $SO_2$")

            # Подписи осей
            if self.experiment_data.fuel_name == 'waste_oil':
                ax.set_xlabel(r"$F_{\text{waste oil}}$, kg/h")

            elif self.experiment_data.fuel_name == 'crude_oil':
                ax.set_xlabel(r"$F_{\text{crude oil}}$, kg/h")

            elif self.experiment_data.fuel_name == 'heavy_oil':
                ax.set_xlabel(r"$F_{\text{heavy oil}}$, kg/h")

            else:
                ax.set_xlabel(f"$F_{{{self.experiment_data.fuel_name}}}$, kg/h", fontsize=18)
            ax.set_ylabel(f"$F_{{{self.experiment_data.additive_name}}}$, kg/h", fontsize=18)

            # Подпись colorbar
            clb = plt.colorbar()
            if self.experiment_data.component_name in ["O2", "CO2"]:
                clb.ax.set_title(r"vol.%")
            else:
                clb.ax.set_title("ppm")

            plt.tight_layout()

            if not os.path.exists(PATH_TO_RBF_PLOT):
                os.mkdir(PATH_TO_RBF_PLOT)

            plt.savefig(
                PATH_TO_RBF_PLOT + f"/{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}.png"
            )
            plt.close()
        # Сохранение карт в mg/m3
        for experiment_parameters in self.available_variations:
            if experiment_parameters[2] in COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3:
                self.experiment_data.get_experiment_data(*experiment_parameters, convert_to_mg_m3=True)
                fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()

                fig, ax = plt.subplots(figsize=(16, 9))
                plt.rcParams.update({'font.size': 18})
                ax.tick_params(axis='both', which='both', labelsize=18)

                plt.contourf(fuel_axis, additive_axis, approximated_component_surface)

                # Название графика
                if self.experiment_data.component_name == 'CO':
                    plt.title(r"Rbf(linear)+med.filter+non negative: $CO$")

                elif self.experiment_data.component_name == 'NOx':
                    plt.title(r"Rbf(linear)+med.filter+non negative: $NO_X$")

                # Подписи осей
                if self.experiment_data.fuel_name == 'waste_oil':
                    ax.set_xlabel(r"$F_{\text{waste oil}}$, kg/h")

                elif self.experiment_data.fuel_name == 'crude_oil':
                    ax.set_xlabel(r"$F_{\text{crude oil}}$, kg/h")

                elif self.experiment_data.fuel_name == 'heavy_oil':
                    ax.set_xlabel(r"$F_{\text{heavy oil}}$, kg/h")

                else:
                    ax.set_xlabel(f"$F_{{{self.experiment_data.fuel_name}}}$, kg/h", fontsize=18)
                ax.set_ylabel(f"$F_{{{self.experiment_data.additive_name}}}$, kg/h", fontsize=18)

                # Подпись colorbar
                clb = plt.colorbar()
                clb.ax.set_title(r"$mg/m^3$")

                plt.tight_layout()

                plt.savefig(
                    PATH_TO_RBF_PLOT + f"/{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}_mg_m3.png"
                )
                plt.close()




    def save_all_rbd_map_to_excel(self):
        """
        Метод, который сохраняет аппроксимируемые поверхности РБФ в excel.
        """
        if not os.path.exists(PATH_TO_EXCEL_RESULT):
            os.mkdir(PATH_TO_EXCEL_RESULT)
        with pd.ExcelWriter(PATH_TO_EXCEL_RESULT + "/Rbf(linear)+med.filter+non_negative.xlsx") as writer:
            for experiment_parameters in self.available_variations:
                self.experiment_data.get_experiment_data(*experiment_parameters)
                fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()

                df_component_matrix = pd.DataFrame(
                    approximated_component_surface, columns=fuel_axis, index=additive_axis[::-1]
                )
                converted_df = self.experiment_data.convert_approximated_surface_to_df(
                    fuel_axis, additive_axis, approximated_component_surface
                )

                sheet_name = f"{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}"

                converted_df.to_excel(writer, sheet_name=sheet_name)
                df_component_matrix.to_excel(writer, sheet_name=sheet_name, startcol=6)
