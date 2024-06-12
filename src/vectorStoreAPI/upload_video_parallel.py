import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define the directory containing the .mp4 files
directory_path = './data/compressed_index'

# Define the API endpoint
api_url = 'http://127.0.0.1:8000/sync/ingestion/upload_and_index_video'

def upload_video(file_path, filename):
    # Open the file in binary mode
    with open(file_path, 'rb') as video_file:
        # Prepare the files and headers for the request
        files = {'video': (filename, video_file, 'video/mp4')}
        headers = {
            'accept': 'application/json',
        }

        # Send the POST request
        response = requests.post(api_url, headers=headers, files=files)
        
        # Return the response from the server
        return filename, response.status_code, response.text

def main():
    # List all .mp4 files in the directory
    video_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4')]
    
    # Use ThreadPoolExecutor to parallelize the upload tasks
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks to the executor
        futures = {executor.submit(upload_video, os.path.join(directory_path, filename), filename): filename for filename in video_files}
        
        # Use tqdm to display progress
        for future in tqdm(as_completed(futures), total=len(video_files)):
            filename = futures[future]
            try:
                filename, status_code, response_text = future.result()
                print(f'Uploaded {filename}: {status_code} - {response_text}')
            except Exception as e:
                print(f'Error uploading {filename}: {e}')

if __name__ == "__main__":
    main()