
import pandas as pd


import zipfile
import requests 

def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

data = 'energy'

if data == 'air_quality':
    file_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00360/AirQualityUCI.zip'
    download_url(url=file_url, save_path='AirQualityUCI', chunk_size=128)
    path_to_zip_file = 'AirQualityUCI'
    directory_to_extract_to = 'temp_dir'
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
    df = pd.read_csv('temp_dir/AirQualityUCI.csv', sep=';')
    print(df.head())

elif data == 'energy':
    file_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00374/energydata_complete.csv'
    df = pd.read_csv(file_url)
    print(df.head())