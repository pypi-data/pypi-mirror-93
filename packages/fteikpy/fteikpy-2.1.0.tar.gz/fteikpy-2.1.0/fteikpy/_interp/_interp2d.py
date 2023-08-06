import numpy
from numba import prange

from .._common import jitted


@jitted("f8(f8[:], f8[:], f8[:, :], f8, f8, f8)")
def _interp2d(x, y, v, xq, yq, fval):
    """Perform bilinear interpolation."""
    condx = x[0] <= xq <= x[-1]
    condy = y[0] <= yq <= y[-1]
    if not (condx and condy):
        return fval

    nx, ny = numpy.shape(v)
    nx -= 1
    ny -= 1

    i1 = numpy.searchsorted(x, xq, side="right") - 1
    j1 = numpy.searchsorted(y, yq, side="right") - 1
    i2 = i1 + 1
    j2 = j1 + 1

    if i1 == nx and j1 != ny:
        x1 = x[i1]
        x2 = 2.0 * x1 - x[-2]
        y1 = y[j1]
        y2 = y[j2]

        v11 = v[i1, j1]
        v21 = 1.0
        v12 = v[i1, j2]
        v22 = 1.0

    elif i1 != nx and j1 == ny:
        x1 = x[i1]
        x2 = x[i2]
        y1 = y[j1]
        y2 = 2.0 * y1 - y[-2]

        v11 = v[i1, j1]
        v21 = v[i2, j1]
        v12 = 1.0
        v22 = 1.0

    elif i1 == nx and j1 == ny:
        x1 = x[i1]
        x2 = 2.0 * x1 - x[-2]
        y1 = y[j1]
        y2 = 2.0 * y1 - y[-2]

        v11 = v[i1, j1]
        v21 = 1.0
        v12 = 1.0
        v22 = 1.0

    else:
        x1 = x[i1]
        x2 = x[i2]
        y1 = y[j1]
        y2 = y[j2]

        v11 = v[i1, j1]
        v21 = v[i2, j1]
        v12 = v[i1, j2]
        v22 = v[i2, j2]

    vq = v11 * numpy.abs((x2 - xq) * (y2 - yq))
    vq += v21 * numpy.abs((x1 - xq) * (y2 - yq))
    vq += v12 * numpy.abs((x2 - xq) * (y1 - yq))
    vq += v22 * numpy.abs((x1 - xq) * (y1 - yq))
    vq /= numpy.abs((x2 - x1) * (y2 - y1))

    return vq


@jitted(parallel=True)
def _interp2d_vectorized(x, y, v, xq, yq, fval):
    """Perform bilinear interpolation for different points."""
    nq = len(xq)
    out = numpy.empty(nq, dtype=numpy.float64)
    for i in prange(nq):
        out[i] = _interp2d(x, y, v, xq[i], yq[i], fval)

    return out


@jitted
def interp2d(x, y, v, q, fval=numpy.nan):
    """Perform bilinear interpolation."""
    if q.ndim == 1:
        return _interp2d(x, y, v, q[0], q[1], fval)

    else:
        return _interp2d_vectorized(x, y, v, q[:, 0], q[:, 1], fval)
