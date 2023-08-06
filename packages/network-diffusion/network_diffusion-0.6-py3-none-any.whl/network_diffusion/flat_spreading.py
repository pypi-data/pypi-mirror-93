# Copyright 2020 by Michał Czuba, Piotr Bródka. All Rights Reserved.
#
# This file is part of Network Diffusion.
#
# Network Diffusion is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# Network Diffusion is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the  GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Network Diffusion. If not, see <http://www.gnu.org/licenses/>.
# =============================================================================
import os
import random
from typing import Any, List, Optional, Tuple, Union

import imageio
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def si_diffusion(
    G: nx.Graph,
    fract_I: float,
    beta_coeff: float,
    track: bool = False,
    name: Optional[str] = None,
) -> Tuple[
    List[int], List[int], List[int], List[List[Any]], List[Union[str, float]]
]:
    """
    Function to simulate Suspected - Infected diffusion on graph G.

    :param G: given graph
    :param fract_I: fraction of infected nodes on start of simulation
        (values 0-1)
    :param beta_coeff: probability of cognition during interaction with ill
        node (one interaction per iteration of simulation) (values 0-1)
    :param track: boolean value to mark if function has to print graph logs on
        console
    :param name: name of given graph - none by default. It is used in further
        visualisations

    :return:
        * list of number of suspected nodes by epoch,
        * list of number of infected nodes by epoch,
        * list of epochs,
        * list of names of new infected nodes by epoch,
        * list of metadata of experiment: name_of_graph, beta_coef, fract_coef
    """
    # Check if given parameters are good
    assert fract_I <= 100 and fract_I > 0
    assert beta_coeff <= 100 and beta_coeff > 0

    # Initialise empty lists to save diffusion statistics
    list_S = []  # list of number of suspected nodes
    list_I = []  # list of number of infected nodes
    list_iter = []  # list of number of iterations
    counter = 0  # main loop iterations counter
    nodes_infected = []  # list of names of infected nodes in each epoch
    nodes_in_epoch_infected = []  # list to keep infections in one epoch

    # Count number of nodes in graph at all
    num_N = len(G.nodes())

    # Count number of infected nodes on start and draw them
    num_I = int(fract_I * num_N) if int(fract_I * num_N) > 0 else 1
    infected_nodes_seed = random.sample(list(G.nodes().keys()), num_I)
    if track:
        print(num_I, " - num infected seed:\n", infected_nodes_seed)

    # Add attribute 'status' to graph to keep information about state of each node
    status_dict = {n: "suspected" for n in G.nodes()}
    nx.set_node_attributes(G, status_dict, "status")
    for n in infected_nodes_seed:
        G.nodes[n]["status"] = "infected"

    # Fill lists with starting parameters
    list_I.append(num_I)
    list_S.append(num_N - num_I)
    list_iter.append(counter)
    nodes_infected.append(infected_nodes_seed)
    if track:
        print(
            "Epoch - {}, Number - {}, Ill - {}, Suspected - {}".format(
                counter, num_N, num_I, num_N - num_I
            )
        )

    # Main loop of simulation - do it unless all nodes are ill
    while num_N > num_I:
        # One epoch of simulation - iteration_nodes through all nodes
        for n in G.nodes():
            # Omit nodes which are infected yet
            if G.nodes[n]["status"] != "infected":
                # Check neighbours of given node, when one is infected try to
                # infect given node too by drawing a number from binomial
                # distribution.
                # If infection happens skip iterating through neighbors
                for m in nx.neighbors(G, n):
                    if (
                        G.nodes[m]["status"] == "infected"
                        and np.random.choice(
                            np.arange(0, 2), p=[1 - beta_coeff, beta_coeff]
                        )
                        == 1
                    ):
                        G.nodes[n]["status"] = "infected"
                        nodes_in_epoch_infected.append(n)
                        num_I += 1
                        break

        # Append info to lists and reset nodes_in_epoch_list
        counter += 1
        nodes_infected.append(nodes_in_epoch_infected)
        nodes_in_epoch_infected = list()
        list_I.append(num_I)
        list_S.append(num_N - num_I)
        list_iter.append(counter)

        if track:
            print(
                "Epoch - {}, Number - {}, Ill - {}, Suspected - {}".format(
                    counter, num_N, num_I, num_N - num_I
                )
            )

    if name is None:
        name = "x"

    return (
        list_S,
        list_I,
        list_iter,
        nodes_infected,
        [name, beta_coeff, fract_I],
    )


