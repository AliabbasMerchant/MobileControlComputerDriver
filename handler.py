from typing import Optional
import pyautogui


def handle(request: dict) -> Optional[str]:
    pyautogui.press(request['signal'])
    return None
