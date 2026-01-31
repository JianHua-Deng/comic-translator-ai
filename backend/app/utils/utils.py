import requests
import os

def download_models(url, dest_path):
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    print(f"Downloading Lama Manga InPainter model from: {url}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
            
            print("Finished Downloading InPainter Model")
    
    except Exception as e:

        if os.path.exists(dest_path):
            os.remove(dest_path)
        raise e
