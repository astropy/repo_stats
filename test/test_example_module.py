import numpy as np

from py_template.example_module import fibonacci, SoftwareGroup


def test_example_function() -> None:
    """Check the Fibonacci sequence function returns correct result"""
    fib = fibonacci(10)
    np.testing.assert_allclose(
        actual=fib,
        desired=[1, 1, 2, 3, 5, 8, 13, 21, 34, 55],
        rtol=1e0,
    )


def test_example_class() -> None:
    """Check the SoftwareGroup class can be instantiated and its class method called"""
    sg = SoftwareGroup(people="us", purpose="fun")
    sg.long_term_goals()
