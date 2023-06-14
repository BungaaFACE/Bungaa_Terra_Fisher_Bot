import win32.win32api as win32api
import win32.win32gui as win32gui
import pythonwin.win32ui as win32ui
import win32.lib.win32con as win32con
from ctypes import windll
import numpy as np


def get_terraria_window():
    """
    Функция для получения окна
    Окно необходимо для дальнейшей работы с ним
    """
    
    def handle_windows(hwnd, _):
        """
        Функция для нахождения нужного окна из списка всех окон
        """
        if "Terraria: " in win32gui.GetWindowText(hwnd):
            terraria_window.append(hwnd)
            
    # Вывод окна в лист, чтобы вытащить его из функции без return
    terraria_window = []
    
    # Перебор всех окон и вызов функции handle_windows для каждого
    win32gui.EnumWindows(handle_windows, None)
    
    if terraria_window == []:
        print("Окно не найдено")
        exit()
        
    return terraria_window[0]


def get_window_region(hwnd):
    """
    Функция достает координаты и размеры окна
    """
    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    width = x1 - x0
    height = y1 - y0
    return (x0, y0, width, height)


def background_click(cookie_window, x, y):
    """
    Имитирует нажатия в окне без использования основного курсора (даже в окне на фоне)
    """
    
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(cookie_window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(cookie_window, win32con.WM_LBUTTONUP, None, lParam)
    

def get_background_sreenshot(hwnd):
    """
    Функция делаем скриншот окна из фонового режима
    """
    
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    
    window_region = get_window_region(hwnd)
    width, height = window_region[2], window_region[3]
   
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)    
    saveDC.SelectObject(saveBitMap)
    
    # Printwindow нужно для избежания черного скриншота
    windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
    
    bmpstr = saveBitMap.GetBitmapBits(True)
    
    # Конвертируем в матрицу для дальнейшего использования в CV2
    screenshot = np.frombuffer(bmpstr, dtype='uint8')
    screenshot.shape = (height, width, 4)
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    
    return screenshot


def get_window_cur_pos_mouse(hwnd):
    """
    Функция находит текущее местоположение курсора с перерасчетом
    с координат экрана на координаты окна
    """
    
    # Координаты курсора
    mouse_x, mouse_y = win32api.GetCursorPos()
    # Координаты начальной точки окна (левый верхний угол)
    win_x, win_y, _, _ = get_window_region(hwnd)
    
    # Координаты курсора относительно окна
    win_mouse_x = mouse_x - win_x
    win_mouse_y = mouse_y - win_y
    
    return win_mouse_x, win_mouse_y
    