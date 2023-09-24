import cfscrape
import re
import random
import string
import os
from dotenv import load_dotenv
import threading
import json

def random_str(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

with open('countries.json', 'r') as file:
    data = json.load(file)

countries = data['countries']
load_dotenv()
success_accs = 0
domain = os.getenv("DOMAIN")

def register_account(thread_id):
    while True:
        scraper = cfscrape.create_scraper()

        url = f"https://{domain}/register/info"

        response = scraper.get(url)

        html = response.text

        pattern = r'name="_token" value="(.+?)"'
        match = re.search(pattern, html)
        if match:
            token = match.group(1)
            print(f"Поток {thread_id}: {token}")
        else:
            print(f"Поток {thread_id}: Не удалось найти _token")

        data = {
            "_token": token,
            "email": f"{random_str(10)}@zenettany.life",
            "password": "",
            "Username": f"{random_str(10)}",
            "country": random.choice(countries),
            "birthdate": "",
            "game": "dota2",
            "agreement": "false"
        }

        response = scraper.post(f"https://{domain}/register/complete", data=data)

        if response.status_code == 200:
            print(f"Поток {thread_id}: Регистрация прошла успешно")
            global success_accs
            success_accs += 1
            print(f"Успешных аккаунтов: {success_accs}")
        else:
            print(f"Поток {thread_id}: Регистрация не удалась")

threads = []

for i in range(20):
    thread = threading.Thread(target=register_account, args=(i,))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
