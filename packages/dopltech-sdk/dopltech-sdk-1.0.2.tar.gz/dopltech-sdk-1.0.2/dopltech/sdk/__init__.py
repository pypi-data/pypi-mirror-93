from ctypes import *
import logging
import os
import signal
import sys
import threading
import time

from dopltech.protos.common_pb2 import Frame

go_int_type=None
if sys.maxsize > 2**32:
    go_int_type = c_longlong
else:
    go_int_type = c_int32

# define class GoString to map:
# C type struct { const char *p; GoInt n; }
class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", go_int_type)]

# define class GoSlice to map to:
# C type struct { void *data; GoInt len; GoInt cap; }
class GoSlice(Structure):
    _fields_ = [("data", POINTER(c_void_p)), ("len", go_int_type), ("cap", go_int_type)]

# Setup logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

lib_extension = '.so'
if os.name == 'nt':
    lib_extension = '.dll'

lib_arch = 'amd64'
if sys.maxsize <= 2**32:
    lib_arch = 'arm'

script_dir = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.join(script_dir, 'bin', 'libsdk_' + lib_arch + lib_extension)

lib = cdll.LoadLibrary(lib_path)

# Describe GetFrame
get_frame_func_type = CFUNCTYPE(c_bool, POINTER(c_ubyte), POINTER(c_int))
on_frame_func_type = CFUNCTYPE(c_bool, POINTER(c_ubyte), c_int)
on_session_func_type = CFUNCTYPE(None, c_ulonglong)

# Describe initialize
lib.libsdk_initialize.argtypes = [GoString, on_session_func_type, on_session_func_type, get_frame_func_type, on_frame_func_type]
lib.libsdk_initialize.restype = None

# Describe connect
lib.libsdk_connect.argtypes = []
lib.libsdk_connect.restype = None

# Describe disconnect
lib.libsdk_disconnect.argtypes = []
lib.libsdk_disconnect.restype = None

def to_go_string(pyString):
    return GoString(pyString.encode(), len(pyString))

def to_go_slice(arr):
    size = len(arr)
    return GoSlice((c_void_p * size)(*arr), size, size)

def ctrl_c_handler(sig, frame):
    print('Disconnecting from telerobotics')
    device_id = int(os.environ.get('DEVICE_ID'))
    disconnect(device_id)

def block_until_ctrl_c():
    signal.signal(signal.SIGINT, ctrl_c_handler)
    while True:
        time.sleep(1)

class Sdk:
    def __init__(
        self,
        config_file_path,
        on_session_joined,
        on_session_ended,
        get_frame_callback,
        on_frame_callback,
    ):
        self.__config_file_path__ = to_go_string(config_file_path)
        self.__on_session_joined__ = on_session_func_type(on_session_joined)
        self.__on_session_ended__ = on_session_func_type(on_session_ended)
        self.__get_frame_callback__ = get_frame_callback
        self.__on_frame_callback__ = on_frame_callback

        self.__c_get_frame_handler__ = get_frame_func_type(self.__get_frame_handler__)
        self.__c_on_frame_handler__ = on_frame_func_type(self.__on_frame_handler__)
        
        logging.info("Initializing dopltech sdk")
        return lib.libsdk_initialize(
            self.__config_file_path__,
            self.__on_session_joined__,
            self.__on_session_ended__,
            self.__c_get_frame_handler__,
            self.__c_on_frame_handler__,
        )
    
    @staticmethod
    def test():
        return lib.libsdk_test()

    def connect(self):
        logging.info("Connecting to telerobotics")
        return lib.libsdk_connect()

    def connect_async(self):
        connect_thread = threading.Thread(
            target=self.connect,
        )
        connect_thread.start()

    def disconnect(self):
        return lib.libsdk_disconnect()

    def join_session(self, session_id):
        return lib.libsdk_joinSession(0, session_id)

    def __get_frame_handler__(self, buffer, buffer_size_ptr):
        frame = self.__get_frame_callback__()
        if not frame:
            return True
        
        return self.__fill_buffer_with_frame__(buffer, buffer_size_ptr, frame)

    def __on_frame_handler__(self, buffer, buffer_size):
        frame = self.__buffer_to_frame__(buffer, buffer_size)
        if not frame:
            return False
            
        return self.__on_frame_callback__(frame)

    def __fill_buffer_with_frame__(self, buffer, buffer_size_ptr, frame):
        frame_bytes = frame.SerializeToString()
        frame_bytes_length = len(frame_bytes)

        buffer_size_ptr[0] = frame_bytes_length

        for index in range(frame_bytes_length):
            buffer[index] = frame_bytes[index]

        return True

    def __buffer_to_frame__(self, buffer, buffer_size):
        buffer_copy = bytearray(buffer_size)
        for index in range(buffer_size):
            buffer_copy[index] = buffer[index]

        frame = Frame()
        frame.ParseFromString(buffer_copy)
        return frame