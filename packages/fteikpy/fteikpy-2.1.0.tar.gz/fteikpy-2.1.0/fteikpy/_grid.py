import numpy

from ._base import BaseGrid2D, BaseGrid3D, BaseTraveltime
from ._fteik import ray2d, ray3d
from ._interp import vinterp2d, vinterp3d


class Grid2D(BaseGrid2D):
    def __init__(self, *args, **kwargs):
        """
        2D grid class.

        Parameters
        ----------
        grid : array_like
            Grid array.
        gridsize : array_like
            Grid size (dz, dx).
        origin : array_like
            Grid origin coordinates.

        """
        super().__init__(*args, **kwargs)


class Grid3D(BaseGrid3D):
    def __init__(self, *args, **kwargs):
        """
        3D grid class.

        Parameters
        ----------
        grid : array_like
            Grid array.
        gridsize : array_like
            Grid size (dz, dx, dy).
        origin : array_like
            Grid origin coordinates.

        """
        super().__init__(*args, **kwargs)


class TraveltimeGrid2D(BaseGrid2D, BaseTraveltime):
    def __init__(self, grid, gridsize, origin, source, gradient, vzero):
        """
        2D traveltime grid class.

        Parameters
        ----------
        grid : array_like
            Traveltime grid array.
        gridsize : array_like
            Grid size (dz, dx).
        origin : array_like
            Grid origin coordinates.
        source : array_like
            Source coordinates.
        gradient : array_like
            Gradient grid.
        vzero : scalar
            Slowness at the source.

        """
        super().__init__(
            grid=grid,
            gridsize=gridsize,
            origin=origin,
            source=source,
            gradient=gradient,
            vzero=vzero,
        )

    def __call__(self, points, fill_value=numpy.nan):
        """
        Bilinear apparent velocity interpolation.

        Parameters
        ----------
        points : array_like
            Query point coordinates or list of point coordinates.
        fill_value : scalar, optional, default nan
            Returned value for out-of-bound query points.

        Returns
        -------
        scalar or :class:`numpy.ndarray`
            Interpolated traveltime(s).

        """
        return vinterp2d(
            self.zaxis,
            self.xaxis,
            self._grid,
            numpy.asarray(points, dtype=numpy.float64),
            self._source,
            self._vzero,
            fill_value,
        )

    def raytrace(self, points, stepsize=None, honor_grid=False):
        """
        2D a posteriori ray-tracing.

        Parameters
        ----------
        points : array_like
            Query point coordinates or list of point coordinates.
        stepsize : scalar or None, optional, default None
            Unit length of ray.
        honor_grid : bool, optional, default False
            If `True`, coordinates of raypaths are calculated with respect to traveltime grid discretization. `stepsize` might not be honored.

        Returns
        -------
        :class:`numpy.ndarray` or list of :class:`numpy.ndarray`
            Raypath(s).

        """
        stepsize = stepsize if stepsize else numpy.min(self._gridsize)
        gradient = self.gradient

        return ray2d(
            self.zaxis,
            self.xaxis,
            gradient[0].grid,
            gradient[1].grid,
            numpy.asarray(points, dtype=numpy.float64),
            self._source,
            stepsize,
            honor_grid,
        )

    @property
    def gradient(self):
        """Return Z and X gradient grids as a list of :class:`fteikpy.Grid2D`."""
        return (
            [
                Grid2D(self._gradient[:, :, i], self._gridsize, self._origin)
                for i in range(2)
            ]
            if self._gradient is not None
            else [
                Grid2D(grad, self._gridsize, self._origin)
                for grad in numpy.gradient(self._grid, *self._gridsize)
            ]
        )


class TraveltimeGrid3D(BaseGrid3D, BaseTraveltime):
    def __init__(self, grid, gridsize, origin, source, gradient, vzero):
        """
        3D traveltime grid class.

        Parameters
        ----------
        grid : array_like
            Traveltime grid array.
        gridsize : array_like
            Grid size (dz, dx, dy).
        origin : array_like
            Grid origin coordinates.
        source : array_like
            Source coordinates.
        gradient : array_like
            Gradient grid.
        vzero : scalar
            Slowness at the source.

        """
        super().__init__(
            grid=grid,
            gridsize=gridsize,
            origin=origin,
            source=source,
            gradient=gradient,
            vzero=vzero,
        )

    def __call__(self, points, fill_value=numpy.nan):
        """
        Trilinear apparent velocity interpolation.

        Parameters
        ----------
        points : array_like
            Query point coordinates or list of point coordinates.
        fill_value : scalar, optional, default nan
            Returned value for out-of-bound query points.

        Returns
        -------
        scalar or :class:`numpy.ndarray`
            Interpolated traveltime(s).

        """
        return vinterp3d(
            self.zaxis,
            self.xaxis,
            self.yaxis,
            self._grid,
            numpy.asarray(points, dtype=numpy.float64),
            self._source,
            self._vzero,
            fill_value,
        )

    def raytrace(self, points, stepsize=None, honor_grid=False):
        """
        3D a posteriori ray-tracing.

        Parameters
        ----------
        points : array_like
            Query point coordinates or list of point coordinates.
        stepsize : scalar or None, optional, default None
            Unit length of ray.
        honor_grid : bool, optional, default False
            If `True`, coordinates of raypaths are calculated with respect to traveltime grid discretization. `stepsize` might not be honored.

        Returns
        -------
        :class:`numpy.ndarray` or list of :class:`numpy.ndarray`
            Raypath(s).

        """
        stepsize = stepsize if stepsize else numpy.min(self._gridsize)
        gradient = self.gradient

        return ray3d(
            self.zaxis,
            self.xaxis,
            self.yaxis,
            gradient[0].grid,
            gradient[1].grid,
            gradient[2].grid,
            numpy.asarray(points, dtype=numpy.float64),
            self._source,
            stepsize,
            honor_grid,
        )

    @property
    def gradient(self):
        """Return Z, X and Y gradient grids as a list of :class:`fteikpy.Grid3D`."""
        return (
            [
                Grid3D(self._gradient[:, :, :, i], self._gridsize, self._origin)
                for i in range(3)
            ]
            if self._gradient is not None
            else [
                Grid3D(grad, self._gridsize, self._origin)
                for grad in numpy.gradient(self._grid, *self._gridsize)
            ]
        )