def sir_diffusion(
    G: nx.Graph,
    fract_I: float,
    beta_coeff: float,
    gamma_coeff: float,
    track: bool = False,
    name: Optional[str] = None,
) -> Tuple[
    List[int],
    List[int],
    List[int],
    List[int],
    List[List[Any]],
    List[List[Any]],
    List[Union[str, float]],
]:
    """
    Function to simulate Suspected - Infected - Recovered diffusion on graph G.

    :param G: given graph
    :param fract_I: fraction of infected nodes on start of simulation
        (values 0-1)
    :param beta_coeff: probability of cognition during interaction with ill
        node (one interaction per iteration of simulation) (values 0-1)
    :param gamma_coeff: probability of recovery
    :param track: boolean value to mark if function has to print graph logs on
        console
    :param name: name of given graph - none by default. It is used in further
        visualisations
    :return:
        * list of number of suspected nodes by epoch,
        * list of number of infected nodes by epoch,
        * list of number of recovered nodes by epoch,
        * list of epochs,
        * list of names of new infected nodes by epoch,
        * list of names of new recovered nodes by epoch,
        * list of metadata of experiment: name_of_graph, beta_coef, gamma_coef,
            fract_coef
    """
    # Check if given parameters are good
    assert 100 >= fract_I > 0
    assert 100 >= beta_coeff > 0
    assert 100 >= gamma_coeff > 0

    # Initialise empty lists to save diffusion statistics
    list_S = []  # list of number of suspected nodes
    list_I = []  # list of number of infected nodes
    list_R = []  # list of number of recovered nodes
    list_iter = []  # list of number of iterations
    counter = 0  # main loop iterations counter
    nodes_infected = []  # list of names of infected nodes in each epoch
    nodes_in_epoch_infected = []  # list to keep infections in one epoch
    nodes_recovered: List[List[Any]] = []  # list od names of recovered nodes
    # in each epoch
    nodes_in_epoch_recovered = []  # list to save recoveries in one epoch

    # Count number of nodes in graph at all
    num_N = len(G.nodes())

    # Count number of infected nodes on start and draw them
    num_I = int(fract_I * num_N) if int(fract_I * num_N) > 0 else 1
    infected_nodes_seed = random.sample(list(G.nodes().keys()), num_I)
    if track:
        print(num_I, " - num infected seed:\n", infected_nodes_seed)

    # Initialise number of recovered nodes in graph
    R = 0

    # Add attr 'status' to graph to keep information about state of each node
    status_dict = {n: "suspected" for n in G.nodes()}
    nx.set_node_attributes(G, status_dict, "status")
    for n in infected_nodes_seed:
        G.nodes[n]["status"] = "infected"

    # Fill lists with starting parameters
    list_I.append(num_I)
    list_S.append(num_N - num_I - R)
    list_R.append(R)
    list_iter.append(counter)
    nodes_infected.append(infected_nodes_seed)
    nodes_recovered.append([])
    if track:
        print(
            f"Epoch - {counter}, Number - {num_N}, Suspected - {num_N - num_I - R}, "
            f"Ill - {num_I}, Recovered - {R}"
        )

    # Main loop of simulation - do it unless all nodes are recovered & no is ill
    while num_N > R and num_I != 0:
        # One epoch of simulation - iteration_nodes through all nodes
        for n in G.nodes():
            #  If node is infected try to make it recovered by drawing a value
            #  given binomial distribution
            if (
                G.nodes[n]["status"] == "infected"
                and np.random.choice(
                    np.arange(0, 2), p=[1 - gamma_coeff, gamma_coeff]
                )
                == 1
            ):
                G.nodes[n]["status"] = "recovered"
                nodes_in_epoch_recovered.append(n)
                R += 1
                num_I -= 1

            elif G.nodes[n]["status"] == "suspected":
                # Check neighbours of given node, when one is infected try to
                # infect given node too by drawing a number from binomial
                # distribution.
                # If infection happens skip iterating through neighbors
                for m in nx.neighbors(G, n):
                    if (
                        G.nodes[m]["status"] == "infected"
                        and np.random.choice(
                            np.arange(0, 2), p=[1 - beta_coeff, beta_coeff]
                        )
                        == 1
                    ):
                        G.nodes[n]["status"] = "infected"
                        nodes_in_epoch_infected.append(n)
                        num_I += 1
                        break

        # Append info to lists and reset nodes_in_epoch_list
        counter += 1
        nodes_infected.append(nodes_in_epoch_infected)
        nodes_in_epoch_infected = []
        nodes_recovered.append(nodes_in_epoch_recovered)
        nodes_in_epoch_recovered = []

        list_I.append(num_I)
        list_R.append(R)
        list_S.append(num_N - num_I - R)
        list_iter.append(counter)

        if track:
            print(
                f"Epoch - {counter}, Number - {num_N}, "
                f"Suspected - {num_N - num_I - R}, Ill - {num_I}, "
                f"Recovered - {R}"
            )

    if name is None:
        name = "x"

    return (
        list_S,
        list_I,
        list_R,
        list_iter,
        nodes_infected,
        nodes_recovered,
        [name, beta_coeff, gamma_coeff, fract_I],
    )


