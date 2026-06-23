# Graphical user interface
# Autor: Leon Okida
# Last changes: 03/30/2026

import streamlit as st
import networkx as nx
import streamlit.components.v1 as components
from pyvis.network import Network

from arborescence_generator.arborescence_generator import generate_arborescences

def main():
    st.set_page_config(page_title="Arborescence-Based Routing", layout="wide")
    
    st.title("Arborescence-Based Routing")
    st.sidebar.header("Settings")

    # loads the file
    file_upload = st.sidebar.file_uploader("Load topology file", type=['txt'])
    if file_upload is not None:
        try:
            lines = file_upload.getvalue().decode("utf-8").splitlines()
            graph = nx.parse_edgelist(lines)
            nx.set_edge_attributes(graph, 1, "capacity")
            routers = sorted(list(graph.nodes()))
        except Exception as e:
            st.error(f"Error upon reading file: {e}")
            return

        # Selects the origin and the destination of the routes
        st.sidebar.subheader("Select the origin and the destination")
        origin = st.sidebar.selectbox("Origin:", routers, index=0)
        destination = st.sidebar.selectbox("Destination:", routers, index=min(1, len(routers)-1))

        # Computes arborescence-based routes
        if st.sidebar.button("Compute Routes"):
            with st.spinner("Computing arborescence-based routes..."):
                arborescences = generate_arborescences(graph, destination)

            try:
                color_names = [
                    'blue', 'red', 'gold', 'green', 
                    'purple', 'maroon', 'turquoise', 'orange'
                ]
                
                colors_en = {
                    'blue': 'Blue', 'red': 'Red', 'gold': 'Yellow', 
                    'green': 'Green', 'purple': 'Purple', 'maroon': 'Maroon', 
                    'turquoise': 'Turquoise', 'orange': 'Orange'
                }

                arborescence_number = nx.edge_connectivity(graph)

                st.markdown(f"""
                    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
                        <h3 style="margin: 0;">Results:</h3>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="height: 15px; width: 15px; background-color: darkblue; border-radius: 50%; display: inline-block;"></span>
                            <span style="font-weight: bold;">Origin: {origin}</span>
                        </div>
                        <span style="font-size: 20px;">➝</span>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="height: 15px; width: 15px; background-color: orange; border-radius: 50%; display: inline-block;"></span>
                            <span style="font-weight: bold;">Destination: {destination}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                all_routes = []
                cols = st.columns(arborescence_number)
                
                for i in range(arborescence_number):
                    route = nx.shortest_path(G=arborescences[destination][i], source=origin, target=destination)
                    all_routes.append(route)
                    
                    curr_color = color_names[i % len(color_names)]
                    
                    with cols[i]:
                        st.markdown(f"**#{i + 1} Route**")
                        st.markdown(f"<span style='color:{curr_color}; font-weight:bold;'>{colors_en[curr_color]}</span>", unsafe_allow_html=True)
                        st.caption(" ➝ ".join(route))

                st.markdown("---")
                # Calls the function to draw the topology and the routes
                graphical_visualization(graph, all_routes, origin, destination, color_names)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("Waiting for the upload of the input file.")
    

    st.markdown("""
## About the tool
* This is an interactive tool that computes and displays **arborescence-based routes**.  
* The source code and the documentation are available [here](https://github.com/leonokida/arborescence_based_routing).
## Authors
* Leon Okida | [laogoncalves@inf.ufpr.br](mailto:laogoncalves@inf.ufpr.br)
* André Vignatti | [vignatti@inf.ufpr.br](mailto:vignatti@inf.ufpr.br)
* Elias P. Duarte Jr. | [elias@inf.ufpr.br](mailto:elias@inf.ufpr.br)
    """)
    st.markdown("""
## Example Inputs
* [Internet2](https://raw.githubusercontent.com/leonokida/arborescence_based_routing/refs/heads/main/topologies/internet2.txt)
* [RNP](https://raw.githubusercontent.com/leonokida/arborescence_based_routing/refs/heads/main/topologies/rnp.txt)
* [Géant](https://raw.githubusercontent.com/leonokida/arborescence_based_routing/refs/heads/main/topologies/geant.txt)
    """)

def graphical_visualization(G, routes, origin, destination, colors):
    """Renders the graph with the highlighted routes"""
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black", directed=False)
    net.set_options("""
    var options = {
        "nodes": {
            "font": {
                "size": 40
            }
        }
    }
    """)
    
    for node in G.nodes():
        color_no = "lightblue"
        size = 20
        if node == origin: color_no = "darkblue"; size = 25
        if node == destination: color_no = "orange"; size = 25
        net.add_node(node, label=str(node), color=color_no, size=size)

    # Mapping of edges
    highlighted_edges = {}
    for idx, routes in enumerate(routes):
        route_color = colors[idx % len(colors)]
        for u, v in zip(routes, routes[1:]):
            edge_key = frozenset([u, v])
            highlighted_edges[edge_key] = route_color

    for u, v in G.edges():
        curr_key = frozenset([u, v])
        
        if curr_key in highlighted_edges:
            edge_color = highlighted_edges[curr_key]
            width = 7
        else:
            edge_color = "lightgray"
            width = 1

        net.add_edge(u, v, color=edge_color, width=width)

    net.save_graph("graph_temp.html")
    with open("graph_temp.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=650)

if __name__ == "__main__":
    main()