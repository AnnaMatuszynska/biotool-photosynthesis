def infection(beta, s, i, r):
    return beta * s * i / (s + i + r)

def proportional(k, x):
    return k * x
