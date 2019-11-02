import os, requests, shutil

def get_files(folder_path):
    return [os.path.join(folder_path, i) for i in os.listdir(folder_path) if i.lower().endswith(".mkv")]

def download_image(url, destination):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(destination, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return destination

    return False

if __name__ == '__main__':
    download_image(
        "https://image.tmdb.org/t/p/w300//lZpWprJqbIFpEV5uoHfoK0KCnTW.jpg",
        r"E:\_PythonSuli\Desktop_App_1019\movies\test.jpg"
    )