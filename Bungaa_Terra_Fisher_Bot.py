# from pynput import mouse, keyboard
from Bungaa_Terra_utils import get_terraria_window, background_click, get_background_sreenshot, get_window_pos_mouse, get_cropped_screenshot, mean_squared_error
from time import sleep
import cv2
import sys

class main_programm():
    
    def __init__(self):
        self.quit_flag = False
        get_terraria_window()
        self.throw_point = None
        self.float_point = None
        border_len = 10
        # self.hotkey_interruptor()
        # self.start_mouse_listener()
        # self.wait_until_cords()
        # self.start_fisher(border_len)
        while True:
            background_click(900, 600)
            sleep(0.5)
        
    def start_fisher(self, border_len):
        float_x, float_y = self.float_point
        throw_x, throw_y = self.throw_point
        fish_counter = 0
        sleep(2)
        old_screenshot = get_cropped_screenshot(float_x, float_y, border_len)
        max_error = 0
        
        while True:
            if self.quit_flag:
                sys.exit()
            current_screenshot = get_cropped_screenshot(float_x, float_y, border_len)
            error, diff = mean_squared_error(old_screenshot, current_screenshot)
            # print("Image matching Error between the two images:",error)
            if error > max_error:
                max_error = error
                print(f"max error = {max_error}")
            if error > 39.1:
                if error > 65.0:
                    print("Началась кровавая луна.")
                    sleep(540)
                    continue
                
                fish_counter += 1
                print(f'fish! №{fish_counter}')
                background_click(float_x, float_y)
                sleep(0.2)
                background_click(throw_x, throw_y)
                sleep(1.5)
            sleep(0.2)
            old_screenshot = current_screenshot
            
            
            
        
    def wait_until_cords(self):
        while True:
            if self.throw_point and self.float_point:
                return
            elif self.quit_flag:
                sys.exit()
            print('waiting for cords')
            sleep(0.5)
        
        
    def on_mouse_press(self, mouse_x, mouse_y, button, pressed):
        print(f"call_button = {button}")
        if button == mouse.Button.left:
            self.throw_point = get_window_pos_mouse(mouse_x, mouse_y)
            print("left")
            if self.float_point:
                return False
        elif button == mouse.Button.right:
            self.float_point = get_window_pos_mouse(mouse_x, mouse_y)
            print('right')
            if self.throw_point:
                return False
            
    def on_keyboard_press(self, mouse_x, mouse_y, button, pressed):
        print(f"call_button = {button}")
        if button == mouse.Button.left:
            self.throw_point = get_window_pos_mouse(mouse_x, mouse_y)
            print("left")
            if self.float_point:
                return False
        elif button == mouse.Button.right:
            self.float_point = get_window_pos_mouse(mouse_x, mouse_y)
            print('right')
            if self.throw_point:
                return False
        
    def start_mouse_listener(self):
        mlistener = mouse.Listener(on_click=self.on_mouse_press)
        mlistener.start()
        
    def set_quit_flag(self):
        self.quit_flag = True
        
    def hotkey_interruptor(self):
        klistener = keyboard.GlobalHotKeys({'<ctrl>+q': self.set_quit_flag})
        klistener.start()
            
            
if __name__ == "__main__":
    main = main_programm
    main()