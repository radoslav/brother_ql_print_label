from app import app

import time

def print_task():
    time.sleep(5)

    raise NameError('HiThere')
    return True