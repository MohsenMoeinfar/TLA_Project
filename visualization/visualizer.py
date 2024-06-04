import json
import matplotlib.pyplot as plt
import networkx as nx


def visualize(json_fa: str) -> None:
    # Create a graph
    G = nx.DiGraph()
    # Add some nodes and edges
    fa_dict = json.loads(json_fa)

    for state in fa_dict['states']:
        if state in fa_dict['final_states'] and state == fa_dict['initial_state']:
            G.add_node(state, label='init state - final state')
        elif state == fa_dict['initial_state']:
            G.add_node(state, label='init state')
        elif state in fa_dict['final_states']:
            G.add_node(state, label='final state')
        else:
            G.add_node(state, label=state)

    edges: dict[tuple[str, str], list[str]] = {}
    for node in fa_dict['states']:
        for symbol, neigh in fa_dict[node].items():
            if (node, neigh) not in edges.keys():
                G.add_edge(node, neigh)
                edges[(node, neigh)] = []
            edges[(node, neigh)].append(symbol)

    # Define node positions
    pos = nx.circular_layout(G)

    # Draw the graph
    plt.figure(figsize=(8, 6))  # Create a figure with a specified size
    ax = plt.gca()  # Get the current Axes instance on the current figure
    cf = ax.get_figure()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1500,
        node_color='lightblue',
        font_size=16,
        edge_color='gray',
        arrows=True,
        labels=nx.get_node_attributes(G, 'label')
    )
    nx.draw_networkx_edge_labels(G,
                                 pos,
                                 {key: ','.join(val) for key, val in edges.items()},
                                 font_size=12,
                                 rotate=False,
                                 )
    # cf.set_facecolor('lightgreen')

    # If you want to remove the axes
    ax.set_axis_off()
    plt.savefig(fname='temp.png')
    plt.show()  # Display the figure


if __name__ == "__main__":
    visualize('{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_4"], '
              '"alphabet": ["1", "2", "3", "4"], "q_0": {"1": "q_1", "2": "q_2", "3": "q_2", "4": "q_3"}, '
              '"q_1": {"1": "q_4", "2": "q_4", "3": "q_3", "4": "q_3"}, "q_2": {"1": "q_4", "2": "q_4", "3": "q_4", '
              '"4": "q_3"}, "q_3": {"1": "q_3", "2": "q_3", "3": "q_3", "4": "q_3"}, "q_4": {"1": "q_4", "2": "q_4", '
              '"3": "q_4", "4": "q_4"}}')
