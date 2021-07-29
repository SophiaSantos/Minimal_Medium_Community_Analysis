import numpy as np
from tqdm import tqdm
import os

from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt

import cobra
from cobra.io import read_sbml_model

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/sophia_models"

SBML_FILE = (os.path.join(basePath, 'model_saz_v13a.xml'))
model = read_sbml_model(SBML_FILE)

## == model parameters
medium = model.medium

minimal_medium = ['EX_C00059__dra', 'EX_C00009__dra', 'EX_C14818__dra', 'EX_C00001__dra']

oxygen = ['EX_C00007__dra']

carbon = ['EX_C00011__dra']

ammonia = ['EX_C00014__dra']

for i in carbon:
    model.reactions.get_by_id(i).lower_bound = -12
    model.reactions.get_by_id(i).upper_bound = -12

for i in oxygen:
    model.reactions.get_by_id(i).lower_bound = -1
    model.reactions.get_by_id(i).upper_bound = -1

for i in ammonia:
    model.reactions.get_by_id(i).lower_bound = -0.018
    model.reactions.get_by_id(i).upper_bound = -0.018

#solution = model.optimize()
#print(model.summary())

def add_dynamic_bounds(model, y):
    """Use external concentrations to bound the uptake flux of glucose."""
    biomass, co2, cell, ac, d_ala, hco3 = y  # expand the boundary species
    co2_max_import = -10 * co2 / (5 + co2) # altered to meet model conditions
    model.reactions.EX_C00011__dra.lower_bound = -12


def dynamic_system(t, y):
    """Calculate the time derivative of external species."""

    biomass, co2, cell, ac, d_ala, hco3 = y  # expand the boundary species

    # Calculate the specific exchanges fluxes at the given external concentrations.
    with model:
        add_dynamic_bounds(model, y)

        cobra.util.add_lp_feasibility(model)
        feasibility = cobra.util.fix_objective_as_constraint(model)
        lex_constraints = cobra.util.add_lexicographic_constraints(
            model, ['e_Biomass__cytop', 'EX_C00011__dra', 'EX_C00760__dra', 'EX_C00033__dra', 'EX_C00993__dra', 'EX_C00288__dra'], ['max', 'max', 'max', 'max', 'max', 'max'])

    # Since the calculated fluxes are specific rates, we multiply them by the
    # biomass concentration to get the bulk exchange rates.
    fluxes = lex_constraints.values
    fluxes *= biomass

    # This implementation is **not** efficient, so I display the current
    # simulation time using a progress bar.
    if dynamic_system.pbar is not None:
        dynamic_system.pbar.update(1)
        dynamic_system.pbar.set_description('t = {:.3f}'.format(t))

    return fluxes

dynamic_system.pbar = None


def infeasible_event(t, y):
    """
    Determine solution feasibility.

    Avoiding infeasible solutions is handled by solve_ivp's built-in event detection.
    This function re-solves the LP to determine whether or not the solution is feasible
    (and if not, how far it is from feasibility). When the sign of this function changes
    from -epsilon to positive, we know the solution is no longer feasible.

    """

    with model:

        add_dynamic_bounds(model, y)

        cobra.util.add_lp_feasibility(model)
        feasibility = cobra.util.fix_objective_as_constraint(model)

    return feasibility - infeasible_event.epsilon

infeasible_event.epsilon = 1E-6
infeasible_event.direction = 1
infeasible_event.terminal = True

ts = np.linspace(0, 20, 100)  # Desired integration resolution and interval
y0 = [0.1, -12, 0.0, 0.0, 0.0, 0.0]

with tqdm() as pbar:
    dynamic_system.pbar = pbar

    sol = solve_ivp(
        fun=dynamic_system,
        events=[infeasible_event],
        t_span=(ts.min(), ts.max()),
        y0=y0,
        t_eval=ts,
        rtol=1e-6,
        atol=1e-8,
        method='BDF'
    )

print(sol)

ax = plt.subplot(111)
ax.plot(sol.t, sol.y.T[:, 0], label = 'Biomass')
ax2 = plt.twinx(ax)
ax2.plot(sol.t, sol.y.T[:, 1], color='r', label='CO2')
ax2.plot(sol.t, sol.y.T[:, 2], color='g', label = 'Cellulose')
ax2.plot(sol.t, sol.y.T[:, 3], color='y', label = 'Acetate')
ax2.plot(sol.t, sol.y.T[:, 4], color='k', label = 'D-Alanyl-D-alanine')
ax2.plot(sol.t, sol.y.T[:, 5], color='k', label = 'Bicarbonate')

ax.set_ylabel('Biomass', color='b')

plt.title("Cellulose production in S. azorense")
plt.legend()
plt.show()