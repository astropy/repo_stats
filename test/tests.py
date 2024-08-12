import numpy as np 

from repo_stats.utilities import rolling_average

def test_rolling_average():
    x = np.arange(10)

    np.testing.assert_allclose(
        actual=rolling_average(x, window=3)[0],
        desired=[1, 2, 3, 4, 5, 6, 7, 8],
        rtol=1e0,
    )
    
    