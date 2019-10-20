import os

STATIC_PATH = os.path.dirname(__file__).replace("utilities", "static")

def get_static(name):
    files = [i for i in os.listdir(STATIC_PATH) if name in i]
    if files:
        return os.path.join( STATIC_PATH, files[0])
    return ""



if __name__ == '__main__':
    print(get_static("MovieDB"))