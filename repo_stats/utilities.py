import numpy as np
import ast
from datetime import datetime, timezone


def rolling_average(unaveraged, window):
    """
    Obtain a rolling average of 'unaveraged' data in a sliding window of index length 'window'

    Arguments
    ---------
    unaveraged : list
        Data to be averaged
    window : int
        Width (in indices) of sliding window. Enforced to be odd

    Returns
    -------
    roll_avg : array
        Averaged data
    window : int
        The input 'window', potentially decreased by 1 to make odd
    """
    if not window % 2:
        print("window_avg should be odd --> decreasing by 1")
        window -= 1

    roll_avg = np.convolve(unaveraged, np.ones(window), mode="valid") / window

    return roll_avg, window
