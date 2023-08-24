import requests
import random

input_sample =[37, 47, 21, 24, 14, 31, 21, 10, 14, 32, 5, 39, 50, 16, 40, 43, 30, 21, 14, 36, 47, 12, 37, 44, 43, 49, 48, 40, 14, 7]

for i in range(100_000):
    num = random.choice(input_sample)
    resp = requests.get(f"http://localhost:5000/calculate/{num}")
    if not resp.ok:
        print(f"Response not ok for iteration {i} and value {num}. Breaking...")
        break