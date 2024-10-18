import os

from control.map import Map
from control.experiment_data import ExperimentData
from control.database import DatabaseHandler
from control.uploader import ApproximatedMapUploader, FlameHeightUploader, GetExperimentData
from config import DATA_RES_DIR

from config import COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3

if __name__ == '__main__':
    db = DatabaseHandler()
    ex = ExperimentData()
    m = Map()
    flame = FlameHeightUploader()
    gas_analysis = GetExperimentData()

    #flame.save_to_csv(os.path.join(DATA_RES_DIR, 'diesel_steam_flame_height.csv'))
    #gas_analysis.save_experiment_data_to_csv(
    #    os.path.join(DATA_RES_DIR, 'diesel_steam_gas_analysis.csv'),
    #    1,
    #    'steam')

    #db.get_experiment_data('waste_oil_40_2024', 'steam', 'CO')
    #m.save_all_source_map_to_excel()
    #m.save_all_source_map()

    #m.save_all_rbf_map()
    #m.save_all_rbf_map_to_excel()

    m.save_all_co_min_map()
    #m.save_all_o2_min_map()