def _print_si_params(fig_params: List[Union[str, float]]) -> str:
    """
    Function to print parameters of plotted visualisation of SI diffusion.

    :param fig_params: list with 3 elements (printable):
        - name of graph,
        - beta coefficient,
        - fraction of ill nodes on start

    :return: formatted string which is a subtitle of gif
    """
    return rf"Graph - {fig_params[0]}, $\beta$ - {fig_params[1]}, \
    $I/N$ - {fig_params[2]}"


def visualise_si_nodes(
    G: nx.Graph,
    nodes_infected: List[List[Any]],
    fig_params: List[Union[str, float]],
    path: str,
) -> None:
    """
    Function to visualise SI diffusion.

    It plots a gif from given experiment results with state of NODES.

    :param G: given graph on which the experiment has been performed.
    :param nodes_infected: list of lists which contains nodes infected in each
        epoch.
    :param fig_params: parameters_of experiment to plot as the title of figure.
        List with - name of graph, beta coefficient, fraction of infected nodes
        on start.
    :param path: path to save figure at.

    :return: After call, this function saves rendered gif into program's dir.
    """
    # Data frame with characteristics for nodes
    node_labels = pd.DataFrame(
        {
            "ID": [n for n in G.nodes()],
            "status": ["suspected" for m in G.nodes()],
        }
    )
    node_labels = node_labels.set_index("ID")

    # Set the layout of visualisation - circular
    pos = nx.circular_layout(G)

    # Initialise list to store figures to plot gif
    image_list = list()

    # Main loop of the function
    for i in range(len(nodes_infected)):

        # Mark nodes which were infected in i epoch as infected in the node
        # labels dataframe
        for n in nodes_infected[i]:
            node_labels.at[n] = "infected"

        # Transform categorical column in a numerical value:
        # group1->1, group2->2...
        node_labels["status"] = pd.Categorical(node_labels["status"])

        # Plot a image of this epoch:
        fig, ax = plt.subplots(figsize=(7, 7))
        nx.draw(
            G,
            pos=pos,
            with_labels=True,
            node_color=node_labels["status"].cat.codes,
            cmap=plt.cm.Set1,
            node_size=100,
            alpha=0.7,
            font_size=10,
        )

        plt.figtext(
            0.5, 0.92, _print_si_params(fig_params), fontsize=10, ha="center"
        )
        plt.figtext(0.5, 0.94, "SI diffusion", fontsize=10, ha="center")
        plt.figtext(0.95, 0.05, i, fontsize=10, ha="right")

        # Draw the canvas, cache the image and append it to image_list
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
        image_list.append(
            image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        )

        plt.close(fig)

    # Convert image_list to gif
    if not os.path.isdir(path):
        os.mkdir(path)
    imageio.mimsave(f"{path}/{fig_params[0]}_si_n.gif", image_list, fps=1.5)


