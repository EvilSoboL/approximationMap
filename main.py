from control.map import Map
from control.experiment_data import ExperimentData
from control.database import DatabaseHandler
from control.uploader import FlameHeightUploader, GetExperimentData


if __name__ == '__main__':
    db = DatabaseHandler()
    ex = ExperimentData()
    m = Map()
    flame = FlameHeightUploader()
    gas_analysis = GetExperimentData()

    #m.save_all_source_map(russian=True)
    #m.show_3d_plot('diesel', 'steam', 'CO', russian=True)
    m.show_map_without_postprocessing('diesel', 'steam', 'CO', russian=True)
