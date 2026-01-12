import ctypes
dll = ctypes.CDLL('/home/mffvd/Documents/py lib so test/point/libpoint.so')


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
class Point:
    class Struct(ctypes.Structure):
        _fields_ = [
            ("x", f32),
            ("y", f32),
            ("vx", f32),
            ("vy", f32),
            ("error", i32),
        ]
    
    Struct_LP = ctypes.POINTER(Struct)
    c_rotate = dll.Point_rotate
    c_update = dll.Point_update
    c_create = dll.Point_create
    c_destroy = dll.Point_destroy
    c__error = dll.Point__error
    c_throw = dll.Point_throw

    def __init__(self):
        self._struct = Point.Struct_LP()
        self._struct.contents = Point.Struct()
        self.c_create(self._struct)
        error = self.c__error(self._struct)
        if error: raise MemoryError("Point.create failed with code {error}")
    def __del__(self):
        self.c_destroy(self._struct)
        error = self.c__error(self._struct)
        if error: raise MemoryError("Point.destroy failed with code {error}")

    def rotate(self, center=ctypes.POINTER(Struct)(), angle=f32()):
        self.c_rotate(self._struct, center, angle)
        error = self.c__error(self._struct)
        if error: raise MemoryError("Point.rotate failed with code {error}")

    def update(self):
        self.c_update(self._struct)
        error = self.c__error(self._struct)
        if error: raise MemoryError("Point.update failed with code {error}")

    def _error(self):
        self.c__error(self._struct)
        error = self.c__error(self._struct)
        if error: raise MemoryError("Point._error failed with code {error}")

    def throw(self, code=i32()):
        self.c_throw(self._struct, code)
        error = self.c__error(self._struct)
        if error: raise MemoryError("Point.throw failed with code {error}")

    @property
    def x(self): return self._struct.contents.x
    @x.setter
    def x(self, value): self._struct.contents.x = value

    @property
    def y(self): return self._struct.contents.y
    @y.setter
    def y(self, value): self._struct.contents.y = value

    @property
    def vx(self): return self._struct.contents.vx
    @vx.setter
    def vx(self, value): self._struct.contents.vx = value

    @property
    def vy(self): return self._struct.contents.vy
    @vy.setter
    def vy(self, value): self._struct.contents.vy = value

    @property
    def error(self): return self._struct.contents.error
    @error.setter
    def error(self, value): self._struct.contents.error = value

    def __repr__(self):
        contents_array = [("x", self._struct.contents.x), ("y", self._struct.contents.y), ("vx", self._struct.contents.vx), ("vy", self._struct.contents.vy), ("error", self._struct.contents.error)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<Point {{{string}}}>"