def visualise_si_nodes_edges(
    G: nx.Graph,
    nodes_infected: List[List[Any]],
    fig_params: List[Union[str, float]],
    path: str,
) -> None:
    """
    Function to visualise SI diffusion.

    It plots a gif from given experiment results with state of EDGES and NODES.

    :param G: given graph on which the experiment has been performed.
    :param nodes_infected: list of lists which contains nodes infected in each
        epoch.
    :param fig_params: parameters_of experiment to plot as the title of figure.
        List with - name of graph, beta coefficient, fraction of infected
        nodes on start.
    :param path: path to save figure at.

    :return: After call, this function saves rendered gif into program's dir.
    """
    # Data frame with characteristics for nodes - on start all nodes are
    # 'suspected'
    node_labels = pd.DataFrame(
        {
            "ID": [n for n in G.nodes()],
            "status": ["suspected" for m in G.nodes()],
        }
    )
    node_labels = node_labels.set_index("ID")

    # Data frame with characteristics for edges - on start all nodes are
    # 'passive'
    edge_labels = pd.DataFrame(
        {
            "from": [n[0] for n in G.edges()],
            "to": [n[1] for n in G.edges()],
            "status": "passive",
        }
    )

    # Make copy of edge_labels to easily reset this dataframe
    # edge_labels_start = edge_labels.copy()

    # Set the layout of visualisation - circular
    pos = nx.circular_layout(G)

    # Initialise list to store figures to plot gif
    image_list = list()

    # Main loop of the function
    for i in range(len(nodes_infected)):

        # Mark nodes which were infected in i epoch as infected in the node
        # labels dataframe
        for n in nodes_infected[i]:
            node_labels.at[n] = "infected"

            # Mark edges which were active in i epoch. These are the those
            # who are network_diffusion from infected nodes
            edges = list(G.edges([n]))
            for e in edges:
                index = edge_labels[
                    (
                        (edge_labels["from"] == e[0])
                        & (edge_labels["to"] == e[1])
                    )
                    | (
                        (edge_labels["from"] == e[1])
                        & (edge_labels["to"] == e[0])
                    )
                ].index.values.astype(int)
                edge_labels.at[index, "status"] = "active"

        # Transform categorical column in a numerical value:
        # group1->1, group2->2...
        node_labels["status"] = pd.Categorical(
            node_labels["status"], categories=["infected", "suspected"]
        )
        edge_labels["status"] = pd.Categorical(
            edge_labels["status"], categories=["active", "passive"]
        )

        # Plot a image of this epoch:
        fig, ax = plt.subplots(figsize=(7, 7))
        nx.draw(
            G,
            pos=pos,
            with_labels=True,
            node_color=node_labels["status"].cat.codes,
            edge_color=edge_labels["status"].cat.codes,
            cmap=plt.cm.Set1,
            edge_cmap=plt.cm.Set1,
            node_size=100,
            alpha=0.7,
            font_size=10,
        )

        plt.figtext(
            0.5, 0.92, _print_si_params(fig_params), fontsize=10, ha="center"
        )
        plt.figtext(0.5, 0.94, "SI diffusion", fontsize=10, ha="center")
        plt.figtext(0.95, 0.05, i, fontsize=10, ha="right")

        # Draw the canvas, cache the image and append it to image_list
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
        image_list.append(
            image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        )

        plt.close(fig)

    # Convert image_list to gif
    if not os.path.isdir(path):
        os.mkdir(path)
    imageio.mimsave(f"{path}/{fig_params[0]}_si_ne.gif", image_list, fps=1.5)


