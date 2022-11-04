import requests
import datetime
import os

import pandas as pd
import numpy as np

from dotenv import load_dotenv
load_dotenv()


# URLS
dict_of_urls = {
    '1D': {
        'fastapi_1D': 'https://172.16.5.30:8443/fastapi_aires/color1D',
        'flask_1D'  : 'https://172.16.5.30:8443/flask_aires/color1D',
        'node_1D'   : 'https://172.16.5.30:8443/node_aires/color1D',
    }, 
    '2D': {
        'fastapi_2D': 'https://172.16.5.30:8443/fastapi_aires/color2D',
        'flask_2D'  : 'https://172.16.5.30:8443/flask_aires/color2D',
        'node_2D'   : 'https://172.16.5.30:8443/node_aires/color2D'
    }
}

# LIST OF FILES FOR BENCHMARK
path_to_dataset = str( os.environ.get('BENCHMARK_FILES_FOLDER') )
list_of_files = []
for root, folders, files in os.walk(path_to_dataset):
    for file in files:
        if (
                os.path.isfile( os.path.join(path_to_dataset,file) ) 
                and file.split('.')[-1]=='h5'
        ):
            list_of_files.append(
                os.path.join(path_to_dataset,file)
            )
            

# UTILS FUNCTION
def contact_api(api_url, file_to_send):
    print(f"Analysing {file_to_send.split('/')[-1]} to {api_url}")
    file_size = os.path.getsize(file_to_send)
    print(f'File size: {file_size} bytes')
    opened_file = open(file_to_send, 'rb')
    files = {'file': opened_file} 
    
    starting_time = datetime.datetime.now()
    r = requests.post(api_url, files=files, verify=False)
    total_time = datetime.datetime.now() - starting_time
    
    print(f'It tooks {total_time} ms to get the reply from {api_url} with a file of size {file_size} bytes;')
    
    return total_time, file_size

def benchmark_api(path_to_store_csv):
    starting_time_total = datetime.datetime.now()

    df_results = pd.DataFrame(
        columns = ['size'] + list(dict_of_urls['1D'].keys() ) + list( dict_of_urls['2D'].keys()  ),
        index = [file.split('/')[-1].split('.')[0] for file in list_of_files ]
    )

    for branch in dict_of_urls.keys():
        starting_time_branch = datetime.datetime.now()
        print(f'Analysing {branch} branch;\n\n')
        for api in dict_of_urls[branch]:
            starting_time_api = datetime.datetime.now()
            print(f'Analysing {api} {branch}')
            for file in list_of_files:
                filename = file.split('/')[-1].split('.')[0]

                total_time, file_size = contact_api(
                    dict_of_urls[branch][api],
                    file
                )

                df_results['size'].loc[filename] = file_size
                df_results[api].loc[filename]  = total_time

                df_results.to_csv(path_to_store_csv)

            print(f'Analysis of {api} {branch} done in {datetime.datetime.now() - starting_time_api}\n\n')
        print(f'Analysis of {branch} branch done in {datetime.datetime.now() - starting_time_branch};\n\n')
    print(f'Total benchmarking done in {datetime.datetime.now() - starting_time_total}')

# RUN
if __name__ == "__main__":
    path_to_store_csv = str( os.environ.get('BENCHMARK_RESULTS_FOLDER') )
    benchmark_api(path_to_store_csv)