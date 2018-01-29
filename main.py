# from bms_interface import *
from image_processor import *
from HUD_image_processor import *
import rpc_server
import threading

if __name__ == "__main__":
    image_processor = ImageProcessor()
    thread = threading.Thread(target = image_processor.rec_main)
    thread.start()

    # HUD_image_Processor = HUD_ImageProcessor()
    # HUD_thread = threading.Thread(target=HUD_image_Processor.HUD_rec_main)
    # HUD_thread.start()

    rpc_server.register_rpc(image_processor)