import ctypes
dll = ctypes.CDLL('/home/mffvd/Documents/py lib so test/nn2/libnn2.so')


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
class NN:
    class Struct(ctypes.Structure):
        _fields_ = [
            ("depth", i32),
            ("layer_sizes", ptr<i32>),
            ("weights", ptr<ptr<f32>>),
            ("biases", ptr<ptr<f32>>),
            ("_error", i32),
        ]
    
    Struct_LP = ctypes.POINTER(Struct)
    c__error = dll.NN__error
    c_create = dll.NN_create
    c_destroy = dll.NN_destroy
    c_forward = dll.NN_forward

    @staticmethod
    def init_from(struct_instance):
        if not isinstance(struct_instance, NN.Struct):
            raise TypeError("init_from requires a NN.Struct instance")
        instance = object.__new__(NN)
        instance._struct = NN.Struct_LP()
        instance._struct.contents = struct_instance
        return instance

    def __init__(self, depth=i32(), layer_sizes=ctypes.POINTER(i32)()):
        self._struct = NN.Struct_LP()
        self._struct.contents = NN.Struct()
        self.c_create(self._struct, depth, layer_sizes)
        error = self.c__error(self._struct)
        if error: raise MemoryError("NN.create failed with code {error}")
    def __del__(self):
        self.c_destroy(self._struct)
        error = self.c__error(self._struct)
        if error: raise MemoryError("NN.destroy failed with code {error}")

    def forward(self, input=ctypes.POINTER(f32)(), output=ctypes.POINTER(f32)()):
        retval = self.c_forward(self._struct, input, output)
        error = self.c__error(self._struct)
        if error: raise MemoryError("NN.forward failed with code {error}")
        return retval

    @property
    def depth(self): return self._struct.contents.depth
    @depth.setter
    def depth(self, value): self._struct.contents.depth = value

    @property
    def layer_sizes(self): return self._struct.contents.layer_sizes
    @layer_sizes.setter
    def layer_sizes(self, value): self._struct.contents.layer_sizes = value

    @property
    def weights(self): return self._struct.contents.weights
    @weights.setter
    def weights(self, value): self._struct.contents.weights = value

    @property
    def biases(self): return self._struct.contents.biases
    @biases.setter
    def biases(self, value): self._struct.contents.biases = value

    def __repr__(self):
        contents_array = [("depth", self._struct.contents.depth), ("layer_sizes", self._struct.contents.layer_sizes), ("weights", self._struct.contents.weights), ("biases", self._struct.contents.biases), ("_error", self._struct.contents._error)]
        string = ", ".join(f"{k}:{v}" for k,v in contents_array)
        return f"<NN {{{string}}}>"
