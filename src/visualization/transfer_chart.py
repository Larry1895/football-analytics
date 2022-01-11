import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from src.scrapper.repositories.player_club_transfer_repository import find_transfers_for_club

transfers = find_transfers_for_club(1)

from_nodes = []
to_nodes = []
weight_edges = []
weight_edges_width = []

for transfer in transfers:
    from_nodes.append(transfer.from_club_id)
    to_nodes.append(transfer.to_club_id)
    weight_edges.append(transfer.fee)

    weight_edge = transfer.fee / 1000000
    if weight_edge < 1:
        weight_edge = 1
    weight_edges_width.append(weight_edge)

# Build a dataframe with your connections
df = pd.DataFrame({'from': from_nodes, 'to': to_nodes, 'value': weight_edges})

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())

pos = nx.spring_layout(G, k=1, iterations=100)

# Custom the nodes:
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='b', width=1,
        edge_cmap=plt.cm.Blues, alpha=0.3, arrows=True)
plt.show()
