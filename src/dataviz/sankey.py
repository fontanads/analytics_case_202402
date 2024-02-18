"""A sankey chart for a bipartite graph showing the flow of source nodes to target nodes."""
import pandas as pd
import plotly.graph_objects as go


class SankeyChartCreator:

    def __init__(self, df: pd.DataFrame, flow_column: str, source_column: str, target_column: str):
        """Initializes the SankeyChartCreator with the input DataFrame and column names.
        """
        # dataframe schema is the following:
        # source_column | target_column | flow_column
        # dtype: str    | dtype: str    | dtype: float

        self.df = df
        self.flow_column = flow_column
        self.source_column = source_column
        self.target_column = target_column
        self.source_nodes, self.target_nodes = self.extract_unique_regions()
        self.intersection_node_values, self.all_node_values = self.extract_intersection_and_all_regions()
        self.colors = self.assign_colors()

    def extract_unique_regions(self):
        source_nodes = sorted(self.df[self.source_column].unique())
        target_nodes = sorted(self.df[self.target_column].unique())
        return source_nodes, target_nodes

    def extract_intersection_and_all_regions(self):
        intersection_node_values = sorted(list(set(self.source_nodes) & set(self.target_nodes)))
        all_node_values = sorted(list(set(self.source_nodes + self.target_nodes)))
        return intersection_node_values, all_node_values

    def assign_colors(self):
        # Assigning unique colors for intersecting node values and extra nodes on each side
        base_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        color_dict = {region: base_colors[i % len(base_colors)] for i, region in enumerate(self.intersection_node_values)}

        # Update color_dict with unique colors for non-intersecting source and target node values
        extra_colors = ['#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666', '#7570b3', '#1b9e77', '#d95f02', '#7570b3', '#1b9e77']
        unused_colors = iter(extra_colors)

        for node in self.all_node_values:
            if node not in color_dict:
                color_dict[node] = next(unused_colors)

        return color_dict

    def generate_sankey_chart(self):
        pass