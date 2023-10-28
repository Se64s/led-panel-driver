#
# main.py
# Brief: Application entry point
#

import sys
import micropython
import led_panel_handler
import link_layer
import cmd_layer

# -----------------------------------------------------------------------------

class DeviceHandler:

    def __init__(self) -> None:
        self.__link_handler = link_layer.LinkHandler(frame_callback=self.__link_callback, send_func=self.__link_write)
        self.__cmd_handler = cmd_layer.CommandHandler(cmd_callback=self.__cmd_callback, send_func=self.__cmd_write)
        self.__led_panel = led_panel_handler.LedPanel()

    def __link_callback(self, link_frame:bytearray):
        self.__cmd_handler.process_frame(link_frame)

    def __link_write(self, data_link:bytearray):
        sys.stdout.buffer.write(data_link)

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

    def process_byte(self, data_byte:int):
        self.__link_handler.get_byte(data_byte)


# -----------------------------------------------------------------------------

def enable_repl_scape(status:bool):
    if status:
        micropython.kbd_intr(3)
    else:
        micropython.kbd_intr(-1)

def read_byte():
    return sys.stdin.buffer.read(1)

# -----------------------------------------------------------------------------

device = DeviceHandler()

# -----------------------------------------------------------------------------

def main(arguments):

    # Disable scape character on REPL
    enable_repl_scape(False)

    # Main loop
    while True:
        c = read_byte()
        if c != None:
            device.process_byte(c)


if __name__ == '__main__':
    main(None)

# EOF
