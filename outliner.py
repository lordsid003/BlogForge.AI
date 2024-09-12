import networkx as nx
import plotly.graph_objects as go

class Outliner:
    def create_mind_map(self, outline):
        G = nx.Graph()

        central_node = outline[0]
        G.add_node("Main", size=30, color="darkblue", hover_text=central_node)

        for i, item in enumerate(outline[1:], 1):
            label = f"Topic {i}"
            G.add_node(label, size=20, color="lightcoral", hover_text=item)
            G.add_edge("Main", label)

        pos = nx.spring_layout(G, k=0.8, seed=42)

        # Edges coordinates
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        # Nodes coordinates
        node_x, node_y = [], []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        # Scatter plot for edges
        fig = go.Figure(data=[
            go.Scatter(x=edge_x, y=edge_y, line=dict(width=2, color='gray'),
                       hoverinfo='none', mode='lines'),
            go.Scatter(
                x=node_x, y=node_y, mode='markers+text',
                marker=dict(
                    size=[G.nodes[node]['size'] for node in G.nodes()],
                    color=[G.nodes[node]['color'] for node in G.nodes()],
                    opacity=0.85, 
                    line=dict(width=2, color="black") 
                ),
                text=[node for node in G.nodes()],
                textposition="top center",
                textfont=dict(color='black'),
                hoverinfo='text',
                hovertext=[G.nodes[node]['hover_text'] for node in G.nodes()]
            )
        ])
        
        fig.update_layout(
            title="Interactive Mind Map", title_x=0.5,
            showlegend=False, hovermode='closest',
            plot_bgcolor='rgba(240,240,240,0.9)',
            margin=dict(b=20, l=5, r=5, t=40),
            height=500,
        )
        return fig