def _print_sir_params(fig_params: List[Union[str, float]]) -> str:
    """
    Function to print parameters of plotted visualisation of SIR diffusion.

    :param fig_params: list with 4 elements (printable):
        name of graph,
        beta coefficient,
        gamma coefficient,
        fraction of ill nodes on start.

    :return: formatted string which is a subtitle of gif.
    """
    return rf"Graph - {fig_params[0]}, $\beta$ - {fig_params[1]}, \
    $\gamma$ - {fig_params[2]}, $I/N$ - {fig_params[3]}"


def visualise_sir_nodes(
    G: nx.Graph,
    nodes_infected: List[List[Any]],
    nodes_recovered: List[List[Any]],
    fig_params: List[Union[str, float]],
    path: str,
) -> None:
    """
    Function to visualise SIR diffusion.

    It plots a gif from given experiment results with state of NODES.

    :param G: given graph on which the experiment has been performed.
    :param nodes_infected: list of lists which contains nodes infected in each
    epoch.
    :param fig_params: parameters_of experiment to plot as the title of figure.
     List with - name of graph, beta coefficient, fraction of infected nodes
     on start.
    :param path: path to save figure at.

    :return: After call, this function saves rendered gif into program's dir.
    """
    # Data frame with characteristics for nodes
    node_labels = pd.DataFrame(
        {
            "ID": [n for n in G.nodes()],
            "status": ["suspected" for m in G.nodes()],
        }
    )
    node_labels = node_labels.set_index("ID")

    # Set the layout of visualisation - circular
    pos = nx.circular_layout(G)

    # Initialise list to store figures to plot gif
    image_list = list()

    # Main loop of the function
    for i in range(len(nodes_infected)):

        # Mark nodes which were infected in i epoch as infected in the node
        # labels dataframe

        for n in nodes_infected[i]:
            node_labels.at[n] = "infected"

        # Mark nodes which were recovered in i epoch as infected in the node
        # labels dataframe
        for n in nodes_recovered[i]:
            node_labels.at[n] = "recovered"

        # Transform categorical column in a numerical value:
        # group1->1, group2->2...
        node_labels["status"] = pd.Categorical(
            node_labels["status"],
            categories=["infected", "recovered", "suspected"],
        )

        # Plot a image of this epoch:
        fig, ax = plt.subplots(figsize=(7, 7))
        nx.draw(
            G,
            pos=pos,
            with_labels=True,
            node_color=node_labels["status"].cat.codes,
            cmap=plt.cm.Set1,
            node_size=100,
            alpha=0.7,
            font_size=10,
        )

        plt.figtext(
            0.5, 0.92, _print_sir_params(fig_params), fontsize=10, ha="center"
        )
        plt.figtext(0.5, 0.94, "SIR diffusion", fontsize=10, ha="center")
        plt.figtext(0.95, 0.05, i, fontsize=10, ha="right")

        # Draw the canvas, cache the image and append it to image_list
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
        image_list.append(
            image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        )

        plt.close(fig)

    # Convert image_list to gif
    if not os.path.isdir(path):
        os.mkdir(path)
    imageio.mimsave(f"{path}/{fig_params[0]}_sir_n.gif", image_list, fps=2)


