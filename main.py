import os

from control.map import Map
from control.experiment_data import ExperimentData
from control.database import DatabaseHandler
from control.uploader import ApproximatedMapUploader, FlameHeightUploader
from config import DATA_RES_DIR

from config import COMPONENTS_TO_CONVERSATION_FROM_PPM_TO_MG_M3

if __name__ == '__main__':
    db = DatabaseHandler()
    ex = ExperimentData()
    m = Map()
    upl = FlameHeightUploader()

    upl.save_to_csv(os.path.join(DATA_RES_DIR, 'diesel_steam_flame_height.csv'))
    #m.save_all_source_map_to_excel()

    #m.save_all_rbf_map()
    #m.save_all_rbf_map_to_excel()

    #m.save_all_co_min_map()
    #m.save_all_o2_min_map()



