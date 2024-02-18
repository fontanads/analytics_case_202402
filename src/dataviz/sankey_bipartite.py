"""A sankey chart for a bipartite graph showing the flow of source nodes to target nodes."""
import pandas as pd
import plotly.graph_objects as go


class SankeyBipartite:
    """A class to create a Sankey chart from a DataFrame with source and target nodes and a flow value."""
    def __init__(self, df: pd.DataFrame, flow_column: str, source_column: str, target_column: str, normalized=False):
        self.df = df
        self.flow_column = flow_column
        self.source_column = source_column
        self.target_column = target_column
        self.normalized = normalized
        self.source_nodes, self.target_nodes, self.all_nodes = self.prepare_nodes()
        self.colors = self.assign_colors()

    def prepare_nodes(self):
        unique_nodes = sorted(set(self.df[self.source_column].unique()).union(self.df[self.target_column].unique()))
        source_nodes = [f"Source: {val}" for val in unique_nodes]
        target_nodes = [f"Target: {val}" for val in unique_nodes]
        all_nodes = source_nodes + target_nodes  # This will inherently match since they're based on the same unique_nodes list
        return source_nodes, target_nodes, all_nodes

    def assign_colors(self):
        # Assign unique colors based on the base node names without prefixes
        unique_nodes = sorted(set(self.df[self.source_column].unique()).union(self.df[self.target_column].unique()))
        base_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        color_dict = {f"Source: {node}": self.hex_to_rgba(base_colors[i % len(base_colors)], opacity=0.8) for i, node in enumerate(unique_nodes)}
        color_dict.update({f"Target: {node}": color_dict[f"Source: {node}"] for node in unique_nodes})  # Ensure target nodes match source nodes in color
        return color_dict

    def hex_to_rgba(self, hex_color, opacity=0.8):
        """Converts a hex color to RGBA string with the specified opacity."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        return f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{opacity})'

    def adjust_link_opacity(self, rgba_color, new_opacity):
        """Adjusts the opacity of an existing RGBA color string."""
        parts = rgba_color.rstrip(')').split(',')
        parts[-1] = f' {new_opacity})'
        return ','.join(parts)


    def generate_sankey_chart(self):
        # Map the source and target nodes to indices
        node_indices = {node: i for i, node in enumerate(self.all_nodes)}
        source_indices = [node_indices[f"Source: {val}"] for val in self.df[self.source_column]]
        target_indices = [node_indices[f"Target: {val}"] for val in self.df[self.target_column]]

        # Use the adjusted opacity for link colors
        opacity = 0.4  # New opacity for links
        link_colors = [self.adjust_link_opacity(self.colors[f"Source: {self.df[self.source_column].iloc[i]}"], opacity) for i in range(len(self.df))]

        # Enhancing tooltips for links
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=self.all_nodes,
                color=[self.colors.get(node, '#AAA') for node in self.all_nodes]
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=self.df[self.flow_column],
                color=link_colors
            ))])

        fig.update_layout(title_text="Sankey Diagram", font_size=10)
        fig.show()