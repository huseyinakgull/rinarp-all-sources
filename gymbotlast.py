import cv2
import pygetwindow as gw
import pyautogui
import numpy as np
import requests
import uuid
import time
import socket
import platform
import dxcam
import json
import os
from datetime import datetime

def get_username():
    if os.name == 'nt':
        return os.getlogin()
    else:
        import pwd
        return pwd.getpwuid(os.getuid()).pw_name
    
class LicenseManager:
    def __init__(self):
        self.allowed_macs = self.get_allowed_macs_from_web()

    def get_mac_address(self):
        mac = ':'.join(("%012X" % uuid.getnode())[i:i + 2] for i in range(0, 12, 2))
        return mac

    def get_allowed_macs_from_web(self):
        try:
            url = "https://raw.githubusercontent.com/thatshussain/USBReview-Infos/main/all-validations1.json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get("allowed_macs", [])
            else:
                print(f"Web sitesine bağlanırken hata oluştu: {response.status_code}")
                return []
        except Exception as e:
            print(f"Web sitesine bağlanırken hata oluştu: {e}")
            return []

    def is_valid_user(self):
        current_mac = self.get_mac_address()
        return current_mac in self.allowed_macs

def send_discord_webhook(title, content, renk):
    webhook_url = "webhook gir."
    data = {
        "username": "quecy gym bot.",
        "avatar_url": "https://i.pinimg.com/564x/48/21/86/4821866c230995536516f4b3b8210913.jpg",
        "embeds": [
            {
                "title": title,
                "description": content,
                "color": renk
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print(f"Discord webhook error: {response.text}")

def send_screenshot_to_discord_webhook(webhook_url: str):
    screenshot = pyautogui.screenshot()
    screenshot_path = "C:screenshot.png"
    screenshot.save(screenshot_path)
    screenshot.close()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        payload = {
            "file": open(screenshot_path, "rb")
        }
        response = requests.post(webhook_url, files=payload)
        response.raise_for_status()
        
        print("[+] Kontroller tamamlandı.")
    except requests.exceptions.RequestException as e:
        print("[!] Hata Kodu: #002 (Ticket üzerinden bildiriniz.)")
        pass


def get_open_windows():
    windows = gw.getAllTitles()
    return [w for w in windows if w.strip()]

license_manager = LicenseManager()
if not license_manager.is_valid_user():
    username = get_username()
    log_content = f"**MAC Adresi:** {license_manager.get_mac_address()}\n**Kullanıcı Adı:** {platform.node()}\n**Bilgisayar Adı:** {username}\n**Tarih ve Saat:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n**IP Adresi:** {socket.gethostbyname(socket.gethostname())}"
    open_windows = get_open_windows()
    log_content += f"\n**Açık Sekmeler:** {', '.join(open_windows)}"
    print("[!] Herhangi bir lisansınız bulunmuyor, lütfen ticket oluşturunuz.")
    send_discord_webhook(":octagonal_sign: Giriş Başarısız", log_content, 15158332)
    send_screenshot_to_discord_webhook("webhook")
    screenshot_path = "screenshot.png"
    os.remove(screenshot_path)
    time.sleep(5)
    exit()

username = get_username()
log_content = f"**MAC Adresi:** {license_manager.get_mac_address()}\n**Kullanıcı Adı:** {platform.node()}\n**Bilgisayar Adı:** {username}\n**Tarih ve Saat:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n**IP Adresi:** {socket.gethostbyname(socket.gethostname())}"
open_windows = get_open_windows()
log_content += f"\n**Açık Sekmeler:** {', '.join(open_windows)}"
send_discord_webhook(":white_check_mark: Giriş Başarılı", log_content, 3066993)
send_screenshot_to_discord_webhook("wh")
screenshot_path = "screenshot.png"
os.remove(screenshot_path)
print("[+] Lisansın doğrulandı! Giriş yapıyorsun, lütfen bekle.")
time.sleep(5)
target_window_title = None
windows = [w for w in gw.getAllTitles() if w.strip()]
print("[?] Aşağıda bulunan liste üzerinden oyun sekmesinin numarasını giriniz.")
for idx, window_title in enumerate(windows, start=2):
    print(f" ({idx}) '{window_title}'")
try:
    selected_idx = int(input("[=] Hedef Oyuna Ait Numara: "))
    if 1 <= selected_idx <= len(windows) + 1:
        if selected_idx == 1:
            print("[+] Pencere numarası olarak '1' seçtiniz.")
        else:
            target_window_title = windows[selected_idx - 2]
            print(f"[+] '{target_window_title}' başarıyla seçildi.")
    else:
        print("[-] Geçersiz pencere numarası.")
except ValueError:
    print("[-] Geçersiz giriş. Lütfen sadece numara girin.")
target_window = gw.getWindowsWithTitle(target_window_title)

camera = dxcam.create()
cv2.namedWindow("product by huseyin.")
def is_object_in_area(x1, y1, x2, y2, area):
    result = cv2.pointPolygonTest(np.array(area, np.int32), (int(x1+((x2-x1)/2)), int(y1+(y2-y1))), False)
    return result >= 0

dizim =[]
a = time.time()
i = 0
time.sleep(2)
area = []
ff = 0
cameraac = True
baslat = time.time()
while True:
        try:
            window = pyautogui.getWindowsWithTitle(target_window_title)
            if window or window[0].isActive:
                if cameraac:
                    window = window[0]
                    left, top, width, height = window.left, window.top, window.width, window.height
                    left,top,width,height = 325, 352, 520, 30
                    if height > 1080:
                        height = 1080
                    if width > 1920:
                        width = 1920
                    if top < 0:
                        top = 0
                    if left < 0:
                        left = 0
                    if cameraac:
                        camera.start(target_fps=60,region=(left, top, left + width, top + height))
                        cameraac = False
                        i += 1
                else:
                    start = time.time()
                    screenshot = camera.get_latest_frame()
                    screenshot = np.array(screenshot)
                    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
                    screenshot[screenshot[:,:,1]<130] = [0,0,0]
                    white_mask = np.logical_and.reduce((screenshot[:, :, 0] > 90, screenshot[:, :, 1] > 90, screenshot[:, :, 2] > 125))
                    screenshot[white_mask] = [255, 255, 255]
                    mask = np.logical_and(screenshot[:, :, 1] > 100, screenshot[:, :, 1] < 156)
                    screenshot[mask] = [0, 255, 0]
                    screenshot[screenshot[:, :, 0]>100] = [255,255,255]
                    screenshot[screenshot[:, :, 2]>156] = [255,255,255]
                    if area == [] and time.time()-baslat > 2:
                        baslat = time.time()
                        try:
                            lower_white = np.array([200, 200, 200])
                            upper_white = np.array([255, 255, 255])
                            white_mask = cv2.inRange(screenshot, lower_white, upper_white)
                            contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                            for contour in contours:
                                ax, ay, aw, ah = cv2.boundingRect(contour)
                                if ax <501:
                                    area = [(ax-2, ay), (ax + aw, ay), (ax+2 + aw, ay + ah), (ax, ay + ah)]
                                    break
                                elif ax > 501 and ax < 678:
                                    if ax > 500 and ax < 550:
                                        area = [(ax-4, ay), (ax + aw, ay), (ax+4 + aw, ay + ah), (ax, ay + ah)]
                                    elif ax >= 550 and ax < 600:
                                        area = [(ax-5, ay), (ax + aw, ay), (ax+5 + aw, ay + ah), (ax, ay + ah)] 
                                    else:
                                        area = [(ax-4, ay), (ax + aw, ay), (ax+4 + aw, ay + ah), (ax, ay + ah)]
                                    break
                                else:
                                    area = [(ax-2, ay), (ax + aw, ay), (ax+2 + aw, ay + ah), (ax, ay + ah)]
                                    break
                        except:
                            continue
                    try:
                        if area != [] and time.time()-baslat > 1:
                            cv2.rectangle(screenshot, (ax-5, ay), (ax +5+ aw, ay + ah), (0, 0, 255), 1)
                            lower_green = np.array([0, 200, 0])
                            upper_green = np.array([50, 255, 50])
                            green_mask = cv2.inRange(screenshot, lower_green, upper_green)
                            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                            for contour in contours:
                                x, y, w, h = cv2.boundingRect(contour)
                                yx1, yy1, yx2, yy2 = x, y, x + w, y + h
                                if is_object_in_area(x, y, x + w, y + h, area):
                                    baslat = time.time()
                                    cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 0, 255), 3)
                                    area = []
                                    pyautogui.press("space")
                                    ff += 1
                                    break
                    except:
                        pass
                    cv2.putText(screenshot, f"{ff}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow("product by huseyin.", screenshot)
                    if cv2.waitKey(1) == ord('q'):
                        break
        except:
            time.sleep(0.5)
            continue



print(time.time()-a)
print(i)
    
camera.stop()
