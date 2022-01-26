#!/usr/bin/env python
import time
import sys
import websocket
import _thread
import time
import rel
import json
import base64
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# if len(sys.argv) < 2:
#     sys.exit("Require an image argument")
# else:
#     image_file = sys.argv[1]

# image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)
# double_buffer = matrix.CreateFrameCanvas()

rel.safe_read()

def on_message(ws, message):
    data = json.loads(message)
    if data['type'] == 'user-init':
        ws.send(json.dumps({'type':'viewer-init'}))
    elif data['type'] == 'buffer':
        print('buffer received')
        decoded_image_data = base64.decodebytes(data['content'].encode('utf-8'))
        im = Image.frombytes('RGBA', (32, 32), decoded_image_data)
        matrix.SetImage(im.convert('RGB'))
        # double_buffer.SetImage(im.convert('RGB'))
        # double_buffer = matrix.SwapOnVSync(double_buffer)


def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://192.168.0.24:8000",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()