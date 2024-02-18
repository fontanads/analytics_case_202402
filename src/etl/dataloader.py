import pandas as pd
from utils.rest_country import CountrySuperRegionMapper


class DataLoader:

    def __init__(self) -> None:
        pass

    def load_data_xlsx_from_tab(self, path: str, sheet_name: str) -> pd.DataFrame:
        """Reads a xlsx from a specific sheet given the path and sheet name.
        Returns a Pandas DataFrame.
        """
        return pd.read_excel(path, sheet_name=sheet_name)


class DataTransformer:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy()

    def transform_data(
            self, 
            fill_super_region=True, 
            drop_post_book=True, 
            map_property_to_super_region=True
        ) -> pd.DataFrame:

        if fill_super_region:
            self.fill_na_super_region()

        if drop_post_book:
            self.drop_post_book()
        self.split_week_col_into_date_cols()

        if map_property_to_super_region:
            self.map_property_countries_to_super_regions()

        self.reorder_and_rename_columns()
        return self.df

    def fill_na_super_region(self) -> None:
        # fill na column of Super Region with "North America"
        self.df['Super Region'] = self.df['Super Region'].fillna('North America')

    def drop_post_book(self) -> None:
        # drop rows where "Booking Window Group" is "Post Book"
        self.df = self.df[self.df['Booking Window Group'] != 'Post Book']
    
    def split_week_col_into_date_cols(self) -> None:
        # week col follows the format "YYYY-WXX" where XX is the week number (double digit not guaranteed)
        self.df['Year'] = self.df['Week'].str.split('-').str[0]
        self.df['Week'] = self.df['Week'].str.split('-').str[1].str.replace('W', '')
        self.df['Week'] = self.df['Week'].astype(int)
        # below, we create a new column "Date" with the date corresponding to the first day of the week (on Monday)s
        # we use the ISO 8601 format for the week number and day of the week
        # %G is the year in the ISO 8601 format, %V is the week number in the ISO 8601 format, and %u is the day of the week
        self.df['Date'] = pd.to_datetime(self.df['Year'].astype(str) + self.df['Week'].astype(str) + '-1', format='%G%V-%u')

    def map_property_countries_to_super_regions(self) -> pd.DataFrame:
        # map countries to super regions
        country_mapper = CountrySuperRegionMapper()
        unique_mapping, mapped_series = country_mapper.map_countries_to_super_regions(self.df['Property Country'])
        self.df['Property Super Region'] = mapped_series
        return self.df
    
    def reorder_and_rename_columns(self) -> None:
        # output columns order
        cols_order = [
            'Super Region',
            'Country Name',
            'Platform Type Name',
            'Mobile Indicator Name',
            'Property Super Region',
            'Property Country',
            'Booking Window Group',
            'Date',
            'Year',
            'Week',
            'Net Gross Booking Value USD',
            'Net Orders']
        
        # rename columns simplifying the names with the following mapping dictionary
        cols_mapping = {
            'Super Region': 'client_region',
            'Country Name': 'client_country',
            'Platform Type Name': 'platform',
            'Mobile Indicator Name': 'mobile',
            'Property Super Region': 'property_region',
            'Property Country': 'property_country',
            'Booking Window Group': 'booking_window',
            'Date': 'date',
            'Year': 'year',
            'Week': 'week',
            'Net Gross Booking Value USD': 'net_gross_booking_usd',
            'Net Orders': 'net_orders'
        }

        self.df = self.df[cols_order].rename(columns=cols_mapping)
