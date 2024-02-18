import pandas as pd


class DataLoader:

    def __init__(self) -> None:
        pass

    def load_data_xlsx_from_tab(self, path: str, sheet_name: str) -> pd.DataFrame:
        """Reads a xlsx from a specific sheet given the path and sheet name.
        Returns a Pandas DataFrame.
        """
        return pd.read_excel(path, sheet_name=sheet_name)

