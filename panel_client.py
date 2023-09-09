#
# panel_client.py
# Brief: App to manage panel server
#

from lib import link_layer, cmd_layer, ppm_handler
import serial
import argparse

# -----------------------------------------------------------------------------

def link_write(data_link:bytearray):
    global ser
    ser.write(data_link)

def cmd_write(data_cmd:bytearray):
    global lh
    lh.send_frame(data_cmd)

def link_cb(link_frame:bytearray):
    global ch
    ch.process_frame(link_frame)

def cmd_cb(cmd_payload:cmd_layer.CommandPayload):
    global ch
    if cmd_payload.get_cmd() == cmd_layer.CMD_ID_ACK:
        print("ACK")
        pass
    elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_CLEAR:
        pass
    elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_SET:
        pass
    elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_IMG:
        pass
    elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_EXIT:
        pass
    else:
        pass

# -----------------------------------------------------------------------------

cmd_to_code = {
    'clear': cmd_layer.CMD_ID_CLEAR,
    'set': cmd_layer.CMD_ID_SET,
    'exit': cmd_layer.CMD_ID_EXIT,
    'image': cmd_layer.CMD_ID_IMG,
}

cmd_min_arg = {
    'clear': 0,
    'set': 3,
    'exit': 0,
    'image': 1,
}

SERIAL_PORT="/dev/ttyACM0"
SERIAL_BAUD=115200
SERIAL_TIMEOUT=0.2
APP_VERSION="0.0.1"

lh = link_layer.LinkHandler(frame_callback=link_cb, send_func=link_write)
ch = cmd_layer.CommandHandler(cmd_callback=cmd_cb, send_func=cmd_write)
ser = serial.Serial(baudrate=SERIAL_BAUD, timeout=SERIAL_TIMEOUT)

# -----------------------------------------------------------------------------


def init_argparse() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description="Client app to send control commands to Led Panel server."
    )

    parser.add_argument("-v", "--version", action="version", version = f"{parser.prog} version {APP_VERSION}")
    parser.add_argument("-p", "--port", help="Serial port")
    parser.add_argument("-b", "--baudrate", help="Serial baudrate")
    parser.add_argument("command", choices=["clear", "set", "exit", "image"], help="Control command")
    parser.add_argument('cmd_args', nargs='*', help="Command input arg")

    return parser

# -----------------------------------------------------------------------------

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    # Check input arg
    if args.baudrate:
        ser.baudrate = SERIAL_BAUD
    if args.port:
        ser.port = args.port
    else:
        ser.port = SERIAL_PORT
    ser.open()

    # Send command
    if len(args.cmd_args) != cmd_min_arg[args.command]:
        raise ValueError(f"Incorrect number of arguments, got {len(args.cmd_args)}, expected {cmd_min_arg[args.command]}")

    if args.command == "clear":
        ch.send_clear()

    elif args.command == "set":
        ch.send_set(r_value=int(args.cmd_args[0]),
                    g_value=int(args.cmd_args[1]),
                    b_value=int(args.cmd_args[2]))
        
    elif args.command == "exit":
        ch.send_exit()

    elif args.command == "image":
        image_path = args.cmd_args[0]
        ih=ppm_handler.PpmImage(image_path)
        ch.send_image(ih.high, ih.width, ih.pixel_data)

    ser.close()


if __name__ == '__main__':
    main()

# EOF
