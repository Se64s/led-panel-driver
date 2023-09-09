#
# ppm_handler.py
# Brief: Class to handle ppm file format
#

PIXEL_MAX_VALUE=255
PIXEL_NUM_CHANNELS=3
PIXEL_BIN_FORMAT='P6'

class PpmImage:

    @staticmethod
    def __read_ascii_line(f):
        data=f.readline()
        while data.count(ord('#')) != 0:
            data=f.readline()
        return str(data, 'utf-8').strip()

    def __init__(self, image_path:str) -> None:
        f = open(image_path, "rb")
        self.format = self.__read_ascii_line(f)
        if self.format != PIXEL_BIN_FORMAT:
            raise ValueError(f"Format not supported: read {PIXEL_BIN_FORMAT}, expected {self.format}.")
        (ascii_width, ascii_high) = self.__read_ascii_line(f).split()
        self.width = int(ascii_width)
        self.high = int(ascii_high)
        self.max_pixel_value = int(self.__read_ascii_line(f))
        if self.max_pixel_value != PIXEL_MAX_VALUE:
            raise ValueError(f"Max pixel value supported: {PIXEL_MAX_VALUE}, read {self.max_pixel_value}.")
        pixel_raw_data = f.read()
        if len(pixel_raw_data) % PIXEL_NUM_CHANNELS != 0:
            raise ValueError(f"Pixel data channels doesnt match with expeted value.")
        self.pixel_data=pixel_raw_data
        f.close()

    def show_metadata(self):
        print(f"PPM Format: {self.format}")
        print(f"Image size: {self.width} x {self.high}, {self.width * self.high} pixels")
        print(f"Pixel max value: {self.max_pixel_value}")
        print(f"Pixel data Array: {self.pixel_data}")


def test():
    test_image="./test_data/test_bin.ppm"
    ih = PpmImage(test_image)
    ih.show_metadata()

if __name__ == '__main__':
    test()

# EOF
