import os

def get_files(folder_path):
    return [os.path.join(folder_path, i) for i in os.listdir(folder_path) if i.lower().endswith(".mkv")]