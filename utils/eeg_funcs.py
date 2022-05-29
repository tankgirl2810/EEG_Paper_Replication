""" Put Useful EEG utility functions here """
import mne
import pandas as pd
import matplotlib.pyplot as plt


def setup_eeg_data(df: pd.DataFrame, montage_name: str="biosemi64") -> mne.EvokedArray:
    """ Processes the dataframe and returns an evoked object. Useful for plotting

    Args:
        df: The dataframe to process (No formatting required)
    
    Returns:
        evoked: The evoked object
    """
    montage = mne.channels.make_standard_montage(montage_name)
    # Rename columns to just the lead names
    df = df.copy()
    df.rename(columns = lambda x: x.split(".")[-1], inplace=True)
    # Rename T3 and T4 to T7 and T8 and T5 and T6 to P7 and P8
    # Follows the MCN changes
    df.rename(columns={'T3': 'T7', 'T4': 'T8', 'T5': 'P7', 'T6': 'P8'}, inplace=True)
    # Create the info object
    ch_names = list(df.columns)
    info = mne.create_info(ch_names=ch_names, sfreq=128, ch_types='eeg')
    # Create the evoked object
    data = df.iloc[[0]].T
    evoked = mne.EvokedArray(data, info)
    evoked.set_montage(montage, on_missing='warn', match_case=False)
    return evoked 

def plot_topomap(df: pd.DataFrame, montage_name: str="biosemi64",
                 show_names: bool=False, ax: plt.Axes | None = None,
                 marker: str='k.', cmap: str='Reds') -> plt.Axes:
    """ Plots the topomap of the evoked object

    Args:
        df: The dataframe to process (No formatting required) 
        montage_name: The name of the montage to use
        show_names: Whether to show the channel names
        ax: The axes to plot on. If left as 'None', ax is created
        marker: The marker to use for the topomap. Uses matplotlib markers
        cmap: The colormap to use for the topomap
    """
    evoked = setup_eeg_data(df, montage_name)
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))
    # Plot the topo map to the axes provided
    mne.viz.plot_topomap(
        evoked.data[:, 0], 
        evoked.info, 
        axes=ax, 
        show=False, 
        names=evoked.ch_names,
        show_names=show_names,
        sensors=marker,
        cmap=cmap
    )
    return ax