import os
import itertools
import csv

import numpy as np
import pandas as pd

from framed import load_cbmodel
from framed import essential_reactions
from framed import FVA
from reframed import pFBA, FBA, Environment
from optimModels.utils.utils import fix_exchange_reactions_model
from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.optimization.run import cbm_strain_optim
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.constantes import optimType

met_list = []
rxn_list = []
exchange_dict = []
Rxn = []
Flux = []
constraints = {}

def simulation_output (fModel, fSimulation):
    for r_id, rxn in fModel.reactions.items():
        if rxn.is_exchange or r_id.startswith('R_sink'):
            met_list.append(rxn.get_substrates())
            rxn_list.append(fSimulation.get_fluxes_distribution()[r_id])

    met_list_merged = list(itertools.chain(*met_list))
    met_list_name = [1] * len(met_list_merged)

    for m_id, met in fModel.metabolites.items():
        for k in met_list_merged:
            for l in range(0, len(met_list_merged)):
                if met_list_merged[l] == m_id:
                    met_list_name[l] = str(met)

    for m in range(0, len(met_list_name)):
        exchange_dict.update({met_list_name[m]: rxn_list[m]})

    for key in exchange_dict:
        if exchange_dict[key] != 0:
            Rxn.append(key)
            Flux.append(exchange_dict[key])
            print('Rxn: ' + str(key) + ', Flux: ' + str(exchange_dict[key]))

    constraints.update({j: (0, 0)})
