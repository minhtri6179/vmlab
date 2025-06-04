from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import json
import requests
import discord


def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=en-US")

    options.add_argument("--accept-lang=en-US,en;q=0.9")
    prefs = {
        "intl.accept_languages": "en-US,en",
        "profile.default_content_setting_values.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)

    return options


webhook_url = "https://discord.com/api/webhooks/1379869557526626475/ocm_hsxOx2nNU2iQC8UHrTdCYSJiL67NjcW8Z0gQv8W1Vzd28vkJv9kSJCzaNg4S_QY3"


def send_discord_message(webhook_url, tittle, content):
    url = webhook_url

    x = {
        "embeds": [
            {
                "title": tittle,
                "color": discord.Color.blue().value,
                "description": content,
            }
        ]
    }

    response = requests.post(url, json=x)
    if response.status_code != 200:
        print(response.text)
    return response.status_code == 200


def write_match_to_csv_if_new(
    match_dict, filename="matches.csv", unique_key_fields=None
):
    hash_key = ""
    flag = True
    try:
        with open(filename, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            for k, v in loaded_data.items():
                if k == "time_ago":
                    continue
                hash_key += str(v)
    except:
        print("file read error, create new file")
        flag = False
    if flag and hash_key == unique_key_fields:
        return False
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(match_dict, f, ensure_ascii=False, indent=4)
    return True


def match_list_to_dict(data):
    return {
        "game_mode": data[0],
        "time_ago": data[1],
        "result": data[2],
        "duration": data[3],
        "level": int(data[4]),
        "kills": int(data[5]),
        "deaths": int(data[7]),
        "assists": int(data[9]),
        "kda": data[10],
        "kill_participation": data[11],
        "cs": data[12],
        "rank": data[13].title(),
        "team_left": data[14:19],
        "team_right": data[19:24],
    }


driver = webdriver.Chrome(options=get_default_chrome_options())
driver.get("https://op.gg/vi/lol/summoners/vn/Begamimi-vn2")
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@id="content-container"]/div[2]/div/div[2]/main/div/div[2]')
    )
)
x = element.text
a = x.split("\n")
result = match_list_to_dict(a)
hash_key = ""
for k, v in result.items():
    if k == "time_ago":
        continue
    hash_key += str(v)
# false la ko update, true la update
x = write_match_to_csv_if_new(result, "matches.csv", hash_key)
if x:
    send_discord_message(
        webhook_url,
        f"lol ccc vừa {result['result']}",
        f"đánh {result['game_mode']}   {result['kills']}/{result['deaths']}/{result['assists']}",
    )
driver.quit()
