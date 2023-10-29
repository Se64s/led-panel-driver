#
# main.py
# Brief: Application entry point
#

import sys
import micropython
import led_panel_handler
import link_layer
import cmd_layer
import machine
import time

# -----------------------------------------------------------------------------

DEFAULT_SERIAL_PORT = 1
DEFAULT_SERIAL_TX_PIN = 8
DEFAULT_SERIAL_RX_PIN = 9
DEFAULT_BAUDRATE = 921600
DEFAULT_RX_BUFF_SIZE = 4*1024

class DeviceHandler:

    def __init__(self) -> None:
        self.__link_handler = link_layer.LinkHandler(frame_callback=self.__link_callback, send_func=self.__link_write)
        self.__cmd_handler = cmd_layer.CommandHandler(cmd_callback=self.__cmd_callback, send_func=self.__cmd_write)
        self.__led_panel = led_panel_handler.LedPanel()
        self.__uart = machine.UART(DEFAULT_SERIAL_PORT)
        self.__uart.init(baudrate=DEFAULT_BAUDRATE, rx=machine.Pin(DEFAULT_SERIAL_RX_PIN), tx=machine.Pin(DEFAULT_SERIAL_TX_PIN), rxbuf=DEFAULT_RX_BUFF_SIZE)

    def __link_callback(self, link_frame:bytearray):
        self.__cmd_handler.process_frame(link_frame)

    def __link_write(self, data_link:bytearray):
        self.__uart.write(data_link)

    def __cmd_callback(self, cmd_payload:cmd_layer.CommandPayload):
        if cmd_payload.get_cmd() == cmd_layer.CMD_ID_ACK:
            pass
        elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_CLEAR:
            self.__led_panel.clear()
            self.__cmd_handler.send_ack()
        elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_SET:
            (r,g,b) = cmd_payload.get_payload()
            self.__led_panel.fill(r,g,b)
            self.__cmd_handler.send_ack()
        elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_IMG:
            (n_row, n_col, pixel_data) = cmd_payload.get_payload()
            self.__led_panel.set_image(n_row, n_col, pixel_data)
            self.__cmd_handler.send_ack()
        elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_EXIT:
            self.__cmd_handler.send_ack()
            enable_repl_scape(True)
        else:
            pass

    def __cmd_write(self, data_cmd:bytearray):
        self.__link_handler.send_frame(data_cmd)

    def check_port(self):
        while self.__uart.any() > 0:
            self.__link_handler.get_bytes(self.__uart.read(self.__uart.any()))
            

# -----------------------------------------------------------------------------

def enable_repl_scape(status:bool):
    if status:
        micropython.kbd_intr(3)
    else:
        micropython.kbd_intr(-1)

# -----------------------------------------------------------------------------

device = DeviceHandler()

# -----------------------------------------------------------------------------

def main(arguments):

    # Main loop
    while True:
        device.check_port()


if __name__ == '__main__':
    main(None)

# EOF
