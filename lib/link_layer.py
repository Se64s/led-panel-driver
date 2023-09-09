#
# link_layer.py
# Brief: Class to handle com link layer
#

LINK_INIT_FLAG=0x7E

LINK_STATE_FLAG=0
LINK_STATE_SIZE=1
LINK_STATE_PAYLOAD=2
LINK_STATE_CHECKSUM=3

class LinkHandler:

    def __init__(self, frame_callback=None, send_func=None) -> None:
        self.send = send_func
        self.cb = frame_callback
        self.__reset_state()

    def get_bytes(self, input_data:bytearray) -> None:
        for byte in input_data:
            self.__process_byte(byte)

    def get_byte(self, input_data:int) -> None:
        self.__process_byte(input_data)

    def __reset_state(self) -> None:
        self.__rx_state = LINK_STATE_FLAG
        self.__rx_len = 0
        self.__rx_index = 0
        self.__frame = bytearray()

    def __process_byte(self, byte:int) -> None:
        if self.__rx_state == LINK_STATE_FLAG:
            if byte == LINK_INIT_FLAG:
                self.__rx_index += 1
                self.__rx_state = LINK_STATE_SIZE

        elif self.__rx_state == LINK_STATE_SIZE:
            if self.__rx_index == 1:
                self.__rx_index += 1
                self.__rx_len = byte << 8
            elif self.__rx_index == 2:
                self.__rx_index += 1
                self.__rx_len |= byte
                if self.__rx_len == 0:
                    self.__reset_state()
                else:
                    self.__rx_state = LINK_STATE_PAYLOAD
            else:
                self.__reset_state()

        elif self.__rx_state == LINK_STATE_PAYLOAD:
            if (self.__rx_index - 3) < self.__rx_len:
                self.__frame.append(byte)
                self.__rx_index += 1
                if (self.__rx_index - 3) == self.__rx_len:
                    self.__rx_state = LINK_STATE_CHECKSUM
            else:
                self.__reset_state()
            
        elif self.__rx_state == LINK_STATE_CHECKSUM:
            if byte == self.__compute_checksum(self.__frame):
                if self.cb:
                    self.cb(self.__frame)
                self.__reset_state()
            else:
                self.__reset_state()

        else:
            self.__reset_state()

    def send_frame(self, frame:bytearray) -> None:
        if self.send:
            out_data = bytearray()
            out_data.append(LINK_INIT_FLAG)
            out_data.append((len(frame) >> 8) & 0xFF)
            out_data.append((len(frame) >> 0) & 0xFF)
            self.send(out_data)
            self.send(frame)
            out_data = bytearray()
            out_data.append(self.__compute_checksum(frame))
            self.send(out_data)

    @staticmethod
    def __compute_checksum(input_data:bytearray) -> int:
        checksum = 0
        for byte in input_data:
            checksum +=  int(byte)
        return checksum & 0xFF


def __test_send(data_to_send:bytearray):
    print(f" - Tx:")
    for data in data_to_send:
        print(f"0x{data:02x}")

def __test_cb(data_frame:bytearray):
    print(f" - Rx:")
    for data in data_frame:
        print(f"0x{data:02x}")

def test():
    test_send_data = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08')
    test_read_data = bytearray(b'\x7e\x00\x08\x01\x02\x03\x04\x05\x06\x07\x08\x24')
    lh = LinkHandler(frame_callback=__test_cb, send_func=__test_send)
    # Send frame test
    print(f"\n--- Send test ---\n")
    lh.send_frame(test_send_data)
    # Read frame test
    print(f"\n--- Read test ---\n")
    lh.get_bytes(test_read_data)

if __name__ == '__main__':
    test()

# EOF
