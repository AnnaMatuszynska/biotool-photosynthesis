from modelbase.ode import Simulator
from modelbase.ode.integrators import Scipy

simulator = Simulator(model, integrator=Scipy)