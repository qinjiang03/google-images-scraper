import os
import json
import shutil
import requests
import urllib
import posixpath


IMAGES_DIR = './data/images'
RESULTS_DIR = './data/results'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}

def get_file_type(image_url):
    path = urllib.parse.urlsplit(image_url).path
    filename = posixpath.basename(path).split('?')[0]
    file_type = filename.split('.')[-1]
    if file_type.lower() not in ['jpe', 'jpeg', 'jfif', 'exif', 'tiff', 'gif', 'bmp', 'png', 'webp', 'jpg']:
        file_type = 'jpg'
    return file_type


for result_file in os.listdir(RESULTS_DIR):
    class_name = result_file.replace('.json', '')
    out_dir = os.path.join(IMAGES_DIR, class_name)
    os.makedirs(out_dir, exist_ok=True)

    print(f'>> Downloading images for {class_name}...')
    result_file_path = os.path.join(RESULTS_DIR, result_file)
    result = json.load(open(result_file_path, 'r', encoding='utf-8'))

    for i, image in enumerate(result['images_results']):
        image_url = image['original']
        file_type = get_file_type(image_url)
        file_path = os.path.join(out_dir, '{}_g{}.{}'.format(class_name, str(i+1).zfill(3), file_type))
        if os.path.exists(file_path):
            print(f'  >> Skipping since {file_path} exists...')
            continue

        try:
            print(f'  >> Downloading image #{i+1} from {image_url}')
            response = requests.get(image_url, headers=headers, stream=True, timeout=60)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
        except Exception as e:
            print()
            print(f'  !! Error downloading image from {image_url}')
            print(e)
            print()