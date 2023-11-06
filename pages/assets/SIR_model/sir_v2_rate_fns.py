import matplotlib.pyplot as plt
from cycler import cycler
from modelbase.ode import Model, Simulator

def infection(beta, s, i, r):
    return beta * s * i / (s + i + r)


def recovery(gamma, x):
    return gamma * x
