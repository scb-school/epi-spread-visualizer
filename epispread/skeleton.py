import pandas as pd
import geopandas as gpd
import country_converter as coco
import matplotlib.pyplot as plt
 
FILE_1 = "./time_series_covid19_confirmed_global.csv"
FILE_2 = "./WHO-COVID-19-global-data.csv"

COUNTRY_LOOKUP = {""}

#matches names of column 2 to be those of column 1
def iso2_to_iso3(iso2_codes):
    return coco.convert(names = iso2_codes, to='ISO3')

def main():
    df = pd.read_csv(
        FILE_2, delimiter=",")
    
    proof_of_concept = df.loc[df['Date_reported'] == '2021-10-01']
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    iso3_codes = iso2_to_iso3(proof_of_concept['Country_code'])
    proof_of_concept.loc[:,'Country_code_iso3'] = iso3_codes

    proof_of_concept.to_csv(r'./poc_country.csv')
    
    world['iso_a3'].to_csv(r'./world.csv')
    
    merge = pd.merge(left=world, right=proof_of_concept, left_on='iso_a3', right_on='Country_code_iso3', how='left')
    
    #disease.plot()
    merge.plot(column = 'Cumulative_cases', legend='True')
    plt.show()

if __name__ == "__main__":
    main()