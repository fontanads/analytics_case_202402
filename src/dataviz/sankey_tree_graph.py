import pandas as pd
import plotly.graph_objects as go


class SankeyTree:
    def __init__(self, dataframe, metric, root_nodes_col, sequence_cols):
        self.dataframe = dataframe
        self.metric = metric
        self.root_nodes_col = root_nodes_col
        self.sequence_cols = sequence_cols
        
    def generate_nodes_and_links(self):
        # Nodes list and mapping of node names to indices
        nodes = []
        node_indices = {}
        
        # Helper function to add nodes and ensure uniqueness
        def add_node(node):
            if node not in node_indices:
                node_indices[node] = len(nodes)
                nodes.append(node)
                
        # Links with source, target, and value (metric)
        links = {'source': [], 'target': [], 'value': []}
        
        # Generate nodes and links
        for cols in zip([self.root_nodes_col] + self.sequence_cols, self.sequence_cols):
            src_col, tgt_col = cols
            for _, row in self.dataframe.groupby([src_col, tgt_col]).sum().reset_index().iterrows():
                src_node = f'{src_col}: {row[src_col]}'
                tgt_node = f'{tgt_col}: {row[tgt_col]}'
                add_node(src_node)
                add_node(tgt_node)
                links['source'].append(node_indices[src_node])
                links['target'].append(node_indices[tgt_node])
                links['value'].append(row[self.metric])
        
        return nodes, links

    def plot(self):
        nodes, links = self.generate_nodes_and_links()
        
        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
            ),
            link=dict(
                source=links['source'],
                target=links['target'],
                value=links['value']
            ))])
        
        fig.update_layout(title_text=f"Sankey Diagram for {self.metric}", font_size=10)
        fig.show()

# # Example usage with your DataFrame
# data = {
#     "platform": ["Desktop", "Desktop", "Mobile App", "Mobile App", "Mobile Web", "Mobile Web"],
#     "mobile": ["Desktop", "Desktop", "Mobile", "Mobile", "Mobile", "Mobile"],
#     "year": [2022, 2023, 2022, 2023, 2022, 2023],
#     "net_gross_booking_usd": [76.42, 68.86, 9.12, 13.09, 14.46, 18.04],
#     "net_orders": [69.38, 60.66, 11.98, 16.64, 18.63, 22.70],
#     "avg_ticket": [300.54, 288.29, 207.72, 199.86, 211.71, 201.90]
# }

# df = pd.DataFrame(data)

# # Creating a Sankey chart instance
# sankey_chart = SankeyChart(df, 'net_gross_booking_usd', 'year', ['mobile', 'platform'])

# # Generating and plotting the Sankey diagram
# sankey_chart.plot()
