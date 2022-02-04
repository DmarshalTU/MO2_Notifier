import pyautogui
import os
import requests
import json
from win10toast import ToastNotifier
import time
import requests
import json
from gtts import gTTS
import win32com.client


PATH = '/Users/Home/Desktop/code/TestMO2'
ID = f'{PATH}/1.jpeg'
API = 'K81039540788957'
LANG = 'en'


def ocr_space_file(filename, overlay=False, api_key=API, language='eng'):

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    m = r.content.decode()
    jsonstr = json.loads(m)
    txt = jsonstr["ParsedResults"][0]["ParsedText"]
    q = [int(s) for s in txt.split() if s.isdigit()]
    w = q[0]
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(f'Your position is {str(w)}')
    if(w == 10):
        noty(str(w))
        speaker.Speak(f'Attention! {str(w)} left!')
    

def noty(msg):
    toaster = ToastNotifier()
    toaster.show_toast("MO2",
                       f'Position in que: {msg}',
                       duration=10)
    while toaster.notification_active(): time.sleep(0.1)

while True:
    try:

        isExist = os.path.exists(PATH)

        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(ID)
        try:
            ocr_space_file(filename=ID, language='eng')
            time.sleep(50)
            continue
        except Exception as e:
            print(e)

    except FileNotFoundError as e:
        print(e)
        os.makedirs(PATH)
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(ID)
        try:
            ocr_space_file(filename=ID, language='eng')
            time.sleep(50)
            continue
        except Exception as e:
            print(e)
