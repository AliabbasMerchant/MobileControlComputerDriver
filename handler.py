from typing import Optional
import pyautogui
import json

pyautogui.FAILSAFE = False

def handle(request: dict) -> Optional[str]:
    print(request['signal'], request['action'])
    if request['action'] == 'type':
        pyautogui.press(request['signal'])
    elif request['action'] == 'mouse':
        signal = json.loads(request['signal'])
        x = signal['x']
        y = signal['y']
        w = signal['w']
        h = signal['h']
        W, H = pyautogui.size()
        x = x * W / w
        y = y * H / h
        print(x, y)
        pyautogui.moveTo(x, y)
    return None
