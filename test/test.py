import ctypes
dll = ctypes.CDLL('/home/mffvd/Documents/py_so_test/test/libtest.so')


i8 = ctypes.c_int8
u8 = ctypes.c_uint8
i16 = ctypes.c_int16
u16 = ctypes.c_uint16
i32 = ctypes.c_int32
u32 = ctypes.c_uint32
i64 = ctypes.c_int64
u64 = ctypes.c_uint64
f32 = ctypes.c_float
f64 = ctypes.c_double
f80 = ctypes.c_longdouble
void = None

sizeof = ctypes.sizeof
def ptr(typ):
    if typ==None:
        return ctypes.c_void_p
    c = ctypes.POINTER(typ)
    c.size = ctypes.sizeof(ctypes.c_void_p)
    return c
#struct
class str(ctypes.Structure):
    _fields_ = [
        ("len", i32),
        ("data", ptr(i8)),
    ]

    def __repr__(self):
        contents_array = [("len", self.len), ("data", self.data)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<str {{{string}}}>"
add = dll.add
add.argtypes = [i32, i32]
add.restype = i32
add_array = dll.add_array
add_array.argtypes = [ptr(i32), ptr(i32), ptr(i32), i32]
add_array.restype = void
init_str_arr = dll.init_str_arr
init_str_arr.argtypes = [ptr(str), i32]
init_str_arr.restype = void
