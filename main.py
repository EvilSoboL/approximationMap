from control.map import Map
from control.experiment_data import ExperimentData
from control.database import DatabaseHandler

if __name__ == '__main__':
    #m = Map()
    #m.save_all_source_map()
    db = DatabaseHandler()
    ex = ExperimentData()
    print(ex.get_minimum_and_maximum_consumption())


