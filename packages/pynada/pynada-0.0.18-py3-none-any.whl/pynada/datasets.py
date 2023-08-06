from .commons import *
import pandas as pd


def list_datasets():
    """
    Returns a list of all datasets in the catalog
    Returns: DataFrame of dataset information
    """
    
    params = {}
    response = make_get_request('datasets', params)
 
    return pd.DataFrame.from_dict(response['datasets']).set_index('id')


def search_datasets_by_idno(partial_idno):
    """
    Returns a list of datasets whose idno contains a partial match
    Returns: DataFrame of dataset information
    """

    datasets = list_datasets()
    return datasets[datasets['idno'].str.contains(partial_idno)]

