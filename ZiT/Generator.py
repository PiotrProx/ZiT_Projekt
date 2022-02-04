import zlib
from base64 import b64encode


class Generator:
    def __init__(self) -> None:
        self.compression_level = 9
        self.wrap = 0
        self.syscall = None
        self.use_stdin = False
        self._generator = None

        self.output = ""
        self.prep_elf = self._prepare_elf
        self.wrap = self.wrap
        self.syscall = self.syscall
        self.use_stdin = self.use_stdin

    def _prepare_elf(self, elf: bytes) -> bytes:
        # compress the binary and encode it with base64
        compressed_elf = zlib.compress(elf, self.compression_level)
        encoded = b64encode(compressed_elf)

        return encoded

    def generate_code(self, elf: bytes, argv: str) -> str:
        self.add_header()
        self.add_elf(elf)
        self.add_dump_elf()
        self.add_call_elf(argv)
        return self.output

    def with_command(self, path="/usr/bin/env python") -> str:
        escaped = self.output.replace('"', '\\"')
        return f'{path} -Bc "{escaped}"'

    def add(self, line: str) -> None:
        self.output += f"{line}\n"

    def add_header(self) -> None:
        imports = "ctypes, os"
        if not self.use_stdin:
            imports += ", base64, zlib"
        self.add(f"import {imports}")
        self.add("l = ctypes.CDLL(None)")
        if self.syscall:
            self.add("s = l.syscall")
        else:
            self.add("s = l.memfd_create")

    def add_elf(self, elf: bytes) -> None:
        if self.use_stdin:
            self.add("from sys import stdin, version_info")
            self.add("if version_info >= (3, 0):")
            self.add(" e = stdin.buffer.read()")
            self.add("else:")
            self.add(" e = stdin.read()")
            return

        # prepare elf
        encoded = f"{self.prep_elf(elf)}"

        if self.wrap > 3:
            chars = self.wrap - 3
            length = len(encoded)
            encoded = "'\nb'".join(
                encoded[i: i + chars] for i in range(0, length, chars)
            )

        self.add(f"c = base64.b64decode(\n{encoded}\n)")
        self.add("e = zlib.decompress(c)")

    def add_dump_elf(self) -> None:
        # create the fd with no name
        if self.syscall:
            self.add(f"f = s({self.syscall}, '', 1)")
        else:
            self.add("f = s('', 1)")
        self.add("os.write(f, e)")

    def add_call_elf(self, argv: str) -> None:
        self.add("p = '/proc/self/fd/%d' % f")
        args = argv.strip()
        args = args.replace("'", "\\'")
        args = args.replace(" ", "', '")
        self.add(f"os.execle(p, '{args}', {{}})")
