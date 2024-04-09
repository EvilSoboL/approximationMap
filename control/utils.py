import pandas as pd


def get_min_indexes_in_approximated_surface(fuel_axis, additive_axis, approximated_component_surface) -> tuple[list, list]:
    """
    Метод, который возвращает индексы (значения x и y) минимальных значений в каждой строке интерполяционной
    поверхности (approximated_component_surface).

    Args:
        fuel_axis - значения оси расхода топлива,
        additive_axis - значения оси расхода добавочного компонента,
        approximated_surface - аппроксимированная поверхность добавочного компонента.

    Returns:
        tuple[list, list]: Индексы минимальных значений в каждой строке аппроксимированной поверхности.
    """
    df = pd.DataFrame(approximated_component_surface, columns=fuel_axis, index=additive_axis)
    df = df.idxmin(axis=1)
    min_x = list(df)
    min_y = list(df.index)

    return min_x, min_y


def linear_function(fx, a, b):
    return a * fx + b
