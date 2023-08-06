"""Trajectory calculation module."""

import numpy as np

from ..spice import SPICEPool, SPICERef, et, utc
from ..spice.toolbox import sub_obs_pt


class Trajectory:
    """Trajectory calculation object.

    Parameters
    ----------
    kernels: str or tuple
        List of kernels to be loaded in the SPICE pool.

    observer: str or spice.SPICERef
        Observer SPICE reference.

    observer: str or spice.SPICERef
        Target SPICE reference.

    ets: float or str or list
        Ephemeris time(s).

    abcorr: str, optional
        Aberration corrections to be applied when computing
        the target's position and orientation.
        Only the SPICE keys are accepted.

    """

    def __init__(self, kernels, observer, target, ets, abcorr='NONE'):
        self.kernels = kernels

        # Init SPICE references
        self.observer = observer if isinstance(observer, SPICERef) else SPICERef(observer)
        self.target = target if isinstance(target, SPICERef) else SPICERef(target)

        # Init ephemeris times
        self.ets = ets

        # Optional parameters
        self.abcorr = abcorr

        # Init cache computation
        self.__sub_obs_pts = None

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}> '
            f'Observer: {self.observer} | '
            f'Target: {self.target}'
            f'\n - Start time: {self.start}'
            f'\n - Stop time: {self.stop}'
            f'\n - Nb of pts: {len(self)}'
        )

    def __len__(self):
        return len(self.ets)

    @property
    def kernels(self):
        """Get the list of kernels to used."""
        return self.__kernels

    @kernels.setter
    def kernels(self, kernels):
        """List of kernels setter.

        Note
        ----
        SPICE pool content is checked to see if
        all the kernels are correctly loaded.
        If it's not the case, the pool will
        be purge and refilled.

        """
        self.__kernels = kernels

        if SPICEPool != kernels:
            SPICEPool.add(kernels, purge=True)

    @property
    def ets(self):
        """Ephemeris times."""
        return self.__ets

    @ets.setter
    def ets(self, ets):
        """Ephemeris times setter."""
        if isinstance(ets, str):
            self.__ets = [et(ets)]
        elif isinstance(ets, (int, float)):
            self.__ets = [ets]
        elif isinstance(ets, (tuple, list, np.ndarray)):
            self.__ets = sorted([et(t) if isinstance(t, str) else t for t in ets])
        else:
            raise ValueError('Invalid input Ephemeris Time(s).')

    @property
    def start(self):
        """UTC start time."""
        return utc(self.ets[0])

    @property
    def stop(self):
        """UTC stop time."""
        return utc(self.ets[-1])

    @property
    def abcorr(self):
        """SPICE aberration correction."""
        return self.__abcorr

    @abcorr.setter
    def abcorr(self, key):
        """SPICE aberration correction setter."""
        if key.replace(' ', '').upper() not in [
            'NONE', 'LT', 'LT+S', 'CN', 'CN+S',
            'XLT', 'XLT+S', 'XCN', 'XCN+S',
        ]:
            raise KeyError(f'Invalid aberration correction key:`{key}`')
        self.__abcorr = key.upper()

    @property
    def sub_obs_pts(self):
        """Compute the sub-observer point calculation.

        Returns
        -------
        (float, fl)

        Note
        ----
        Currently the intersection method is fixed internally
        as ``method='NEAR POINT/ELLIPSOID'``.

        """
        if self.__sub_obs_pts is None:
            self.__sub_obs_pts = sub_obs_pt(
                self.ets,
                self.observer,
                self.target,
                abcorr=self.abcorr,
                method='NEAR POINT/ELLIPSOID')
        return self.__sub_obs_pts

    @property
    def sub_obs_lon_e(self):
        """Sub-observer east longitude (degree)."""
        return self.sub_obs_pts[1]

    @property
    def sub_obs_lat(self):
        """Sub-observer latitude (degree)."""
        return self.sub_obs_pts[2]

    @property
    def sub_obs_lonlat(self):
        """Sub-observer ground track (degree)."""
        return self.sub_obs_pts[1:]
