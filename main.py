from control.map import Map
from control.experiment_data import ExperimentData
from control.database import DatabaseHandler

if __name__ == '__main__':
    db = DatabaseHandler()
    ex = ExperimentData()
    m = Map()

    m.save_all_rbf_map()
    #print(ex.get_rbf_data())


