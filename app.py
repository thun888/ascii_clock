import time
import os
import requests
import threading
DIGITS = {
    "0": [
        " ███ ",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    "1": [
        "  █  ",
        " ██  ",
        "  █  ",
        "  █  ",
        " ███ "
    ],
    "2": [
        " ███ ",
        "█   █",
        "  ██ ",
        " █   ",
        "█████"
    ],
    "3": [
        "████ ",
        "    █",
        " ███ ",
        "    █",
        "████ "
    ],
    "4": [
        "█  █ ",
        "█  █ ",
        "█████",
        "   █ ",
        "   █ "
    ],
    "5": [
        "█████",
        "█    ",
        "████ ",
        "    █",
        "████ "
    ],
    "6": [
        " ███ ",
        "█    ",
        "████ ",
        "█   █",
        " ███ "
    ],
    "7": [
        "█████",
        "    █",
        "   █ ",
        "  █  ",
        "  █  "
    ],
    "8": [
        " ███ ",
        "█   █",
        " ███ ",
        "█   █",
        " ███ "
    ],
    "9": [
        " ███ ",
        "█   █",
        " ████",
        "    █",
        " ███ "
    ],
    ":": [
        "     ",
        "  █  ",
        "     ",
        "  █  ",
        "     "
    ],
    "-": [
        "     ",
        "     ",
        "█████",
        "     ",
        "     "
    ],
    "N": [
        "█   █",
        "██  █",
        "█ █ █",
        "█  ██",
        "█   █"
    ],
    "O": [
        " ███ ",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    "W": [
        "█   █",
        "█   █",
        "█ █ █",
        "█ █ █",
        " █ █ "
    ],
    "X": [
        "█   █",
        " █ █ ",
        "  █  ",
        " █ █ ",
        "█   █"
    ],
    "°": [
        " ██  ",
        "█  █ ",
        " ██  ",
        "     ",
        "     "
    ],
    "C": [
        " ███ ",
        "█   █",
        "█    ",
        "█   █",
        " ███ "
    ]
}


tempture = 0
times = 0
cycle = 60


def weather_thread_proc(city: str):
    global tempture
    while True:
        try:
            search_url = f"https://weatherapi.market.xiaomi.com/wtr-v3/location/city/search?name={city}&locale=zh_cn"
            res = requests.get(search_url, timeout=10)
            city_info = res.json()[0]

            weather_url = "https://weatherapi.market.xiaomi.com/wtr-v3/weather/all"
            params = {
                "latitude": city_info["latitude"],
                "longitude": city_info["longitude"],
                "locationKey": city_info["locationKey"],
                "days": 15,
                "appKey": "weather20151024",
                "sign": "zUFJoAR2ZVrDy1vF3D07",
                "isGlobal": "false",
                "locale": "zh_cn",
                "ts": int(time.time())
            }
            res = requests.get(weather_url, params=params, timeout=10)
            tempture = str(res.json()["current"]["feelsLike"]["value"])
        except Exception as e:
            pass
        
        time.sleep(cycle)

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def render(text):
    rows = [""] * 5
    for ch in text:
        if ch == " ":
            for i in range(5): rows[i] += "     "
            continue
        pattern = DIGITS.get(ch, DIGITS["0"])
        for i in range(5):
            rows[i] += pattern[i] + "  "
    return "\n".join(rows)

if __name__ == "__main__":

    t = threading.Thread(target=weather_thread_proc, args=("番禺区",), daemon=True)
    t.start()

    try:
        while True:
            now_date = time.strftime("%Y-%m-%d")
            now_time = time.strftime("%H:%M:%S")
            # clear()
            print("\n" * 2)
            print(render(now_date))
            print("\n")
            print(render(now_time))
            print("\n")
            print(render(f"NOW: {tempture}°C"))
            print("\n"* 3)
            time.sleep(1)

    except KeyboardInterrupt:
        clear()
        print("exited.")
