from control.map import Map
from control.experiment_data import ExperimentData

if __name__ == '__main__':
    m = Map()
    m.save_all_rbf_map()
    #ex = ExperimentData()
    #ex.get_experiment_data('diesel', 'steam', 'NOx')
    #print(ex.df)
    #print(ex.get_rbf_data())

