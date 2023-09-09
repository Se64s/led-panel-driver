#
# cmd_layer.py
# Brief: Class to handle command layer
#

CMD_ID_ACK = 0
CMD_ID_CLEAR = 1
CMD_ID_SET = 2
CMD_ID_IMG = 3
CMD_ID_EXIT = 4

_cmd_len = {
    CMD_ID_ACK: 1,
    CMD_ID_CLEAR: 1,
    CMD_ID_SET: 4,
    CMD_ID_IMG: 5,
    CMD_ID_EXIT: 1,
}

class CommandPayload:

    def __init__(self, cmd=None, payload=None) -> None:
        self.__cmd = cmd
        self.__payload = payload
    
    def get_payload_len(self):
        return len(self.__payload)
    
    def get_cmd(self):
        return self.__cmd
    
    def get_payload(self):
        if self.__cmd == CMD_ID_SET:
            return (self.__payload[0], 
                    self.__payload[1], 
                    self.__payload[2])
        elif self.__cmd == CMD_ID_IMG:
            return ((self.__payload[0] << 8) | self.__payload[1], 
                    (self.__payload[2] << 8) | self.__payload[3], 
                    self.__payload[4:])
        else:
            return None


class CommandHandler:

    def __init__(self, cmd_callback=None, send_func=None) -> None:
        self.__cb = cmd_callback
        self.__send = send_func

    def process_frame(self, frame:bytearray) -> None:
        if self.__cb:
            cmd = frame[0]
            len_cmd = len(frame)
            if cmd == CMD_ID_ACK:
                if len_cmd == _cmd_len[CMD_ID_ACK]:
                    cp = CommandPayload(frame[0], frame[1:])
                    self.__cb(cp)
            elif cmd == CMD_ID_CLEAR:
                if len_cmd == _cmd_len[CMD_ID_CLEAR]:
                    cp = CommandPayload(frame[0], frame[1:])
                    self.__cb(cp)
            elif cmd == CMD_ID_SET:
                if len_cmd == _cmd_len[CMD_ID_SET]:
                    cp = CommandPayload(frame[0], frame[1:])
                    self.__cb(cp)
            elif cmd == CMD_ID_IMG:
                n_row = (frame[1] << 8) | frame[2]
                n_col = (frame[3] << 8) | frame[4]
                cmd_size = 1 + 4 + (n_row * n_col * 3)
                if len_cmd == cmd_size:
                    cp = CommandPayload(frame[0], frame[1:])
                    self.__cb(cp)
            elif cmd == CMD_ID_EXIT:
                if len_cmd == _cmd_len[CMD_ID_EXIT]:
                    cp = CommandPayload(frame[0], frame[1:])
                    self.__cb(cp)
            else:
                pass

    def send_ack(self) -> None:
        cmd_payload = bytearray()
        cmd_payload.append(CMD_ID_ACK)
        if self.__send:
            self.__send(cmd_payload)

    def send_clear(self) -> None:
        cmd_payload = bytearray()
        cmd_payload.append(CMD_ID_CLEAR)
        if self.__send:
            self.__send(cmd_payload)

    def send_set(self, r_value:int, g_value:int, b_value:int) -> None:
        cmd_payload = bytearray()
        cmd_payload.append(CMD_ID_SET)
        cmd_payload.append(r_value)
        cmd_payload.append(g_value)
        cmd_payload.append(b_value)
        if self.__send:
            self.__send(cmd_payload)

    def send_image(self, n_row, n_col, rgb_pixel_array) -> None:
        if (n_row * n_col * 3) == len(rgb_pixel_array):
            cmd_payload = bytearray()
            cmd_payload.append(CMD_ID_IMG)
            cmd_payload.append((n_row >> 8) & 0xFF)
            cmd_payload.append((n_row >> 0) & 0xFF)
            cmd_payload.append((n_col >> 8) & 0xFF)
            cmd_payload.append((n_col >> 0) & 0xFF)
            cmd_payload.extend(rgb_pixel_array)
            if self.__send:
                self.__send(cmd_payload)

    def send_exit(self) -> None:
        cmd_payload = bytearray()
        cmd_payload.append(CMD_ID_EXIT)
        if self.__send:
            self.__send(cmd_payload)


def __test_send(data_to_send:bytearray):
    print(f" - DATA_TX:")
    for data in data_to_send:
        print(f"   0x{data:02x}")

def __test_cb(cmd_payload:CommandPayload):
    print(f" - Command Received:")
    if cmd_payload.get_cmd() == CMD_ID_ACK:
        print("   CMD_ACK")
    elif cmd_payload.get_cmd() == CMD_ID_CLEAR:
        print("   CMD_CLEAR")
    elif cmd_payload.get_cmd() == CMD_ID_SET:
        (r,g,b) = cmd_payload.get_payload()
        print(f"   CMD_SET: {r}, {g}, {b}")
    elif cmd_payload.get_cmd() == CMD_ID_IMG:
        (n_row, n_col, pixel_data) = cmd_payload.get_payload()
        print(f"   CMD_IMG: {n_row}, {n_col}, {pixel_data}")
    elif cmd_payload.get_cmd() == CMD_ID_EXIT:
        print("   CMD_EXIT")
    else:
        print("   Command Unknown")

def test():
    # Test send command
    ch = CommandHandler(__test_cb, __test_send)
    print("TX CMD ACK")
    ch.send_ack()
    print("TX CMD CLEAR")
    ch.send_clear()
    print("TX CMD SET")
    ch.send_set(0xAA,0xBB,0xCC)
    print("TX CMD IMG")
    n_row = 2
    n_col = 2
    pixel_data = bytearray([0,0,0,1,1,1,2,2,2,3,3,3])
    ch.send_image(n_row, n_col, pixel_data)
    print("TX CMD EXIT")
    ch.send_exit()
    # Test rx command
    print("RX CMD ACK")
    cmd_payload_ack=bytearray([CMD_ID_ACK])
    ch.process_frame(cmd_payload_ack)
    print("RX CMD CLEAR")
    cmd_payload_clear=bytearray([CMD_ID_CLEAR])
    ch.process_frame(cmd_payload_clear)
    print("RX CMD SET")
    cmd_payload_set=bytearray([CMD_ID_SET,2,3,4])
    ch.process_frame(cmd_payload_set)
    print("RX CMD IMG")
    cmd_payload_image=bytearray([CMD_ID_IMG,0,1,0,1,0xAA,0xBB,0xCC])
    ch.process_frame(cmd_payload_image)
    print("RX CMD EXIT")
    cmd_payload_exit=bytearray([CMD_ID_EXIT])
    ch.process_frame(cmd_payload_exit)

if __name__ == '__main__':
    test()

# EOF
