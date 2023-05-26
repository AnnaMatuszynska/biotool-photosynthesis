from scipy.integrate import solve_ivp


def sir(t, y, beta, gamma):
    s, i, r = y
    infection = beta * s * i / (s + i + r)
    recovery = gamma * i
    return (
            -infection,             # ds/dt
            infection - recovery,   # di/dt
            recovery,               # dr/dt
    )

res = solve_ivp(
        sir, t_span=(0, 100),
        y0=(0.9, 0.1, 0),       # needs to match s, i, r unpacking order
        args=(1, 0.1),          # needs to match fn argument order
)
