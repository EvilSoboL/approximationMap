import pytest
import pandas as pd
import numpy as np

from control.experiment_data import ExperimentData

ed = ExperimentData()


def test_get_df_in_matrix():
    ed.get_experiment_data('diesel', 'steam', 'CO')
    df = pd.DataFrame({
        'F_fuel': [0, 0, 1, 1],
        'F_steam': [0, 1, 0, 1],
        'CO': [3, 1, 4, 2]
    })
    ed.df = df

    fuel_set, additive_set, arr = ed.get_df_in_matrix(df)
    assert fuel_set == [0, 1]
    assert additive_set == [0, 1]
    assert np.array_equal(arr, np.array([[1, 2], [3, 4]]))


def test_get_df_in_matrix_other_values():
    ed.get_experiment_data('diesel', 'steam', 'CO')
    df = pd.DataFrame({
        'F_fuel': [1, 1, 2, 2],
        'F_steam': [0, 1, 0, 1],
        'CO': [5, 2, 7, 3]
    })
    ed.df = df

    fuel_set, additive_set, arr = ed.get_df_in_matrix(df)
    assert fuel_set == [1, 2]
    assert additive_set == [0, 1]
    assert np.array_equal(arr, np.array([[2, 3], [5, 7]]))


def test_get_df_in_matrix_single_value():
    ed.get_experiment_data('diesel', 'steam', 'CO')
    df = pd.DataFrame({
        'F_fuel': [1],
        'F_steam': [0],
        'CO': [3]
    })
    ed.df = df

    fuel_set, additive_set, arr = ed.get_df_in_matrix(df)
    assert fuel_set == [1]
    assert additive_set == [0]
    assert np.array_equal(arr, np.array([[3]]))


def test_get_df_in_matrix_negative_values():
    ed.get_experiment_data('diesel', 'steam', 'CO')
    df = pd.DataFrame({
        'F_fuel': [0, 0, 1, 1],
        'F_steam': [0, 1, 0, 1],
        'CO': [-3, 1, -4, 2]
    })
    ed.df = df

    fuel_set, additive_set, arr = ed.get_df_in_matrix(df)
    assert fuel_set == [0, 1]
    assert additive_set == [0, 1]
    assert np.array_equal(arr, np.array([[1, 2], [-3, -4]]))
