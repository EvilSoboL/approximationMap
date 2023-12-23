from control.database import DatabaseHandler
from control.experiment import ExperimentData
from config import PATH_TO_EXCEL

if __name__ == '__main__':
    ex = ExperimentData()
    ex.get_experiment_data('diesel', 'air', 'CO')

