# Guru

Guru is a Universal Reputation Module for Distributed Consensus Protocols. This is the simulation of the protocol written in Python 2.7 based on our paper.

## Required Libraries

- SciPy
- matplotlib
- Tkinter

## Running the simulation

Simply compile the `gurudemo.py` python file, and use the graphical interface.
To start a simulation, first specify the number of nodes and the initial maliciousness `alpha_0` (a value between 0 and 1), and choose your preferred selection function and external reputation, then click on `Start!`.

Dynamic changes during a simulation:
- You can flip the honesty of nodes with the `Botnet` function. If you write a positive number, it will turn that many malicious nodes into bad nodes, and if you write a negative number, it will flip that many honest nodes into bad nodes.
- The `Sybil` function adds the written number of either honest or malicious nodes to the network, based on the sign of the integer (positive for honest, negative for malicious nodes)
- The `Remove` function is similar to the `Sybil` one, but it removes the given number of honest or malicious nodes from the network.
- The `Track node` function tracks the reputation value of the closest honest node to the giver value on the bottom two graphs with a green marker.

Every function starts working on the click of their respective `Go!` buttons.

The graphs describe the following:
- The main graph is the success rate of the protocol based on the last 100 rounds.
- The bottom left graph is the current ordered reputation distribution in blue and the original reputation distribution in red.
- The bottom right graph is the nodes grouped into 1/10th of all nodes sized tuples, ordered by reputation.
- The small graph under the options is the overall maliciousness of the network
