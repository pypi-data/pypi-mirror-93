# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Markov Decision Process (MDP)
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

from md_pro.src.uc_mdp.uc_mdp_main import *
from scipy.spatial.distance import pdist, squareform
import argparse
import igraph as ig
import plotly.graph_objects as go
'''
Start a MDP challenge
'''
def start_mdp(params, mdp_challenge):
    obj_mdp = service_MDP()
    dict_mdp = obj_mdp.start_mdp(params, mdp_challenge)
    logging.info(dict_mdp['pi'])
    return dict_mdp

'''
Get the points of a regular grid
'''
def get_meshgrid_points(params):
    xgrid = np.linspace(-10, 10, params["x_grid"])
    ygrid = np.linspace(-10, 10, params["y_grid"])
    X, Y=np.meshgrid(xgrid,ygrid)
    x=np.ravel(X)
    y=np.ravel(Y)
    z=0*y
    P={}
    points=np.transpose(np.vstack((x, y, z))).tolist()
    for idx, act_point in enumerate(points):
        P[str(idx)]=act_point
    return P


'''
Compute distance matrix
'''
def compute_distance_matrix(P):
    rtb=np.vstack(list(P.values()))
    C=squareform(pdist(rtb))
    return C

'''
Convert distance matrix to k_nearest_neigh-topology-matrix
'''
def convert_distance_knear_neigh_mat(C, k=5):
    T = np.zeros((np.size(C,0), np.size(C,1)), dtype=bool)
    idx_mat=np.argsort(C, axis=0)
    for i in range(0, np.size(C, 1)):
        act_idx=idx_mat[0:4, i]
        T[act_idx, i]=True
    return T

"""
get topology T and states for a regular grid
#states
S = ['0', '1', '2', '3']
#topology
T=np.array([[True, True, False, True],
                  [True, True, True, False],
                  [False, True, True, True],
                  [True, False, True, True]])
"""

def get_simple_topology_for_regular_grid(params, P):
    C=compute_distance_matrix(P)
    T=convert_distance_knear_neigh_mat(C)
    amount_nodes=params["y_grid"]*params["x_grid"]
    S=[str(i) for i in range(0, amount_nodes)]
    # T = np.zeros((amount_nodes, amount_nodes), dtype=bool)
    # T=np.eye(amount_nodes, dtype=bool)
    return T, S

'''
Topology to edge list
'''
def topology_to_edge_list(T):
    edge_list=[]
    T=T.tolist()
    for itp in range(0, len(T)):
        act_list=T[itp]
        new_ind=[idx for idx, x in enumerate(act_list) if x]
        for qrt in new_ind:
            edge_list.append((itp, qrt))
    return edge_list
'''
Plot the results
'''
def plot_the_result(dict_mdp, mdp_challenge):
    edge_list=topology_to_edge_list(mdp_challenge['T'])
    g = ig.Graph(edge_list)
    g.vs["name"] = dict_mdp['S']
    g.vs["reward"] = dict_mdp['R']
    g.vs["label"] = g.vs["name"]
    P_2D=list(mdp_challenge['P'].values())
    x_vec = [wlt[0] for wlt in P_2D]
    y_vec = [wlt[1] for wlt in P_2D]
    layout = ig.Layout(P_2D)
    g.vs["vertex_size"] = 20
    visual_style = {}
    visual_style["edge_curved"] = False
    colors = [(1, 0, 1) for i in range(0, len(dict_mdp['S']))]
    g.vs["color"] = colors
    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=x_vec, y=y_vec, text=dict_mdp['S'],
                             mode='markers',
                             name='grid_points'))
    fig.add_trace(go.Scattergl(x=x_vec, y=y_vec,
                    mode='markers',
                    name='value_markers',
                    marker=dict(size=dict_mdp['U'],
                                         color=dict_mdp['U'])
                                         ))
    fig.show()

"""
Reach n-steps
"""
def next_neighbour():
    None

"""
Reachability analysis for topological spaces and n-steps
"""
def reach_n_steps(strt_pnt, mdp_challenge, dict_mdp, params, steps=3):
    reach=[]
    # first neighbours
    neigh=dict_mdp['action'][strt_pnt]
    # reachability variable
    reach.append(neigh)
    for i in range(0, steps):
        neigh = []
        # actual neighbours
        last_reach=reach[i]
        for qrt in last_reach:
            new_neigh=dict_mdp['action'][qrt]
            for wlt in new_neigh:
                neigh.append(wlt)
        neigh=np.unique(neigh)
        reach.append(neigh)
    return reach
"""
Get the trajectory for reachability analysis
"""
def get_trajectory(strt_pnt, dict_mdp, reach_set):
    traj=[]
    traj.append(strt_pnt)
    U=dict_mdp['U']
    for act_reach in reach_set:
        act_U=np.array([U[int(wlt)] for wlt in act_reach])
        idx=np.argmax(act_U)
        candidate=act_reach[idx]
        if(candidate in dict_mdp['action'][traj[-1]]):
            traj.append(candidate)
    return traj