import pandas as pd
import plotly.graph_objects as go


class SankeyTree:

    def __init__(self, dataframe, metric, root_nodes_col, sequence_cols):
        self.dataframe = dataframe
        self.metric = metric
        self.root_nodes_col = root_nodes_col
        self.sequence_cols = sequence_cols
        self.color_map = {}
        self.categorical_colors = self.generate_colors_with_opacity(0.25)
        
    @staticmethod
    def generate_colors_with_opacity(base_opacity):
        categorical_colors = [
            f'rgba(31, 119, 180, {base_opacity})',  # Blue
            f'rgba(255, 127, 14, {base_opacity})',  # Orange
            f'rgba(44, 160, 44, {base_opacity})',   # Green
            f'rgba(214, 39, 40, {base_opacity})',   # Red
            f'rgba(148, 103, 189, {base_opacity})', # Purple
            f'rgba(140, 86, 75, {base_opacity})',   # Brown
            f'rgba(227, 119, 194, {base_opacity})', # Pink
            f'rgba(127, 127, 127, {base_opacity})', # Gray
            f'rgba(188, 189, 34, {base_opacity})',  # Olive
            f'rgba(23, 190, 207, {base_opacity})'   # Cyan
        ]
        return categorical_colors
    
    def generate_nodes_and_links(self):
        # Nodes list and mapping of node names to indices
        nodes = []
        node_indices = {}
        
        # Helper function to add nodes and ensure uniqueness
        def add_node(node):
            if node not in node_indices:
                node_indices[node] = len(nodes)
                nodes.append(node)
                self.color_map[node_indices[node]] = self.categorical_colors[node_indices[node] % len(self.categorical_colors)]
                
        # Links with source, target, and value (metric)
        links = {'source': [], 'target': [], 'value': [], 'color': []}
        
        # Generate nodes and links
        for i, (src_col, tgt_col) in enumerate(zip([self.root_nodes_col] + self.sequence_cols[:-1], self.sequence_cols)):
            grouped_data = self.dataframe.groupby([src_col, tgt_col]).sum().reset_index()
            for _, row in grouped_data.iterrows():
                # Skip rows where the target doesn't provide a valid split or is identical to the source (for non-terminal nodes)
                if row[src_col] == row[tgt_col] and i < len(self.sequence_cols) - 1:
                    continue
                
                src_node = f'{src_col}: {row[src_col]}'
                tgt_node = f'{tgt_col}: {row[tgt_col]}'
                add_node(src_node)
                add_node(tgt_node)
                links['source'].append(node_indices[src_node])
                links['target'].append(node_indices[tgt_node])
                links['value'].append(row[self.metric])
                
        # Apply the color of the source node to the link
        for src in links['source']:
            links['color'].append(self.color_map[src])

        return nodes, links, node_indices


    def plot(self):
        nodes, links, node_indices = self.generate_nodes_and_links()
        
        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color=[self.color_map[node_indices[node]] for node in nodes]  # Map the colors correctly
            ),
            link=dict(
                source=links['source'],
                target=links['target'],
                value=links['value'],
                color=links['color']  # Apply the color mapping to the links
            ))])
        
        fig.update_layout(title_text=f"Sankey Diagram for {self.metric}", font_size=10)
        fig.show()
