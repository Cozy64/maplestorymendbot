import cv2
import numpy as np
import pyautogui
import os

folder = "images"

reference_images = []
for file in os.listdir(folder):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        path = os.path.join(folder, file)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        reference_images.append((file, img))

print(f"Loaded {len(reference_images)} reference images.")

while True:
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    for name, ref_img in reference_images:
        result = cv2.matchTemplate(gray, ref_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val > 0.8:  # threshold
            print(f"Detected {name} on screen!")
            break

