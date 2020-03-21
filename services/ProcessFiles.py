from pathlib import Path
from abc import ABC, abstractmethod

import multiprocessing
import os
import pandas as pd
from sqlalchemy import create_engine

# TODO - pool.map limitations mean fields/engine are poorly defined here
# This is due to limitations around pool.map(it won't take class methods or multiple arguments)
# This is also definitely going to make testing a challenge.

# TODO - Could be a json string in environment variable
fields = [
    'LMK_KEY', 'LODGEMENT_DATE', 'TRANSACTION_TYPE', 'TOTAL_FLOOR_AREA', 'ADDRESS', 'POSTCODE'
]

engine = create_engine(os.environ['DEST_SQL'])

def push_files_to_db(filepath):
    df = pd.read_csv(filepath, usecols=fields)
    df.to_sql(os.environ['DEST_TABLE'], con=engine, index=False, if_exists='append')

# TODO - This push functionality could then support multiple destinations
# adhering to the abstract class
# e.g pushing to s3 and having SQS/Lambda process completely separately
class AbstractProcessFiles(ABC):
    # This could push to a queue etc
    @abstractmethod
    def process(self, fields):
        pass


class ProcessFilesToDB(AbstractProcessFiles):
    def __init__(self, source):
        self.source = source

    def process(self):
        files = self.source.get_files(os.environ['SRC_DATA_FOLDER'], os.environ['SRC_FILE_NAME'])
        # Can be tweaked pending further testing on dedicated hardware
        cores_to_use = round(multiprocessing.cpu_count()/2)
        pool = multiprocessing.Pool(processes=cores_to_use)
        pool.map(push_files_to_db, files)
        pool.close()