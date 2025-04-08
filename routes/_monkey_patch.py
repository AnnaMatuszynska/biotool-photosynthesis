from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, cast

import numpy as np
import scipy.integrate as spi
from modelbase.ode.integrators.int_scipy import _IntegratorScipy
from modelbase.typing import ArrayLike


def _simulate(
    self: _IntegratorScipy,
    *,
    t_end: Optional[float] = None,
    steps: Optional[int] = None,
    time_points: Optional[ArrayLike] = None,
    **integrator_kwargs: Dict[str, Any],
) -> Tuple[Optional[ArrayLike], Optional[ArrayLike]]:
    if time_points is not None:
        if time_points[0] != 0:
            t = [self.t0]
            t.extend(time_points)
        else:
            t = cast(List, time_points)
        t_array = np.array(t)

    elif steps is not None and t_end is not None:
        # Scipy counts the total amount of return points rather than
        # steps as assimulo
        steps += 1
        t_array = np.linspace(self.t0, t_end, steps)
    elif t_end is not None:
        t_array = np.linspace(self.t0, t_end, 100)
    else:
        raise ValueError("You need to supply t_end (+steps) or time_points")
    res = spi.solve_ivp(
        fun=self.rhs,
        t_span=(t_array[0], t_array[-1]),
        y0=self.y0,
        t_eval=t_array,
        method="Radau",  # RK45, RK23, DOP853, Radau, BDF, LSODA
        **{**self.kwargs, **integrator_kwargs},  # type: ignore
    )
    y = res.y.T
    self.t0 = t_array[-1]
    self.y0 = y[-1, :]
    return list(t_array), y
