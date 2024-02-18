import pandas as pd
from utils.rest_country import CountrySuperRegionMapper


class DataTransformer:

    # columns order for raw dataset columns + extra super region
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
        'Net Orders'
    ]

    # mapping dictionary to rename columns
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

    # dtypes of the renamed columns (category as type "string")
    cols_dtype = {
        'client_region': 'string',
        'client_country': 'string',
        'platform': 'string',
        'mobile': 'string',
        'property_region': 'string',
        'property_country': 'string',
        'booking_window': 'string',
        'date': 'datetime64[ns]',
        'year': 'int',
        'week': 'int',
        'net_gross_booking_usd': 'float',
        'net_orders': 'int'
    }    

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy()

    def transform_data(
            self,
            fill_super_region=True,
            drop_post_book=True,
            map_property_to_super_region=True,
            replace_us_client_country=True,
            treat_apac_2022w45_outlier=True
    ) -> pd.DataFrame:

        self.split_week_col_into_date_cols()

        if fill_super_region:
            self.fill_na_super_region()

        if replace_us_client_country:
            self.replace_us_client_country()

        if treat_apac_2022w45_outlier:
            self.treat_apac_2022w45_outlier()

        if drop_post_book:
            self.drop_post_book()

        if map_property_to_super_region:
            self.map_property_countries_to_super_regions()

        self.reorder_and_rename_columns()
        self.apply_dtypes()

        return self.df

    def fill_na_super_region(self) -> None:
        # fill na column of Super Region with "North America"
        self.df['Super Region'] = self.df['Super Region'].fillna('North America')

    def drop_post_book(self) -> None:
        # drop rows where "Booking Window Group" is "Post Book"
        self.df = self.df[self.df['Booking Window Group'] != 'Post Book']

    def split_week_col_into_date_cols(self) -> None:
        # week col follows the format "YYYY-WXX" where XX is the week number (double digit not guaranteed)
        self.df['Year'] = self.df['Week'].str.split('-').str[0].astype(int)
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

        self.df = self.df[self.cols_order].rename(columns=self.cols_mapping)

    def treat_apac_2022w45_outlier(self):
        # filter for:
        # Super Region: APAC
        # Country Name: Australia
        # Property Country: Australia
        # Week: 45
        # Year: 2022
        # Platform Type Name: Mobile App
        # and divide "Net Gross Booking Value USD" by 100
        # using raw column names before renaming

        mask = pd.Series([True] * len(self.df), index=self.df.index)
        mask &= self.df['Super Region'] == 'APAC'
        mask &= self.df['Country Name'] == 'Australia'
        mask &= self.df['Property Country'] == 'Australia'
        mask &= self.df['Platform Type Name'] == 'Mobile App'
        mask &= self.df['Week'] == 45
        mask &= self.df['Year'] == 2022

        self.df.loc[mask, 'Net Gross Booking Value USD'] = self.df.loc[mask, 'Net Gross Booking Value USD'] / 100

    def replace_us_client_country(self):
        self.df["Country Name"] = self.df["Country Name"].replace({"US": "United States of America"})

    def apply_dtypes(self) -> None:
        self.df = self.df.astype(self.cols_dtype)
        return self.df