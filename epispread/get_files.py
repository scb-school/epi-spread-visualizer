import requests
import os

def get_files():
    """
    This function grabs 4 specified URLs from https://covid19.who.int/data and stores them as CSV files in data_files/[file_name]
    Returns 1 if failure, 0 if success
    """
    urls = ['https://covid19.who.int/WHO-COVID-19-global-data.csv', 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv', 'https://covid19.who.int/who-data/vaccination-data.csv', 'https://covid19.who.int/who-data/vaccination-metadata.csv']

    file_names = []

    for url in urls:
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:
            file_name = url.split('/')[-1].replace(".csv", "")
            file_names.append(file_name)
            if not os.path.exists("data_files"):
                os.makedirs("data_files")
            open('data_files/' + file_name + '.csv', 'wb').write(r.content)
        
    return file_names
        
