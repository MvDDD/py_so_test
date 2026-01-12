#!/usr/bin/env python3
import sys
import os
import ctypes
import re
from collections import namedtuple
from pycparser import parse_file, c_ast

# -------------------------
# Data models
# -------------------------
TypeDef = namedtuple("TypeDef", ["name", "ctype"])
StructDef = namedtuple("StructDef", ["name", "fields"])
FuncDef = namedtuple("FuncDef", ["name", "args", "ret"])


# -------------------------
# Helpers
# -------------------------

typemap = {
        "char": "i8",
        "signed char": "i8",
        "unsigned char": "u8",
        "short": "i16",
        "short int": "i16",
        "unsigned short": "u16",
        "int": "i32",
        "unsigned int": "u32",
        "long": "i64",
        "long int": "i64",
        "unsigned long": "u64",
        "long long": "i64",
        "unsigned long long": "u64",
        "float": "f32",
        "double": "f64",
        "long double": "f80",
        "void": "void",

        # Fixed-width types
        "int8_t": "i8",
        "uint8_t": "u8",
        "int16_t": "i16",
        "uint16_t": "u16",
        "int32_t": "i32",
        "uint32_t": "u32",
        "int64_t": "i64",
        "uint64_t": "u64",

        "size_t" :"u64",
        "ssize_t" :"i64",
        "pid_t" :"i32",
        "uid_t" :"i32",
        "gid_t" :"i32",
        "off_t" :"i64",
        "ino_t" :"u64",
        "dev_t" :"u64",
        "time_t" :"i64",
        "suseconds_t" :"i64",
        "intptr_t" :"i64",
        "uintptr_t" :"u64",
}

def clean_type(ctype, pointer=0):
    t = typemap.get(ctype, ctype)
    if pointer:
        return ("ptr<"*pointer) + str(t) + (">"*pointer)
    return t

def get_type_name(typ):
    """Recursively count pointer levels in a pycparser type."""
    count = 0
    while isinstance(typ, c_ast.PtrDecl):
        count += 1
        typ = typ.type  # unwrap pointer

    # typ is now the base type
    if isinstance(typ, c_ast.TypeDecl):
        return count, " ".join(typ.type.names)
    elif isinstance(typ, c_ast.Struct):
        return count, typ.name or ""
    else:
        return count, str(type(typ))




def process_struct(node):
    name = node.name
    fields = []
    if hasattr(node, 'decls') and node.decls:
        for decl in node.decls:
            depth, tname = get_type_name(decl.type)
            fname = decl.name
            fields.append((fname, clean_type(tname, depth)))
    return name, fields

def process_func(decl_node):
    func_decl = decl_node.type
    ret_type = get_type_name(func_decl.type)
    ret_type = clean_type(ret_type[1], ret_type[0])
    args = []
    if func_decl.args:
        for param in func_decl.args.params:
            depth, tname = get_type_name(param.type)
            args.append((param.name, clean_type(tname, depth)))
    return decl_node.name, args, ret_type

def resolve_type(type, classes, structs):
    if type.startswith("ptr<"):
        return f"ptr({resolve_type(type[4:-1], classes, structs)})"
    elif type in classes:
        return f"{type}.Struct"
    elif type in structs:
        return f"{type}"
    else:
        return type
# -------------------------
# Parser for .def file
# -------------------------
def parse_def_file(path):
    types, structs, funcs = {}, {}, {}
    current_struct = None

    with open(path) as f:
        for line in f:
            line = line.split('#')[0].strip()
            if not line:
                continue

            # type alias
            m = re.match(r"type\s+(\w+)\s*=\s*(\w+)", line)
            if m:
                name, ctype = m.groups()
                types[name] = TypeDef(name, ctype)
                continue

            # struct start
            m = re.match(r"struct\s+(\w+)\s*{", line)
            if m:
                current_struct = m.group(1)
                structs[current_struct] = StructDef(current_struct, [])
                continue

            # struct field
            m = re.match(r"((?:ptr<)*\w+(?:>)*)\s+(\w+)", line)
            if m and current_struct:
                t, n = m.groups()
                structs[current_struct].fields.append((n, t))
                continue

            # end struct
            if line == "}":
                current_struct = None
                continue

            # function
            m = re.match(r"func\s+(\w+)\s*\((.*?)\)\s*->\s*((?:ptr<)*\w+(?:>)*)(?:\s+)?", line)
            if m:
                name, argstr, ret = m.groups()
                args = []
                if argstr.strip():
                    for a in argstr.split(','):
                        aname, atype = a.strip().split(':')
                        args.append((aname.strip(), atype.strip()))
                funcs[name] = FuncDef(name, args, ret)
                continue

    return types, structs, funcs

