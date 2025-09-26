import cv2
import numpy as np
import pyautogui
import os
import time
import requests

BOT_TOKEN = ""
CHAT_ID = ""
SEND_INTERVAL = 3  # seconds
last_sent_time = 0

folder = "images"

reference_images = []
for file in os.listdir(folder):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        path = os.path.join(folder, file)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        reference_images.append((file, img))

print(f"Loaded {len(reference_images)} reference images.")

def send_telegram_message(message):
    global last_sent_time
    now = time.time()
    if now - last_sent_time >= SEND_INTERVAL:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        try:
            requests.post(url, data=data)
            print(f"Sent to Telegram: {message}")
        except Exception as e:
            print(f"Error sending to Telegram: {e}")
        last_sent_time = now

while True:
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    for name, ref_img in reference_images:
        result = cv2.matchTemplate(gray, ref_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val > 0.8: 
            msg = f"Detected {name} on screen!"
            print(msg)
            send_telegram_message(msg)
            break

