import unittest
from services.GetSourceData import GetSourceDataFiles
from services.ProcessFiles import ProcessFilesToDB
from pathlib import Path
import os

class TestGettingSourceFiles(unittest.TestCase):

    def test_getting_source_file(self):
        path = os.path.join(os.getcwd(), 'test', 'mock_source_data')
        source_files = [
            Path(os.path.join(os.getcwd(), 'test', 'mock_source_data', 'file_name.csv')),
            Path(os.path.join(os.getcwd(), 'test', 'mock_source_data', 'subfolder','file_name.csv'))
        ]
        source = GetSourceDataFiles()
        files = list(source.get_files(path, 'file_name.csv'))
        self.assertEqual(files, source_files)

if __name__ == '__main__':
    unittest.main()
