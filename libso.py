import ctypes

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
def createbuffer(size):
	return bytearray(size)

def copybuffer(old, new):
	for i in range(len(old)):
		new[i] = old[i]
def cast_buffer(buffer, size):
	return (size * (len(buffer)//ctypes.sizeof(size))).from_buffer(buffer)

def buffer_to_list(buffer):
	return [item for item in buffer]