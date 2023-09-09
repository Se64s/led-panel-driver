#
# main.py
# Brief: Application entry point
#

import uselect
import sys
import micropython
import led_panel_handler
import link_layer
import cmd_layer

# -----------------------------------------------------------------------------

def enable_repl_scape(status:bool):
    if status:
        micropython.kbd_intr(3)
    else:
        micropython.kbd_intr(-1)

def read_byte():
    return(sys.stdin.buffer.read(1) if spoll.poll(0) else None)

def link_write(data_link:bytearray):
    sys.stdout.buffer.write(data_link)

def cmd_write(data_cmd:bytearray):
    global lh
    lh.send_frame(data_cmd)

def link_cb(link_frame:bytearray):
    global ch
    ch.process_frame(link_frame)

def cmd_cb(cmd_payload:cmd_layer.CommandPayload):
    global ch
    global lp
    if cmd_payload.get_cmd() == cmd_layer.CMD_ID_ACK:
        pass
    elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_CLEAR:
        lp.clear()
        ch.send_ack()
    elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_SET:
        (r,g,b) = cmd_payload.get_payload()
        lp.fill(r,g,b)
        ch.send_ack()
    elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_IMG:
        (n_row, n_col, pixel_data) = cmd_payload.get_payload()
        lp.set_image(n_row, n_col, pixel_data)
        ch.send_ack()
    elif cmd_payload.get_cmd() == cmd_layer.CMD_ID_EXIT:
        ch.send_ack()
        enable_repl_scape(True)
    else:
        pass

# -----------------------------------------------------------------------------

spoll = uselect.poll()
lh = link_layer.LinkHandler(frame_callback=link_cb, send_func=link_write)
ch = cmd_layer.CommandHandler(cmd_callback=cmd_cb, send_func=cmd_write)
lp = led_panel_handler.LedPanel()

# -----------------------------------------------------------------------------

def main(arguments):
    # Setup serial polling
    spoll.register(sys.stdin, uselect.POLLIN)

    # Disable scape character on REPL
    enable_repl_scape(False)

    # Main loop
    while True:
        c = read_byte()
        if c != None:
            lh.get_bytes(c)


if __name__ == '__main__':
    main(None)

# EOF
