import time
from random import randint

from tqdm import tqdm

time_wait = [i for i in range(0, randint(100, 160))]


def daley_press(text):
    print(text)
    for _ in tqdm(time_wait):
        time.sleep(1)