def visualise_sir_nodes_edges(
    G: nx.Graph,
    nodes_infected: List[List[Any]],
    nodes_recovered: List[List[Any]],
    fig_params: List[Union[str, float]],
    path: str,
) -> None:
    """
    Function to visualise SIR diffusion.

    It plots a gif from given experiment results with state of NODES and EDGES.

    :param G: given graph on which the experiment has been performed.
    :param nodes_infected: list of lists which contains nodes infected in each
        epoch.
    :param fig_params: parameters_of experiment to plot as the title of figure.
        List with - name of graph, beta coefficient, fraction of infected
        nodes on start.
    :param path: path to save figure at.

    :return: After call, this function saves rendered gif into program's dir.
    """
    # Data frame with characteristics for nodes
    node_labels = pd.DataFrame(
        {
            "ID": [n for n in G.nodes()],
            "status": ["suspected" for m in G.nodes()],
        }
    )
    node_labels = node_labels.set_index("ID")

    # Data frame with characteristics for edges - on start all nodes are 'passive'
    edge_labels = pd.DataFrame(
        {
            "from": [n[0] for n in G.edges()],
            "to": [n[1] for n in G.edges()],
            "status": "passive",
        }
    )

    # Set the layout of visualisation - circular
    pos = nx.circular_layout(G)

    # Initialise list to store figures to plot gif
    image_list = list()

    # Main loop of the function
    for i in range(len(nodes_infected)):

        # Mark nodes which were infected in i epoch as infected in the node
        # labels dataframe
        for n in nodes_infected[i]:
            node_labels.at[n] = "infected"

            # Mark edges which are active. These are the those which are
            # network_diffusion from infected nodes
            edges = list(G.edges([n]))
            for e in edges:
                index = edge_labels[
                    (
                        (edge_labels["from"] == e[0])
                        & (edge_labels["to"] == e[1])
                    )
                    | (
                        (edge_labels["from"] == e[1])
                        & (edge_labels["to"] == e[0])
                    )
                ].index.values.astype(int)
                edge_labels.at[index, "status"] = "active"

        # Mark nodes which were recovered in i epoch as infected in the node
        # labels dataframe
        for n in nodes_recovered[i]:
            node_labels.at[n] = "recovered"

            # Mark edges which are active. These are the those which are
            # network_diffusion from infected nodes
            edges = list(G.edges([n]))
            for e in edges:
                index = edge_labels[
                    (
                        (edge_labels["from"] == e[0])
                        & (edge_labels["to"] == e[1])
                    )
                    | (
                        (edge_labels["from"] == e[1])
                        & (edge_labels["to"] == e[0])
                    )
                ].index.values.astype(int)
                edge_labels.at[index, "status"] = "passive"

        # Transform categorical column in a numerical value:
        # group1->1, group2->2...
        node_labels["status"] = pd.Categorical(
            node_labels["status"],
            categories=["infected", "recovered", "suspected"],
        )
        edge_labels["status"] = pd.Categorical(
            edge_labels["status"], categories=["active", "passive"]
        )

        # Plot a image of this epoch:
        fig, ax = plt.subplots(figsize=(7, 7))
        nx.draw(
            G,
            pos=pos,
            with_labels=True,
            node_color=node_labels["status"].cat.codes,
            edge_color=edge_labels["status"].cat.codes,
            cmap=plt.cm.Set1,
            edge_cmap=plt.cm.Set1,
            node_size=100,
            alpha=0.7,
            font_size=10,
        )

        plt.figtext(
            0.5, 0.92, _print_sir_params(fig_params), fontsize=10, ha="center"
        )
        plt.figtext(0.5, 0.94, "SIR diffusion", fontsize=10, ha="center")
        plt.figtext(0.95, 0.05, i, fontsize=10, ha="right")

        # Draw the canvas, cache the image and append it to image_list
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
        image_list.append(
            image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        )

        plt.close(fig)

    # Convert image_list to gif
    if not os.path.isdir(path):
        os.mkdir(path)
    imageio.mimsave(f"{path}/{fig_params[0]}_sir_ne.gif", image_list, fps=2)
