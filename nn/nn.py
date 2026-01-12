import ctypes
dll = ctypes.CDLL('/home/mffvd/Documents/py lib so test/nn/libnn.so')


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
class __fsid_t(ctypes.Structure):
    _fields_ = [
    ]

    def __repr__(self):
        contents_array = []
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<__fsid_t {{{string}}}>"
#struct
class Layer(ctypes.Structure):
    _fields_ = [
        ("size", i32),
        ("weights", ctypes.POINTER(f32)),
    ]

    def __repr__(self):
        contents_array = [("size", self.size), ("weights", self.weights)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<Layer {{{string}}}>"
#struct
class Path(ctypes.Structure):
    _fields_ = [
        ("source", i32),
        ("target", i32),
        ("weight", f32),
    ]

    def __repr__(self):
        contents_array = [("source", self.source), ("target", self.target), ("weight", self.weight)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<Path {{{string}}}>"
#struct
class PathLayer(ctypes.Structure):
    _fields_ = [
        ("numpaths", i32),
        ("paths", ctypes.POINTER(Path)),
    ]

    def __repr__(self):
        contents_array = [("numpaths", self.numpaths), ("paths", self.paths)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<PathLayer {{{string}}}>"
#struct
class Net(ctypes.Structure):
    _fields_ = [
        ("numlayers", i32),
        ("layers", ctypes.POINTER(Layer)),
        ("pathlayers", ctypes.POINTER(PathLayer)),
    ]

    def __repr__(self):
        contents_array = [("numlayers", self.numlayers), ("layers", self.layers), ("pathlayers", self.pathlayers)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<Net {{{string}}}>"
class NN:
    class Struct(ctypes.Structure):
        _fields_ = [
            ("net", Net),
            ("_error", i32),
        ]
    
    Struct_LP = ctypes.POINTER(Struct)
    c__error = dll.NN__error
    c_create = dll.NN_create
    c_destroy = dll.NN_destroy
    c_run = dll.NN_run
    c_clone = dll.NN_clone
    c_mutate = dll.NN_mutate

    @staticmethod
    def init_from(struct_instance):
        if not isinstance(struct_instance, NN.Struct):
            raise TypeError("init_from requires a NN.Struct instance")
        instance = object.__new__(NN)
        instance._struct = NN.Struct_LP()
        instance._struct.contents = struct_instance
        return instance

    def __init__(self, numlayers=i32(), layersizes=ctypes.POINTER(i32)()):
        self._struct = NN.Struct_LP()
        self._struct.contents = NN.Struct()
        self.c_create(self._struct, numlayers, layersizes)
        error = self.c__error(self._struct)
        if error: raise MemoryError("NN.create failed with code {error}")
    def __del__(self):
        self.c_destroy(self._struct)
        error = self.c__error(self._struct)
        if error: raise MemoryError("NN.destroy failed with code {error}")

    def run(self, input=ctypes.POINTER(f32)(), output=ctypes.POINTER(f32)()):
        retval = self.c_run(self._struct, input, output)
        error = self.c__error(self._struct)
        if error: raise MemoryError("NN.run failed with code {error}")
        return retval

    def clone(self, new=ctypes.POINTER(Struct)()):
        retval = self.c_clone(self._struct, new)
        error = self.c__error(self._struct)
        if error: raise MemoryError("NN.clone failed with code {error}")
        return retval

    def mutate(self, rate=f32()):
        retval = self.c_mutate(self._struct, rate)
        error = self.c__error(self._struct)
        if error: raise MemoryError("NN.mutate failed with code {error}")
        return retval

    @property
    def net(self): return self._struct.contents.net
    @net.setter
    def net(self, value): self._struct.contents.net = value

    def __repr__(self):
        contents_array = [("net", self._struct.contents.net), ("_error", self._struct.contents._error)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<NN {{{string}}}>"
