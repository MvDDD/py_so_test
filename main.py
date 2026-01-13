from file import *
from libso import i8, u8, i16, u16, i32, u32, i64, u64, f32, f64, f80, \
				  CArray



numitems = 10000
a = CArray(numitems, i8)

file = File(CArray.string(b"main.py").ptr, CArray.string(b"rb").ptr)
l = 0
b = a
while (p := file.read(b.ptr, 100)):
	l += p
	b = b[100:]

print(bytes(a.items()[:l]).decode("utf-8"))
