from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from cycler import cycler


def sir(t, y, alpha, beta):
    s, i, r = y
    infection = alpha * s * i / (s + i + r)
    recovery = beta * i
    return (
        -infection,  # ds/dt
        infection - recovery,  # di/dt
        recovery,  # dr/dt
    )


res = solve_ivp(
    sir,
    t_span=(0, 20),
    y0=(900, 100, 0),  # needs to match s, i, r unpacking order
    args=(2, 0.5),  # needs to match fn argument order
)


