import os
import requests
from tqdm import tqdm

# Define the directory containing the .mp4 files
directory_path = './data/compressed_index'

# Define the API endpoint
api_url = 'http://127.0.0.1:8000/sync/ingestion/upload_and_index_video'

# Iterate over all files in the directory
for filename in tqdm(os.listdir(directory_path)):
    # Check if the file is an .mp4 file
    if filename.endswith('.mp4'):
        file_path = os.path.join(directory_path, filename)
        
        # Open the file in binary mode
        with open(file_path, 'rb') as video_file:
            # Prepare the files and headers for the request
            files = {'video': (filename, video_file, 'video/mp4')}
            headers = {
                'accept': 'application/json',
            }
            
            # Send the POST request
            response = requests.post(api_url, headers=headers, files=files)
            
            # Print the response from the server
            print(f'Uploaded {filename}: {response.status_code} - {response.text}')