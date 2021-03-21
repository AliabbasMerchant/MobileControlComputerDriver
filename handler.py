from typing import Optional
import pyautogui
import json

pyautogui.FAILSAFE = False

def handle(request: dict) -> Optional[str]:
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
        pyautogui.moveTo(x, y)
    elif request['action'] == 'click':
        pyautogui.click(button=request['signal'])
    return None
