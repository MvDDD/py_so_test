import ctypes
dll = ctypes.CDLL('/home/mffvd/Documents/py_so_test/file/libfile.so')


i8 = ctypes.c_int8;        u8 = ctypes.c_uint8
i16 = ctypes.c_int16;      u16 = ctypes.c_uint16
i32 = ctypes.c_int32;      u32 = ctypes.c_uint32
i64 = ctypes.c_int64;      u64 = ctypes.c_uint64
f32 = ctypes.c_float;      f64 = ctypes.c_double
f80 = ctypes.c_longdouble; void = None

sizeof = ctypes.sizeof

def ptr(typ):
    if typ==None:
        return ctypes.c_void_p
    c = ctypes.POINTER(typ)
    c.size = ctypes.sizeof(ctypes.c_void_p)
    return c

class FILE(ctypes.Structure):
    _fields_ = [
    ]

    def __repr__(self):
        contents_array = []
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<FILE {{{string}}}>"

class File:
    class Struct(ctypes.Structure):
        _fields_ = [
            ("f", ptr(FILE)),
            ("_error", i32),
        ]
    
    Struct_LP = ctypes.POINTER(Struct)
    c__error = dll.File__error
    c__error.argtypes = [Struct_LP]
    c__error.restype = i32
    c_create = dll.File_create
    c_create.argtypes = [Struct_LP, ptr(i8), ptr(i8)]
    c_create.restype = void
    c_destroy = dll.File_destroy
    c_destroy.argtypes = [Struct_LP]
    c_destroy.restype = void
    c_read = dll.File_read
    c_read.argtypes = [Struct_LP, ptr(void), u64]
    c_read.restype = u64
    c_write = dll.File_write
    c_write.argtypes = [Struct_LP, ptr(void), u64]
    c_write.restype = u64
    c_gethandle = dll.File_gethandle
    c_gethandle.argtypes = [Struct_LP]
    c_gethandle.restype = ptr(FILE)

    @staticmethod
    def init_from(struct_instance):
        if not isinstance(struct_instance, File.Struct):
            raise TypeError("init_from requires a File.Struct instance")
        instance = object.__new__(File)
        instance._struct = File.Struct_LP()
        instance._struct.contents = struct_instance
        return instance

    def __init__(self, path=ptr(i8)(), mode=ptr(i8)()):
        self._struct = File.Struct_LP()
        self._struct.contents = File.Struct()
        self.c_create(self._struct, path, mode)
        error = self.c__error(self._struct)
        if error: raise MemoryError(f"File.create failed with code {error}")
    def __del__(self):
        self.c_destroy(self._struct)
        error = self.c__error(self._struct)
        if error: raise MemoryError(f"File.destroy failed with code {error}")

    def read(self, buffer=ptr(void)(), length=u64()):
        retval = self.c_read(self._struct, buffer, length)
        error = self.c__error(self._struct)
        if error: raise MemoryError(f"File.read failed with code {error}")
        return retval

    def write(self, buffer=ptr(void)(), length=u64()):
        retval = self.c_write(self._struct, buffer, length)
        error = self.c__error(self._struct)
        if error: raise MemoryError(f"File.write failed with code {error}")
        return retval

    def gethandle(self):
        retval = self.c_gethandle(self._struct)
        error = self.c__error(self._struct)
        if error: raise MemoryError(f"File.gethandle failed with code {error}")
        return retval

    @property
    def f(self): return self._struct.contents.f
    @f.setter
    def f(self, value): self._struct.contents.f = value

    def __repr__(self):
        contents_array = [("f", self._struct.contents.f), ("_error", self._struct.contents._error)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<File {{{string}}}>"

