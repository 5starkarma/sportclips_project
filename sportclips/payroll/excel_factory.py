from builtins import property

import pandas as pd


class XLSDataExtractor:
    """
    Extracts the data from an Excel (XLS) spreadsheet
    Output is a pandas data-frame.
    """
    def __init__(self, file_path):
        self.data = pd.read_excel(file_path, sheet_name=0, header=None)

    @property
    def parsed_data(self):
        return self.data


class XLSXDataExtractor:
    """
    Extracts the data from an Excel (XLSX) spreadsheet.
    Output is a pandas data-frame.
    """
    def __init__(self, file_path):
        self.data = pd.read_excel(file_path, sheet_name=0, header=None)

    @property
    def parsed_data(self):
        return self.data


def data_extraction_factory(file_path):
    """A function for assigning the correct DataExtractor constructor."""

    if file_path.endswith('xls'):
        extractor = XLSDataExtractor
    elif file_path.endswith('xlsx'):
        extractor = XLSXDataExtractor
    else:
        raise ValueError(f'Cannot open the file: {file_path}. Incorrect file type.')

    return extractor(file_path)


def extract_data_from(file_path):
    """A function for exception handling."""
    factory_obj = None

    try:
        factory_obj = data_extraction_factory(file_path)
    except ValueError as e:
        print(e)

    return factory_obj
