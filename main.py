from handlers.database import DatabaseHandler
from handlers.experiment import ExperimentData
from config import PATH_TO_EXCEL

if __name__ == '__main__':
    ex = ExperimentData()
    ex.experiments_info()
