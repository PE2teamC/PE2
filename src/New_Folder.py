import os
from datetime import datetime

now = datetime.now()

def NewFolder(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError:
        print('Error : Creating Directory '+path)