# -------------------------
# Generate Python wrapper
# -------------------------

def generate_python_class(types, structs, funcs, dll_path):
    """
    Generates Python wrapper code for all structs and functions in a library.

    - Promoted structs (have methods) become Python classes with nested Struct
    - Non-promoted structs live in global space as ctypes.Structure
    - Struct references inside promoted structs use OtherClass.Struct
    """
    code = ""
    code += "import ctypes\n"
    code += f"dll = ctypes.CDLL('{dll_path.replace("\\", "/")}')\n\n"
    code += "\n"

    code += "i8 = ctypes.c_int8\n"
    code += "u8 = ctypes.c_uint8\n"
    code += "i16 = ctypes.c_int16\n"
    code += "u16 = ctypes.c_uint16\n"
    code += "i32 = ctypes.c_int32\n"
    code += "u32 = ctypes.c_uint32\n"
    code += "i64 = ctypes.c_int64\n"
    code += "u64 = ctypes.c_uint64\n"
    code += "f32 = ctypes.c_float\n"
    code += "f64 = ctypes.c_double\n"
    code += "f80 = ctypes.c_longdouble\n"
    code += "void = None\n"
    code += "\n"

    code += "sizeof = ctypes.sizeof"
    code += "\n"
    code += "def ptr(typ):\n"
    code += "    if typ==None:\n"
    code += "        return ctypes.c_void_p\n"
    code += "    c = ctypes.POINTER(typ)\n"
    code += "    c.size = ctypes.sizeof(ctypes.c_void_p)\n"
    code += "    return c\n"

    classes = {}
    unboundfuncs = {}
    for func, define in funcs.items():
        classname = func.split("_")[0]
        funcname = "_".join(func.split("_")[1:])
        if funcname and (classname in structs):
            if classname in classes: 
                classes[classname][funcname] = define
            else:
                classes[classname] = {funcname:define}
        else:
            unboundfuncs[func] = define
    classdefs = {k:v for k,v in structs.items() if k in classes}
    structs = {k:v for k,v in structs.items() if k not in classes}
    for name, struct in structs.items():
        code += "#struct\n"
        code += f"class {name}(ctypes.Structure):\n"
        code += "    _fields_ = [\n"
        for fname,type in struct.fields:
            code += f"        (\"{fname}\", {resolve_type(type, classes, structs)}),\n"
        code += "    ]\n\n"
        code += "    def __repr__(self):\n"
        contents = [f"(\"{k}\", self.{k})"
            for k,v in struct.fields
        ]
        code += f"        contents_array = [{", ".join(contents)}]\n"
        code += f"        string = \", \".join(f\"{{k}}:{{v}}\" for k,v in contents_array)\n"
        code += f"        return f\"<{name} {{{{{{string}}}}}}>\"\n"

    for classname, methods in classes.items():
        cldef = classdefs[classname]
        code += f"class {classname}:\n"
        code += f"    class Struct(ctypes.Structure):\n"
        code += f"        _fields_ = [\n"
        for field in cldef.fields:
            code += f"{" "*12}(\"{field[0]}\", {resolve_type(field[1], classes, structs).replace(f"ptr({classname}.Struct)", f"{classname}.Struct_LP")}),\n"
        code += f"        ]\n    \n"
        code += f"    Struct_LP = ctypes.POINTER(Struct)\n"
        code += f"    c__error = dll.{classname}__error\n"
        code += f"    c__error.argtypes = [Struct_LP]\n"
        code += f"    c__error.restype = i32\n"
        for funcname, func in {k:v for k,v in methods.items() if not k in ["_error"]}.items():
            code += f"    c_{funcname} = dll.{classname}_{funcname}\n"
            code += f"    c_{funcname}.argtypes = [{", ".join(resolve_type(arg[1], classes, structs).replace(f"ptr({classname}.Struct)", f"Struct_LP") for arg in func.args)}]\n"
            code += f"    c_{funcname}.restype = {resolve_type(func.ret, classes, structs).replace(f"ptr({classname}.Struct)", f"Struct_LP")}\n"
        code += "\n"
        code += "    @staticmethod\n"
        code += "    def init_from(struct_instance):\n"
        code += f"        if not isinstance(struct_instance, {classname}.Struct):\n"
        code += f"            raise TypeError(\"init_from requires a {classname}.Struct instance\")\n"
        code += f"        instance = object.__new__({classname})\n"
        code += f"        instance._struct = {classname}.Struct_LP()\n"
        code += f"        instance._struct.contents = struct_instance\n"
        code += f"        return instance\n"
        code += "\n"

        if "create" in methods:
            args = methods["create"].args[1:]
        if "create" in methods:
            code += (f"    def __init__(self)" if not len(args) else \
                     f"    def __init__(self, {", ".join(arg[0]+f"={resolve_type(arg[1], classes, structs)}()" for arg in args)})") + ":\n"
        else:
            code += f"    def __init__(self):\n"
        code     += f"        self._struct = {classname}.Struct_LP()\n"
        code     += f"        self._struct.contents = {classname}.Struct()\n"
        if "create" in methods:
            code += (f"        self.c_create(self._struct)" if not len(args) else \
                     f"        self.c_create(self._struct, {", ".join(arg[0] for arg in args)})") + "\n"
        code += f"        error = self.c__error(self._struct)\n"
        code += f"        if error: raise MemoryError(f\"{classname}.create failed with code {{error}}\")\n"
        if "destroy" in methods:
            code += f"    def __del__(self):\n"
            code += f"        self.c_destroy(self._struct)\n"
            code += f"        error = self.c__error(self._struct)\n"
            code += f"        if error: raise MemoryError(f\"{classname}.destroy failed with code {{error}}\")\n"
            code += f"\n"

        for name, method in {k:v for k,v in methods.items() if not k in ["create","destroy", "_error"]}.items():
            args = method.args[1:]
            if not args:
                code += f"    def {name}(self):\n"
                code += f"        retval = self.c_{name}(self._struct)\n"
                code += f"        error = self.c__error(self._struct)\n"
                code += f"        if error: raise MemoryError(f\"{classname}.{name} failed with code {{error}}\")\n"
                code += f"        return retval\n"
            else:
                arg_defs = ", ".join(f"{arg[0]}={resolve_type(arg[1], classes, structs).replace(f"{classname}.", "")}()" for arg in args)
                code += f"    def {name}(self, {arg_defs}):\n"
                arg_names = ", ".join(arg[0] for arg in args)
                code += f"        retval = self.c_{name}(self._struct, {arg_names})\n"
                code += f"        error = self.c__error(self._struct)\n"
                code += f"        if error: raise MemoryError(f\"{classname}.{name} failed with code {{error}}\")\n"
                code += f"        return retval\n"
            code += f"\n"
        for name, type in cldef.fields:
            if name == "_error": continue
            code += f"    @property\n"
            code += f"    def {name}(self): return self._struct.contents.{name}\n"
            code += f"    @{name}.setter\n"
            code += f"    def {name}(self, value): self._struct.contents.{name} = value\n"
            code += "\n"
        code += "    def __repr__(self):\n"
        contents = [f"(\"{k}\", self._struct.contents.{k})"
            for k,v in cldef.fields
        ]
        code += f"        contents_array = [{", ".join(contents)}]\n"
        code += f"        string = \", \".join(f\"{{k}}:{{v}}\" for k,v in contents_array)\n"
        code += f"        return f\"<{classname} {{{{{{string}}}}}}>\"\n"
        code += "\n"
    for name, fdef in unboundfuncs.items():
        code += f"{name} = dll.{name}\n"
        code += f"{name}.argtypes = [{", ".join(resolve_type(arg[1], classes, structs) for arg in fdef.args)}]\n"
        code += f"{name}.restype = {resolve_type(fdef.ret, classes, structs)}\n"
    return code

