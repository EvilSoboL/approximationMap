import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

from config import PATH_TO_SOURCE_PLOT, PATH_TO_RBF_PLOT, PROCENT_COMPONENT


def save_source_plot(
         fuel_name: str,
        additive_name: str,
        component_name: str,
        fuel_consumptions: list,
        additive_consumptions: list,
        component_matrix: np.ndarray,
        ppm: bool = True,
        russian: bool = False):

    fig, ax = plt.subplots(figsize=(16, 9))
    plt.rcParams.update({'font.size': 18})

    sns.heatmap(component_matrix, linewidths=1.5, annot=True, fmt='.0f', ax=ax, cbar=True, cbar_kws={'label': 'ppm'})

    # Название графика
    if component_name in PROCENT_COMPONENT:
        plt.title(f'{component_name}, vol. %')
    else:
        plt.title(f'{component_name}, ppm')

    # Подпись расхода топлива и вводимого кмопонента
    fuel_axis = [np.round(fuel_consumption, decimals=2) for fuel_consumption in fuel_consumptions]
    additive_axis = [np.round(additive_consumption, decimals=2) for additive_consumption in reversed(additive_consumptions)]

    plt.xticks(range(len(fuel_axis)), fuel_axis)
    plt.yticks(range(len(additive_axis)), additive_axis)

    if fuel_name == 'waste_oil':
        ax.set_xlabel(r"$F_{\text{waste oil}}$, kg/h")

    elif fuel_name == 'crude_oil':
        ax.set_xlabel(r"$F_{\text{crude oil}}$, kg/h")

    elif fuel_name == 'heavy_oil':
        ax.set_xlabel(r"$F_{\text{heavy oil}}$, kg/h")

    else:
        ax.set_xlabel('fuel consumption, kg/h')
    ax.set_ylabel('additive consumption, kg/h')

    plt.tight_layout()

    if not os.path.exists(PATH_TO_SOURCE_PLOT):
        os.mkdir(PATH_TO_SOURCE_PLOT)
    if ppm:
        plt.savefig(
            PATH_TO_SOURCE_PLOT + f"/{fuel_name}_{additive_name}_{component_name}.png"
        )
    else:
        plt.savefig(
            PATH_TO_SOURCE_PLOT + f"/{fuel_name}_{additive_name}_{component_name}_mg_m3.png"
        )
    plt.close()


def save_rbf_plot(fuel_name,
                  additive_name,
                  component_name,
                  fuel_axis,
                  additive_axis,
                  approximated_component_surface,
                  ppm=True,
                  save=True):
    fig, ax = plt.subplots(figsize=(16, 9))
    plt.rcParams.update({'font.size': 18})
    ax.tick_params(axis='both', which='both', labelsize=18)
    if component_name == 'O2':
        levels = np.arange(0, approximated_component_surface.max() + 1.5, 1.5)
        plt.contourf(fuel_axis, additive_axis, approximated_component_surface, levels=levels, vmin=0)
    else:
        plt.contourf(fuel_axis, additive_axis, approximated_component_surface)

    # Название графика
    if component_name == 'CO':
        plt.title(r"Rbf(linear)+med.filter+non negative: $CO$")

    elif component_name == 'NOx':
        plt.title(r"Rbf(linear)+med.filter+non negative: $NO_X$")

    elif component_name == 'O2':
        plt.title(r"Rbf(linear)+med.filter+non negative: $O_2$")

    elif component_name == 'CO':
        plt.title(r"Rbf(linear)+med.filter+non negative: $CO$")

    elif component_name == 'NO':
        plt.title(r"Rbf(linear)+med.filter+non negative: $NO$")

    elif component_name == 'NO2':
        plt.title(r"Rbf(linear)+med.filter+non negative: $NO_2$")

    elif component_name == 'NOx':
        plt.title(r"Rbf(linear)+med.filter+non negative: $NO_X$")

    elif component_name == 'CO2':
        plt.title(r"Rbf(linear)+med.filter+non negative: $CO_2$")

    elif component_name == 'SO2':
        plt.title(r"Rbf(linear)+med.filter+non negative: $SO_2$")

    # Подписи осей
    if fuel_name == 'waste_oil':
        ax.set_xlabel(r"$F_{\text{waste oil}}$, kg/h")

    elif fuel_name == 'crude_oil':
        ax.set_xlabel(r"$F_{\text{crude oil}}$, kg/h")

    elif fuel_name == 'heavy_oil':
        ax.set_xlabel(r"$F_{\text{heavy oil}}$, kg/h")

    else:
        ax.set_xlabel(f"$F_{{{fuel_name}}}$, kg/h", fontsize=18)
    ax.set_ylabel(f"$F_{{{additive_name}}}$, kg/h", fontsize=18)

    # Подпись colorbar
    clb = plt.colorbar()
    if ppm:
        if component_name in ["O2", "CO2"]:
            clb.ax.set_title(r"vol.%")
        else:
            clb.ax.set_title("ppm")
    else:
        clb.ax.set_title(r"$mg/m^3$")

    plt.tight_layout()

    if save:
        if not os.path.exists(PATH_TO_RBF_PLOT):
            os.mkdir(PATH_TO_RBF_PLOT)
        if ppm:
            plt.savefig(
                PATH_TO_RBF_PLOT + f"/{fuel_name}_{additive_name}_{component_name}.png"
            )
        else:
            plt.savefig(
                PATH_TO_RBF_PLOT + f"/{fuel_name}_{additive_name}_{component_name}_mg_m3.png"
            )
        plt.close()
