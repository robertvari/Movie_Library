import os

def get_files():
    folder_path = "E:/_PythonSuli/Desktop_App_1019/movies"

    return [os.path.join(folder_path, i) for i in os.listdir(folder_path)]