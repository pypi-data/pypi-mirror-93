# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Markov Decision Process (MDP)
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import logging
import argparse
from md_pro.src.uc_mdp.uc_mdp_main import *
from __init__ import *
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ##################
    ### Parameters ###
    ##################
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample_time', '-Ts', type=float, help='Ts=0.1',
                        default='0.1', required=False)
    parser.add_argument('--gamma', '-gam', type=float, help='gamma=0.9',
                        default='0.9', required=False)
    parser.add_argument('--x_grid', '-xgr', type=int, help='x_grid=5',
                        default='8', required=False)
    parser.add_argument('--y_grid', '-ygr', type=int, help='y_grid=5',
                        default='5', required=False)
    parser.add_argument('--n_optimal', '-nopt', type=int, help='n_optimal=5',
                        default='5', required=False)
    args = parser.parse_args()
    params = vars(args)
    ####################################################
    ### Challenge with Markov Decision Process (MDP) ###
    ####################################################
    #start point
    strt_pnt='0'
    # points
    P=get_meshgrid_points(params)
    # Topology
    T, S = get_simple_topology_for_regular_grid(params, P)
    # rewards
    R = {'35': 100}
    mdp_challenge = {'S': S, 'R': R, 'T': T, 'P': P}
    # start Markov Decision Process
    dict_mdp=start_mdp(params, mdp_challenge)
    # reachability analysis n steps
    reach_set=reach_n_steps(strt_pnt, mdp_challenge, dict_mdp, params, steps=8)
    # deterministic trajectory generation
    optimal_traj=get_trajectory(strt_pnt, dict_mdp)
    #get stochastic probability
    get_stochastic_trajectory(strt_pnt, dict_mdp, 10)