# -------------------------
# Main CLI
# -------------------------
def main(target_dir):
    # normalize path
    target_dir = os.path.abspath(target_dir)

    # folder name becomes library name
    lib_name = os.path.basename(target_dir)

    # header assumed to exist in the same folder
    header_path = os.path.join(target_dir, f"{lib_name}.h")

    #print("lib_name =", lib_name)
    #print("header_path =", header_path)
    #print("target_dir =", target_dir)

    init_file = os.path.join(target_dir, "__init__.py")
    with open(init_file, "w") as f:
        f.write("from ." + lib_name + " import *\n")


    # Step 1: parse header -> .def
    cpp_args= [
        '-D__attribute__(...)=',
        '-I./include',
        '-Dint8_t=signed char',
        '-Dint16_t=short',
        '-Dint32_t=int',
        '-Dint64_t=long long',
        '-Duint8_t=unsigned char',
        '-Duint16_t=unsigned short',
        '-Duint32_t=unsigned int',
        '-Duint64_t=unsigned long long',
        '-Dint_least8_t=int8_t',
        '-Dint_least16_t=int16_t',
        '-Dint_least32_t=int32_t',
        '-Dint_least64_t=int64_t',
        '-Duint_least8_t=uint8_t',
        '-Duint_least16_t=uint16_t',
        '-Duint_least32_t=uint32_t',
        '-Duint_least64_t=uint64_t',
        '-Dint_fast8_t=int8_t',
        '-Dint_fast16_t=int16_t',
        '-Dint_fast32_t=int32_t',
        '-Dint_fast64_t=int64_t',
        '-Duint_fast8_t=uint8_t',
        '-Duint_fast16_t=uint16_t',
        '-Duint_fast32_t=uint32_t',
        '-Duint_fast64_t=uint64_t',
        '-Dintptr_t=long',
        '-Duintptr_t=unsigned long',
        '-Dintmax_t=long long',
        '-Duintmax_t=unsigned long long',
    ]

    ast = parse_file(header_path, use_cpp=True, cpp_args=cpp_args)

    structs, funcs = {}, {}

    for ext in ast.ext:
        if isinstance(ext, c_ast.Typedef) and isinstance(ext.type.type, c_ast.Struct):
            sname, fields = process_struct(ext.type.type)
            if not sname:
                sname = ext.name
            structs[sname] = fields

        elif isinstance(ext, c_ast.Decl) and isinstance(ext.type, c_ast.FuncDecl):
            fname, args, ret = process_func(ext)
            funcs[fname] = (args, ret)

    # write .def file into same folder
    def_file = os.path.join(target_dir, f"{lib_name}.def")
    with open(def_file, "w") as f:
        for sname, fields in structs.items():
            f.write(f"struct {sname} {{\n")
            for fname, ftype in fields:
                f.write(f"    {ftype} {fname};\n")
            f.write("}\n\n")
        for fname, (args, ret) in funcs.items():
            argstr = ", ".join(f"{aname}:{atype}" for aname, atype in args)
            f.write(f"func {fname}({argstr}) -> {ret}\n")

    # Step 2: parse .def -> Python wrapper
    types, structs2, funcs2 = parse_def_file(def_file)

    py_file = os.path.join(target_dir, f"{lib_name}.py")
    with open(py_file, "w") as f:
        f.write(
            generate_python_class(
                types,
                structs2,
                funcs2,
                dll_path=os.path.join(target_dir, f"lib{lib_name}" + (".so" if os.name == "posix" else ".dll" if os.name == "nt" else ".dylib")),
            )
        )

if __name__ == "__main__":
    sys.argv.append("./nn2")
    if len(sys.argv) <= 2:
        print(f"Usage: {sys.argv[0]} /path/to/folder")
        sys.exit(1)

    main(sys.argv[1])
