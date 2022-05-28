import pandas as pd
from os.path import join
from os import listdir

def load_eeg_data(path: str) -> pd.DataFrame:
    """ Loads EEG data from a csv file.

    Args:
        path (str): Path to the csv file.

    Returns:
        pd.DataFrame: EEG data.
    """
    return pd.read_csv(join(path, 'EEG.machinelearing_data_BRMH.csv'), index_col=0)