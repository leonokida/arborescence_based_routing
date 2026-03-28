# Arborescence-Based Routing
## Authors: Leon Okida, Elias P. Duarte Jr. and André Vignatti

This repository provides an interactive tool for the computing and visualization of routes in graphs based on **edge-disjoint arborescences**.
It is available on [arborescencebasedrouting.streamlit.app](https://arborescencebasedrouting.streamlit.app/).

## About the Tool
* The tool consists of a program which receives a graph, representing a topology, and two vertices which represent the origin and the destination of a packet.
* Given the edge-connectivity $\lambda$ of the graph, the program decomposes the topology into $\lambda$ arborescences rooted in the destination vertex.
* The arborescences are used to compute $\lambda$ independent routes between the origin and the destination.
* Finally, the tool displays the routes on top of the topology on the main panel.

## Tool Architecture
The tool has two main components:

1.  **Arborescence generator (`arborescence_generator/`):** It contains the logic which receives an `nx.Graph` and computes the arborescences rooted in the destination vertex.
2.  **Graphical User Interface (`main.py`):** It manages the input file and the visualization of the results using the `Pyvis` and `Streamlit` packages.

## Installation
The tool requires Python 3.10+. To configure the environment, follow the steps to install the dependencies:

```bash
# Clone the repository
$ git clone https://github.com/leonokida/arborescence_based_routing.git
$ cd arborescence_based_routing

# Install the dependencies
$ pip install -r requirements.txt
```

The main dependencies are the `networkx`, `streamlit` and `pyvis` packages.

## Execution
### Accessing the tool
The tool is available on [Streamlit Share](https://arborescencebasedrouting.streamlit.app/).  
Alternatively, to execute the tool locally, install it and execute the following command:
```bash
$ streamlit run main.py
```
The tool will be available on `http://localhost:8501/`.
### User flow
1. On the side tab, upload the file containing the topology of the network in the edge list format.
2. Select the **origin** and the **destination**.
3. Click on **"Compute Routes"**.
4. The tool will display the computed routes and display them graphically on top of the topology.

## Input file format
The file must be a simple text file in the [edge list format](https://networkx.org/documentation/stable/reference/readwrite/edgelist.html), where each line represents an edge of the topology:
```txt
s a
s f

f g

a b
a c
a e

c d

b t
e t
d t
g t
```