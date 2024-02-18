"""Class to map countries to super regions. Generated with ChatGPT Prompting"""
import pandas as pd
import requests

class CountrySuperRegionMapper:
    API_ENDPOINT = "https://restcountries.com/v3.1/all"

    def __init__(self):
        self.country_data = self.fetch_country_data()
        self.super_region_map = self.prepare_super_region_map()

    def fetch_country_data(self):
        try:
            response = requests.get(self.API_ENDPOINT)
            response.raise_for_status()  # Raises an exception for HTTP errors
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []

    def prepare_super_region_map(self):
        super_region_map = {}
        for country in self.country_data:
            name = country.get('name', {}).get('common', 'Unknown Country').lower()
            region = country.get('region', '')
            subregion = country.get('subregion', '')

            if region == 'Europe' or subregion == 'Northern Africa':
                super_region = 'EMEA'
            elif region == 'Asia' or (region == 'Oceania' and subregion != 'Australia and New Zealand'):
                super_region = 'APAC'
            elif region == 'Americas':
                if subregion in ['South America', 'Central America', 'Caribbean']:
                    super_region = 'LATAM'
                else:
                    super_region = 'NA'  # North America
            elif region == 'Africa':
                super_region = 'Sub-Saharan Africa'
            else:
                super_region = 'Other'

            super_region_map[name] = super_region
        return super_region_map

    def map_countries_to_super_regions(self, countries):
        if isinstance(countries, pd.Series):
            unique_countries = countries.unique()
            input_type = 'series'
        elif isinstance(countries, list):
            unique_countries = list(set(countries))
            input_type = 'list'
        else:
            raise ValueError("Input must be a list or Pandas Series.")

        unique_mapping = {country: self.super_region_map.get(country.lower(), 'Unknown Country') for country in unique_countries}

        if input_type == 'list':
            mapped_list = [unique_mapping[country] for country in countries]
            return unique_mapping, mapped_list
        elif input_type == 'series':
            # Directly replace country names with their super regions using the unique_mapping
            mapped_series = countries.replace(unique_mapping)
            return unique_mapping, mapped_series


# Example usage
if __name__ == "__main__":
    mapper = CountrySuperRegionMapper()

    countries_list = ['France', 'Brazil', 'Narnia', 'France']
    countries_series = pd.Series(['India', 'China', 'Atlantis', 'India'])

    unique_map_list, mapped_list = mapper.map_countries_to_super_regions(countries_list)
    unique_map_series, mapped_series = mapper.map_countries_to_super_regions(countries_series)

    print("List - Unique Map:", unique_map_list)
    print("List - Mapped List:", mapped_list)
    print("Series - Unique Map:", unique_map_series)
    print("Series - Mapped Series:", mapped_series, sep='\n')
