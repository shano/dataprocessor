# Open folder
# Iterate over folders and find certificates.csv and append to list

import logging

from services.GetSourceData import GetSourceDataFiles
from services.ProcessFiles import ProcessFilesToDB

if __name__=='__main__':
    logging.info('Starting epc data import')

    source = GetSourceDataFiles()
    process_files_to_db = ProcessFilesToDB(source)
    process_files_to_db.process()

    logging.info('Finishing epc data import')

    # TODO - Once core data is persisted, trigger event
    # here that would iterate over the db and populate lng/lat separately