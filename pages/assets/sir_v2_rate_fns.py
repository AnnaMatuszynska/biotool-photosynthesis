def infection(alpha, s, i, r):
    return alpha * s * i / (s + i + r)


def recovery(beta, x):
    return beta * x
