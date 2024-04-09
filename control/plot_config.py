import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

from config import PATH_TO_SOURCE_PLOT, PATH_TO_RBF_PLOT


def save_source_plot(
         fuel_name, additive_name, component_name, fuel_axis, additive_axis, component_matrix,  ppm=True
):
    fuel_axis_str = [str(np.round(value, decimals=2)) for value in fuel_axis]
    additive_axis_str = [str(np.round(value, decimals=2)) for value in additive_axis[::-1]]

    fig, ax = plt.subplots(figsize=(16, 9))
    plt.rcParams.update({'font.size': 18})

    sns.heatmap(component_matrix, linewidths=1.5, annot=True, fmt='g', ax=ax)

    # Название графика
    if ppm:
        if component_name == 'O2':
            plt.title(r"Source: $O_2$, vol.%")

        elif component_name == 'CO':
            plt.title(r"Source: $CO, ppm$")

        elif component_name == 'NO':
            plt.title(r"Source: $NO$, ppm")

        elif component_name == 'NO2':
            plt.title(r"Source: $NO_2$, ppm")

        elif component_name == 'NOx':
            plt.title(r"Source: $NO_X, ppm$")

        elif component_name == 'CO2':
            plt.title(r"Source: $CO_2$, vol.%")

        elif component_name == 'SO2':
            plt.title(r"Source: $SO_2$, ppm")

    else:
        if component_name == 'CO':
            plt.title(r"Source: $CO$, $mg/m^3$")
        else:
            plt.title(r"Source: $NO_X$, $mg/m^3$")

    # Подписи осей
    plt.xticks(range(len(fuel_axis)), fuel_axis_str)
    plt.yticks(range(len(additive_axis)), additive_axis_str)

    if fuel_name == 'waste_oil':
        ax.set_xlabel(r"$F_{\text{waste oil}}$, kg/h")

    elif fuel_name == 'crude_oil':
        ax.set_xlabel(r"$F_{\text{crude oil}}$, kg/h")

    elif fuel_name == 'heavy_oil':
        ax.set_xlabel(r"$F_{\text{heavy oil}}$, kg/h")

    else:
        ax.set_xlabel(f"$F_{{{fuel_name}}}$, kg/h")
    ax.set_ylabel(f"$F_{{{additive_name}}}$, kg/h")

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
