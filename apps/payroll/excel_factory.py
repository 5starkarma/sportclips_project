import pandas as pd

filepath_xls = '/home/david/Documents/sportclips/sample_xls_reports/sample_1/Stylist_Analysis.xls'
filepath_xlsx = '/home/david/Documents/sportclips/sample_xlsx_reports/sample_1/StylistAnalysisReport.xlsx'


class XLSDataExtractor:
    def __init__(self, filepath, rows):
        self.data = pd.read_excel(filepath, sheet_name=0, header=None, skiprows=rows)

    @property
    def parsed_data(self):
        return self.data


class XLSXDataExtractor:
    def __init__(self, filepath, rows):
        self.data = pd.read_excel(filepath, sheet_name=0, header=None, skiprows=rows)

    @property
    def parsed_data(self):
        return self.data


def data_extraction_factory(filepath):
    if filepath.endswith('xls'):
        extractor = XLSDataExtractor
    elif filepath.endswith('xlsx'):
        extractor = XLSXDataExtractor
    else:
        raise ValueError(f'Cannot open {filepath}')
    return extractor(filepath)


def extract_data_from(filepath, r):
    factory_obj = None
    try:
        factory_obj = data_extraction_factory(filepath)
    except ValueError as e:
        print(e)
    return factory_obj

