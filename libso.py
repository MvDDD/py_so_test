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

def is_ctype_type(t):
	# must be a *type*, not an instance
	if not isinstance(t, type):
		return False
	try:
		sizeof(t)
		return True
	except Exception:
		return False

class CArray:

	def __init__(self, length, typ=i32, _buf=None, _owner=None):
		if not is_ctype_type(typ):
			raise TypeError(f"type must be ctypes_type")
		self.length = int(length)
		if self.length < 0:
			raise ValueError("length must be non-negative")
		self.ctype = typ
		self.itemsize = sizeof(self.ctype)

		# underlying contiguous C buffer
		if _buf is None:
			self._buf = (self.ctype * self.length)()
			self._owner = self  # owns memory
		else:
			self._buf = _buf
			self._owner = _owner  # keep reference to original owner

	def __len__(self):
		return self.length

	def __getitem__(self, idx):
		if isinstance(idx, slice):
			start, stop, step = idx.indices(self.length)
			new_length = (stop - start + (step - 1)) // step
			if step != 1:
				# fallback to Python list for non-contiguous slices
				return [self._buf[i] for i in range(start, stop, step)]
			# contiguous slice: type-preserving
			ArrayType = self.ctype * new_length
			base = ctypes.addressof(self._buf)
			addr = base + start * self.itemsize
			new_buf = ArrayType.from_address(addr)
			return CArray(new_length, self.ctype, _buf=new_buf, _owner=self._owner)
		else:
			if idx < 0:
				idx += self.length
			if not 0 <= idx < self.length:
				raise IndexError("index out of range")
			return self._buf[idx]

	def __setitem__(self, idx, value):
		if isinstance(idx, slice):
			start, stop, step = idx.indices(self.length)
			values = list(value)
			if len(values) != ((stop - start + (step - 1)) // step):
				raise ValueError("slice assignment length mismatch")
			for i, v in zip(range(start, stop, step), values):
				self._buf[i] = self.ctype(v)
		else:
			if idx < 0:
				idx += self.length
			if not 0 <= idx < self.length:
				raise IndexError("index out of range")
			self._buf[idx] = self.ctype(value)

	def __iter__(self):
		for i in range(self.length):
			yield self._buf[i]

	# ---- C interop ----

	def address(self):
		return ctypes.addressof(self._buf)

	@property
	def ptr(self):
		return ctypes.cast(self._buf, ctypes.POINTER(self.ctype))

	def as_memoryview(self):
		return memoryview(self._buf)

	# ---- casting support ----

	def cast(self, new_type):
		"""Zero-copy cast using bytearray; returns new CArray with new type."""
		if not is_ctype_type(new_type):
			raise TypeError("new_type must be a ctypes type")
		new_itemsize = sizeof(new_type)
		total_bytes = self.itemsize * self.length
		if total_bytes % new_itemsize != 0:
			raise ValueError(
				f"cannot cast {total_bytes} bytes to element size {new_itemsize}"
			)
		new_length = total_bytes // new_itemsize
		# create array type pointing to same memory
		ArrayType = new_type * new_length
		addr = ctypes.addressof(self._buf)
		new_buf = ArrayType.from_address(addr)
		return CArray(new_length, new_type, _buf=new_buf, _owner=self._owner)

	# ---- representation ----
	def items(self):
		return list(self)

	@property
	def format(self):
		return getattr(self.ctype, "__name__", str(self.ctype))


	def __repr__(self):
		return f"CArray(len={self.length}, type='{self.format}')"

	# ---- from pointer ----

	@classmethod
	def from_pointer(cls, ptr, typ, length):
		if not is_ctype_type(typ):
			raise TypeError("typ must be a ctypes type")
		if isinstance(ptr, int):
			addr = ptr
		elif isinstance(ptr, ctypes.c_void_p):
			addr = ptr.value
		else:
			raise TypeError("ptr must be int or ctypes.c_void_p")
		ArrayType = typ * length
		buf = ArrayType.from_address(addr)
		return cls(length, typ, _buf=buf, _owner=None)

	@classmethod
	def string(cls, string):
		c = cls(len(string), i8)
		c[:] = string
		return c
