''' Centralised configuration for the application '''
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')


DATASETS = {
    "sample": os.path.join(DATA_DIR, 'sample_data.csv'),
}