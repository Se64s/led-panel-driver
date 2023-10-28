#
# led_panel_handler.py
# Brief: Module to manage led panels
#

import time
from machine import Pin
from neopixel import NeoPixel

PIXEL_SIZE = 3
PIXEL_DEFAULT_GPIO = 15

class LedPanel:

    def __init__(self, n_row=12, n_col=72, pixel_gpio=PIXEL_DEFAULT_GPIO) -> None:
        self.__n_row = n_row
        self.__n_col = n_col
        self.__np = NeoPixel(Pin(pixel_gpio, Pin.OUT), self.__n_row * self.__n_col)

    def fill(self, r, g, b):
        self.__np.fill((r,g,b))
        self.__np.write()

    def clear(self):
        self.__np.fill((0,0,0))
        self.__np.write()

    def set_image(self, n_row:int, n_col:int, pixel_data:bytearray):
        len_data = len(pixel_data)
        expected_len = n_row * n_col * PIXEL_SIZE
        print(f"Len data: {len_data}")
        if len_data != expected_len:
            raise TypeError(f"size of pixel_data {len_data} doesnt match with expected value {expected_len}")

        for pixel_data_index in range(0, len_data, PIXEL_SIZE):
            pixel_index = int(pixel_data_index / PIXEL_SIZE)
            # Adjust index to go in reverse for odd rows
            pixel_row = int(pixel_index / self.__n_col)
            if pixel_row % 2:
                pixel_base = (pixel_row + 1) * self.__n_col - 1
                pixel_adjust = pixel_index - (pixel_row * self.__n_col)
                pixel_index = pixel_base - pixel_adjust

            self.__np[pixel_index] = (pixel_data[pixel_data_index], 
                                      pixel_data[pixel_data_index + 1], 
                                      pixel_data[pixel_data_index + 2])
        
        # Write values into screen
        self.__np.write()


def test():
    lp = LedPanel()

    # Test SET
    print("Test SET")
    lp.fill(50, 0, 0)
    time.sleep(1)
    lp.fill(50, 50, 0)
    time.sleep(1)
    lp.fill(50, 50, 50)
    time.sleep(1)

    # Test CLEAR
    print("Test CLEAR")
    lp.clear()
    time.sleep(1)

    # Test IMAGE
    print("Test IMAGE")
    test_pixel_data = bytearray()
    test_row_size = 6
    test_col_size = 72
    
    for a in range(test_col_size):
        test_pixel_data.append(a)
        test_pixel_data.append(0)
        test_pixel_data.append(0)
    for a in range(test_col_size):
        test_pixel_data.append(0)
        test_pixel_data.append(a)
        test_pixel_data.append(0)
    for a in range(test_col_size):
        test_pixel_data.append(0)
        test_pixel_data.append(0)
        test_pixel_data.append(a)
    for a in range(test_col_size):
        test_pixel_data.append(a)
        test_pixel_data.append(a)
        test_pixel_data.append(0)
    for a in range(test_col_size):
        test_pixel_data.append(0)
        test_pixel_data.append(a)
        test_pixel_data.append(a)
    for a in range(test_col_size):
        test_pixel_data.append(a)
        test_pixel_data.append(0)
        test_pixel_data.append(a)
    
    lp.set_image(test_row_size, test_col_size, test_pixel_data)


if __name__ == '__main__':
    test()

# EOF
