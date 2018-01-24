# from bms_interface import *
from image_processor import *
import rpc_server
import threading

if __name__ == "__main__":
    image_processor = ImageProcessor()
    thread = threading.Thread(target = image_processor.rec_main)
    thread.start()
    rpc_server.register_rpc(image_processor)