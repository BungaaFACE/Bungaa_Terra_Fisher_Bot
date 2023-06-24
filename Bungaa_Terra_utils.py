import win32.win32api as win32api
import win32.win32gui as win32gui
import pythonwin.win32ui as win32ui
import win32.lib.win32con as win32con
from ctypes import windll
import numpy as np
import cv2
from time import sleep


def get_terraria_window():
    """
    Функция для получения окна
    Окно необходимо для дальнейшей работы с ним
    """
    
    def handle_windows(hwnd, _):
        """
        Функция для нахождения нужного окна из списка всех окон
        """
        all_win.append(hwnd)
        if "Terraria: " in win32gui.GetWindowText(hwnd):
            terraria_window_list.append(hwnd)
            
    # Вывод окна в лист, чтобы вытащить его из функции без return
    terraria_window_list = []
    all_win = []

    
    # Перебор всех окон и вызов функции handle_windows для каждого
    win32gui.EnumWindows(handle_windows, None)
    
    
    if terraria_window_list == []:
        print("Окно не найдено")
        exit()

    
    return terraria_window_list[0]
        

def get_window_region(terraria_window):
    """
    Функция достает координаты и размеры окна
    """
    x0, y0, x1, y1 = win32gui.GetWindowRect(terraria_window)
    width = x1 - x0
    height = y1 - y0
    return (x0, y0, width, height)


def background_click(terraria_window, x, y):
    """
    Имитирует нажатия в окне без использования основного курсора (даже в окне на фоне)
    """
    print(terraria_window)
    print(x, y)
    
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(terraria_window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    sleep(0.7)
    win32gui.SendMessage(terraria_window, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
    
def get_cropped_screenshot(terraria_window, x, y, border_len):
    screenshot = get_background_sreenshot(terraria_window)
    cropped_screenshot = screenshot[y-border_len:y+border_len, x-border_len:x+border_len]
    gray_cropped_screen = cv2.cvtColor(cropped_screenshot, cv2.COLOR_BGR2GRAY)
    return gray_cropped_screen

def get_background_sreenshot(terraria_window):
    """
    Функция делаем скриншот окна из фонового режима
    """
    
    hwndDC = win32gui.GetWindowDC(terraria_window)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    
    window_region = get_window_region(terraria_window)
    width, height = window_region[2], window_region[3]

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)    
    saveDC.SelectObject(saveBitMap)
    
    # Printwindow нужно для избежания черного скриншота
    windll.user32.PrintWindow(terraria_window, saveDC.GetSafeHdc(), 2)
    
    bmpstr = saveBitMap.GetBitmapBits(True)
    
    # Конвертируем в матрицу для дальнейшего использования в CV2
    screenshot = np.frombuffer(bmpstr, dtype='uint8')
    screenshot.shape = (height, width, 4)
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(terraria_window, hwndDC)
    
    return screenshot


def get_window_pos_mouse(terraria_window, mouse_x, mouse_y):
    """
    Функция перерасчитывает 
    координаты экрана на координаты окна
    """
    
    # Координаты начальной точки окна (левый верхний угол)
    win_x, win_y, _, _ = get_window_region(terraria_window)
    
    # Координаты курсора относительно окна
    win_mouse_x = mouse_x - win_x
    win_mouse_y = mouse_y - win_y
    
    return win_mouse_x, win_mouse_y

# define the function to compute MSE between two images
def mean_squared_error(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse, diff


