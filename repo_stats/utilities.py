import os
import ast
from datetime import datetime, timezone
import numpy as np
from PIL import Image


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


def fill_missed_months(unique_output):
    """
    For an output of 'np.unique(x, return_counts=True)' where 'x' is a list of dates of the format '2024-01', fill in months missing in this list and set their count to 0.

    Arguments
    ---------
    unique_output : tuple of array
        Output of 'np.unique'

    Returns
    -------
    unique_output : list of array
        The input updated with inserted entries for missing months
    """
    unique_output = list(unique_output)

    now = datetime.now(timezone.utc)

    # build list of 'year-month' from oldest entry in 'unique_output' to current month
    oldest, newest = min(unique_output[0]), f"{now.year}-{now.month:02d}"
    years = [str(y) for y in list(range(int(oldest[:4]), int(newest[:4]) + 1))]
    months = [f"{m:02d}" for m in list(range(1, 13))]
    dates = []
    for y in years:
        for m in months:
            dates.append(f"{y}-{m}")
    dates = dates[dates.index(oldest) : dates.index(newest) + 1]

    # insert missing dates into 'unique_output'
    missed_months = [i for i in dates if i not in unique_output[0]]
    for i in missed_months:
        idx = np.searchsorted(unique_output[0], i)
        unique_output[0] = np.insert(unique_output[0], idx, i)
        unique_output[1] = np.insert(unique_output[1], idx, 0)

    return unique_output


def update_cache(cache_file, old_items, new_items):
    """
    Update 'cache_file' with 'new_items' entries, one per line

    Arguments
    ---------
    cache_file : str
        Path to existing ASCII cache file
    old_items, new_items : str or list of str
        Existing and new cache entries

    Returns
    -------
    all_items : list of str
        Combined 'old_items' and 'new_items'
    """
    with open(cache_file, "a+") as f:
        # add initial new line only when appending to existing entries in cache
        if len(old_items) != 0 and new_items != []:
            f.writelines("\n")

        f.writelines("\n".join([str(i) for i in new_items]))

        if new_items == []:
            print(f"  No new entries found - cache not updated")
        else:
            print(f"\n  Updated cache at {cache_file} with {len(new_items)} entries")

    with open(cache_file, "r") as f:
        all_items = f.readlines()
        all_items = [ast.literal_eval(i.rstrip("\n")) for i in all_items]

    return all_items


def make_transparent(image, color=(0,0,0)):
    im = Image.open(image) 
    rgba = im.convert("RGBA") 
    pixel_colors = rgba.getdata() 
  
    # in RGBA, transparent in (255, 255, 255, 0)
    t = (255, 255, 255, 0)
    pixel_colors_trans = [t if x[:3] == color else x for x in pixel_colors]
    rgba.putdata(pixel_colors_trans) 

    savename = f"{os.path.splitext(image)[0]}_transparent.png"
    print(f"Saving updated image as {savename}")
    rgba.save(savename, "PNG") 
