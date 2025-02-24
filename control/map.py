import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from control.experiment_data import ExperimentData
from control.database import DatabaseHandler
from config import (PATH_TO_SOURCE_PLOT,
                    PATH_TO_EXCEL_RESULT,
                    COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3,
                    PATH_TO_RBF_PLOT,
                    PATH_TO_CO_MIN_PLOT,
                    PATH_TO_O2_MIN_PLOT,
                    PROCENT_COMPONENT)
from control.utils import get_min_indexes_in_approximated_surface, linear_function
from control.plot_config import save_source_plot, save_rbf_plot
import control.plot_config as plot_config


class Map:
    def __init__(self):
        self.experiment_data = ExperimentData()
        self.database = DatabaseHandler()
        self.available_variations = self.experiment_data.get_all_available_variations()

    def save_all_source_map(self, russian: bool = False) -> None:
        """
        Метод, который сохраняет результаты экспериментов в виде матрицы.
        """
        # Сохранение карт в ppm
        for experiment_parameters in self.available_variations:
            self.experiment_data.get_experiment_data(*experiment_parameters)
            fuel_axis, additive_axis, component_matrix = self.experiment_data.get_df_in_matrix()
            save_source_plot(
                self.experiment_data.fuel_name,
                self.experiment_data.additive_name,
                self.experiment_data.component_name,
                fuel_axis,
                additive_axis,
                component_matrix,
                ppm=True,
                russian=russian
            )

        for experiment_parameters in self.available_variations:
            if experiment_parameters[2] in COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3:
                self.experiment_data.get_experiment_data(*experiment_parameters, convert_to_mg_m3=True)
                fuel_axis, additive_axis, component_matrix = self.experiment_data.get_df_in_matrix()
                save_source_plot(
                    self.experiment_data.fuel_name,
                    self.experiment_data.additive_name,
                    self.experiment_data.component_name,
                    fuel_axis,
                    additive_axis,
                    component_matrix,
                    ppm=False
                )

    def save_all_source_map_to_excel(self) -> None:
        """
        Метод, который сохраняет результаты экспериментов в виде матрицы в excel.
        """
        if not os.path.exists(PATH_TO_EXCEL_RESULT):
            os.mkdir(PATH_TO_EXCEL_RESULT)
        with pd.ExcelWriter(PATH_TO_EXCEL_RESULT + "/source.xlsx") as writer:
            # Сохранение карт в ppm
            for experiment_parameters in self.available_variations:
                self.experiment_data.get_experiment_data(*experiment_parameters)
                fuel_axis, additive_axis, component_matrix = self.experiment_data.get_df_in_matrix()

                df_component_matrix = pd.DataFrame(component_matrix, columns=fuel_axis, index=additive_axis[::-1])

                sheet_name = f"{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}"

                self.experiment_data.df.to_excel(writer, sheet_name=sheet_name)
                df_component_matrix.to_excel(writer, sheet_name=sheet_name, startcol=6)

            # Сохранение карт в мг/м3
            for experiment_parameters in self.available_variations:
                if experiment_parameters[2] in COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3:
                    self.experiment_data.get_experiment_data(*experiment_parameters, convert_to_mg_m3=True)
                    fuel_axis, additive_axis, component_matrix = self.experiment_data.get_df_in_matrix()

                    df_component_matrix = pd.DataFrame(component_matrix, columns=fuel_axis, index=additive_axis)

                    sheet_name = f"{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}_mg_m3"

                    self.experiment_data.df.to_excel(writer, sheet_name=sheet_name)
                    df_component_matrix.to_excel(writer, sheet_name=sheet_name, startcol=6)

    def save_all_rbf_map(self, russian: bool = False) -> None:
        """
        Метод, который сохраняет аппроксимативные карты, созданные с помощью RbfInterpolator(linear), с удаленными
        отрицательными значениями и применением медианного фильтра.
        """
        # Сохранение карт в ppm
        for experiment_parameters in self.available_variations:
            self.experiment_data.get_experiment_data(*experiment_parameters)
            fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()
            save_rbf_plot(
                self.experiment_data.fuel_name,
                self.experiment_data.additive_name,
                self.experiment_data.component_name,
                fuel_axis,
                additive_axis,
                approximated_component_surface,
                ppm=True,
                russian=russian
            )

        # Сохранение карт в мг/м3
        for experiment_parameters in self.available_variations:
            if experiment_parameters[2] in COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3:
                self.experiment_data.get_experiment_data(*experiment_parameters, convert_to_mg_m3=True)
                fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data(med_filter=False, non_zero=False)
                save_rbf_plot(
                    self.experiment_data.fuel_name,
                    self.experiment_data.additive_name,
                    self.experiment_data.component_name,
                    fuel_axis,
                    additive_axis,
                    approximated_component_surface,
                    ppm=False,
                    russian=russian
                )

    def save_all_rbf_map_to_excel(self) -> None:
        """
        Метод, который сохраняет аппроксимируемые поверхности РБФ в excel.
        """
        if not os.path.exists(PATH_TO_EXCEL_RESULT):
            os.mkdir(PATH_TO_EXCEL_RESULT)
        with pd.ExcelWriter(PATH_TO_EXCEL_RESULT + "/Rbf(linear)+med.filter+non_negative.xlsx") as writer:
            # Сохранение карт в ppm
            for experiment_parameters in self.available_variations:
                self.experiment_data.get_experiment_data(*experiment_parameters)
                fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()

                df_component_matrix = pd.DataFrame(
                    approximated_component_surface, columns=fuel_axis, index=additive_axis
                )
                converted_df = self.experiment_data.convert_approximated_surface_to_df(
                    fuel_axis, additive_axis, approximated_component_surface
                )

                sheet_name = f"{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}"

                converted_df.to_excel(writer, sheet_name=sheet_name)
                df_component_matrix.to_excel(writer, sheet_name=sheet_name, startcol=6)

            # Сохранение карт в мг/м3
            for experiment_parameters in self.available_variations:
                if experiment_parameters[2] in COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3:
                    self.experiment_data.get_experiment_data(*experiment_parameters, convert_to_mg_m3=True)
                    fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()

                    df_component_matrix = pd.DataFrame(
                        approximated_component_surface, columns=fuel_axis, index=additive_axis
                    )
                    converted_df = self.experiment_data.convert_approximated_surface_to_df(
                        fuel_axis, additive_axis, approximated_component_surface
                    )

                    sheet_name = f"{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}_mg_m3"

                    converted_df.to_excel(writer, sheet_name=sheet_name)
                    df_component_matrix.to_excel(writer, sheet_name=sheet_name, startcol=6)

    def save_all_co_min_map(self) -> None:
        """
        Метод, который сохраняет карты с нанесенной аппроксимированной линией минимальных значений на топливной карте.
        """
        # Сохранение карт в ppm
        for experiment_parameters in self.available_variations:
            if experiment_parameters[2] == 'CO':
                self.experiment_data.get_experiment_data(*experiment_parameters)
                fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()

                save_rbf_plot(
                    self.experiment_data.fuel_name,
                    self.experiment_data.additive_name,
                    self.experiment_data.component_name,
                    fuel_axis,
                    additive_axis,
                    approximated_component_surface,
                    ppm=True,
                    save=False
                )

                fuel_min_indexes, additive_min_indexes = get_min_indexes_in_approximated_surface(
                    fuel_axis, additive_axis, approximated_component_surface
                )
                params, covariance = curve_fit(linear_function, fuel_min_indexes, additive_min_indexes)

                a_val, b_val = params  # Коэффициенты аппроксимированного линейного уравнения
                additive_approx = linear_function(np.array(fuel_axis), a_val, b_val)
                plt.plot(
                    fuel_axis, additive_approx, color="black", linestyle='dashed', linewidth=4,
                    label='Аппроксимированная линия минимальных значений CO'
                )

                # Обрезаем часть графика, чтобы линия интерполяции не выходила за пределы интерполяционной поверхнсоти
                plt.ylim(min(additive_min_indexes), max(additive_min_indexes))

                plt.legend()

                if not os.path.exists(PATH_TO_CO_MIN_PLOT):
                    os.mkdir(PATH_TO_CO_MIN_PLOT)

                plt.savefig(
                    PATH_TO_CO_MIN_PLOT + f'/{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}.png'
                )
                plt.close()
        # Сохранение карт в мг/м3
        for experiment_parameters in self.available_variations:
            if experiment_parameters[2] == 'CO':
                self.experiment_data.get_experiment_data(*experiment_parameters, convert_to_mg_m3=True)
                fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()
                save_rbf_plot(
                    self.experiment_data.fuel_name,
                    self.experiment_data.additive_name,
                    self.experiment_data.component_name,
                    fuel_axis,
                    additive_axis,
                    approximated_component_surface,
                    ppm=False,
                    save=False
                )

                fuel_min_indexes, additive_min_indexes = get_min_indexes_in_approximated_surface(
                    fuel_axis, additive_axis, approximated_component_surface
                )
                params, covariance = curve_fit(linear_function, fuel_min_indexes, additive_min_indexes)

                a_val, b_val = params  # Коэффициенты аппроксимированного линейного уравнения
                additive_approx = linear_function(np.array(fuel_axis), a_val, b_val)
                plt.plot(
                    fuel_axis, additive_approx, color="black", linestyle='dashed', linewidth=4, label='Аппроксимированная линия минимальных значений CO'
                )

                # Обрезаем часть графика, чтобы линия интерполяции не выходила за пределы интерполяционной поверхности
                plt.ylim(min(additive_min_indexes), max(additive_min_indexes))

                plt.legend()

                if not os.path.exists(PATH_TO_CO_MIN_PLOT):
                    os.mkdir(PATH_TO_CO_MIN_PLOT)

                plt.savefig(
                    PATH_TO_CO_MIN_PLOT + f'/{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}_mg_m3.png'
                )
                plt.close()

    def save_all_o2_min_map(self) -> None:
        """
        Метод получает изображение, полученное с функцией countorf, которое представляет набор уровней, и предпоследний
        уровень аппроксимирует и получает уравнение прямой.
        """
        for experiment_parameters in self.available_variations:
            if experiment_parameters[2] == 'O2':
                self.experiment_data.get_experiment_data(*experiment_parameters)
                fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data()

                save_rbf_plot(
                    self.experiment_data.fuel_name,
                    self.experiment_data.additive_name,
                    self.experiment_data.component_name,
                    fuel_axis,
                    additive_axis,
                    approximated_component_surface,
                    ppm=True,
                    save=False
                )
                # Получаем уравнения контуров
                levels = np.arange(0, approximated_component_surface.max() + 1.5, 1.5)
                contours = plt.contour(fuel_axis, additive_axis, approximated_component_surface, colors='none', levels=levels)
                selected_contour = contours.collections[2]  # Выбираем нужный контур (предпоследний)
                # Получаем координаты точек на контуре
                path = selected_contour.get_paths()[0]
                points = path.vertices
                contour_x, contour_y = points[:, 0], points[:, 1]

                params, covariance = curve_fit(linear_function, contour_x, contour_y)
                a_val, b_val = params  # Коэффициенты аппроксимированного линейного уравнения
                additive_approx = linear_function(np.array(fuel_axis), a_val, b_val)
                plt.plot(
                    fuel_axis, additive_approx, color="black", linestyle='dashed', linewidth=4, label=r'Аппроксимированная линия эталонного содержания $0_2$'
                )
                # Обрезаем часть графика, чтобы линия интерполяции не выходила за пределы интерполяционной поверхности
                plt.ylim(min(additive_axis), max(additive_axis))

                plt.legend()

                if not os.path.exists(PATH_TO_O2_MIN_PLOT):
                    os.mkdir(PATH_TO_O2_MIN_PLOT)
                plt.savefig(
                    PATH_TO_O2_MIN_PLOT + f"/{self.experiment_data.fuel_name}_{self.experiment_data.additive_name}_{self.experiment_data.component_name}.png"
                )

    def show_3d_plot(self,
                     fuel_name: str,
                     additive_name: str,
                     component_name: str,
                     russian: bool = False) -> None:
        self.experiment_data.get_experiment_data(fuel_name, additive_name, component_name, convert_to_mg_m3=False)

        x = list(self.experiment_data.df["F_fuel"])
        y = list(self.experiment_data.df[f"F_{additive_name}"])
        z = list(self.experiment_data.df[f"{component_name}"])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        approx_x, approx_y, approx_z = self.experiment_data.get_rbf_data(med_filter=False, non_zero=False)
        x_grid, y_grid = np.meshgrid(approx_x, approx_y)

        ax.plot_surface(x_grid, y_grid, approx_z, rstride=1, cstride=1, cmap='viridis', alpha=0.8)
        plt.title(f'{fuel_name}')
        if russian:
            plt.title(f'{plot_config.title_on_russian(fuel_name)}')

            ax.scatter(x, y, z, c='r', marker='o', label='Экспериментальные данные')
            ax.set_xlabel('Расход топлива, кг/ч')

            if additive_name == 'air':
                ax.set_ylabel(f'Расход воздуха, кг/ч')

            else:
                ax.set_ylabel(f'Расход пара, кг/ч')
        else:
            plt.title(f'{fuel_name}')

            ax.scatter(x, y, z, c='r', marker='o', label='Experimental data')
            ax.set_xlabel('Fuel consumption, kg/h')

            if additive_name == 'air':
                ax.set_ylabel(f'Air consumption, kg/h')

            else:
                ax.set_ylabel(f'Steam consumption, kg/h')

        ax.set_zlabel(f'{component_name}, ppm')
        plt.legend()

        plt.show()

    def show_map_without_postprocessing(self,
                                        fuel_name: str,
                                        additive_name: str,
                                        component_name: str,
                                        russian: bool = False) -> None:
        self.experiment_data.get_experiment_data(fuel_name, additive_name, component_name, convert_to_mg_m3=False)
        fuel_axis, additive_axis, approximated_component_surface = self.experiment_data.get_rbf_data(med_filter=False,
                                                                                                     non_zero=False)
        fig, ax = plt.subplots()

        plt.contourf(fuel_axis, additive_axis, approximated_component_surface)

        title = f'{fuel_name}, {component_name}'

        if russian:
            plt.title(plot_config.title_on_russian(title))
            if component_name == "air":
                ax.set_ylabel('Расход воздуха, кг/ч')
            else:
                ax.set_ylabel('Расход пара, кг/ч')

            ax.set_xlabel('Расход топлива, кг/ч')
        else:
            plt.title(title)
            if component_name == "air":
                ax.set_ylabel('Air consumption, kg/h')
            else:
                ax.set_ylabel('Steam consumption, kg/h')

            ax.set_xlabel('Fuel consumption, kg/h')

        clb = plt.colorbar()

        if component_name in PROCENT_COMPONENT:
            clb.ax.set_title(r"vol.%")
        else:
            clb.ax.set_title("ppm")

        plt.tight_layout()
        plt.show()
