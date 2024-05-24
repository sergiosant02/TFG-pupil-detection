import pyautogui


class MouseControl:

    def __init__(self):
        print("Mouse started")
        print("current mouse size:", pyautogui.size())

    def get_current_position(self):
        return [pyautogui.position().x, pyautogui.position().y]
    
    def relative_move(self, direction):
        pyautogui.FAILSAFE = False
        print("pres position:", pyautogui.position())
        pyautogui.moveRel(direction[0], direction[1])
        print("pos position:", pyautogui.position())

    def absolute_move(swelf, point):
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(point[0], point[1])

    def double_click(self):
        print("-----double click----")
        pyautogui.doubleClick()
    
    def click(self):
        print("----- click----")
        pyautogui.click()

    def right_click(self):
        print("-----right click----")
        pyautogui.rightClick()