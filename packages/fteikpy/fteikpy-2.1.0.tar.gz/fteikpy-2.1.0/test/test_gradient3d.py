import numpy
import pytest
from helpers import allclose, eik3d


@pytest.mark.parametrize(
    "points, gzref, gxref, gyref",
    (
        ([0.0, 0.0, 0.0], 0.0, 0.0, 0.0),
        ([-1.0, -1.0, -1.0], numpy.nan, numpy.nan, numpy.nan),
        (
            [
                [0.0, 0.0, 0.0],
                [15.0, 0.0, 0.0],
                [15.0, 15.0, 0.0],
                [0.0, 15.0, 0.0],
                [0.0, 0.0, 15.0],
                [15.0, 0.0, 15.0],
                [15.0, 15.0, 15.0],
                [0.0, 15.0, 15.0],
            ],
            [0.0, 1.0, 0.68911487, 0.0, 0.0, 0.68911487, 0.58770662, 0.0],
            [0.0, 0.0, 0.68911487, 1.0, 0.0, 0.0, 0.58770662, 0.68911487],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.68911487, 0.58770662, 0.68911487],
        ),
    ),
)
def test_call(points, gzref, gxref, gyref):
    sources = 0.0, 0.0, 0.0
    tt = eik3d.solve(sources, nsweep=3, return_gradient=True)

    allclose(gzref, points, lambda x: tt.gradient[0](x))
    allclose(gxref, points, lambda x: tt.gradient[1](x))
    allclose(gyref, points, lambda x: tt.gradient[2](x))
