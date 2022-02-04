#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os.path
import struct
import sys
from Generator import Generator


def print_out(what: str) -> None:
    sys.stdout.write(what)
    sys.stdout.flush()


def _get_e_machine(header: bytes) -> int:
    if header[0x05] == 1:
        endianness = "<"
    else:
        endianness = ">"

    _, machine = struct.unpack(f"{endianness}16xHH", header)

    return machine


def main():
    syscall_numbers = {
        **dict.fromkeys(["autodetect", "libc"], -1),
        **dict.fromkeys(["386", 3], 356),
        **dict.fromkeys(["amd64", 62], 319),
        **dict.fromkeys(["arm", 40], 385),
        **dict.fromkeys(["arm64", "riscv64", 183], 279),
        **dict.fromkeys(["mips", 8], 4354),
        **dict.fromkeys(["mips64", "mips64le", 8], 5314),
        **dict.fromkeys(["ppc", "ppc64", 20], 360),
        **dict.fromkeys(["s390x", 22], 350),
        **dict.fromkeys(["sparc64", 2, 18, 43], 348),
    }

    parser = argparse.ArgumentParser(
        description="Print code to stdout to execute an ELF without dropping files."
    )
    parser.add_argument(
        "path",
        type=str,
        help="path to the ELF file ",
    )

    parser.add_argument(
        "-p",
        "--interpreter-path",
        metavar="PATH",
        help="path to interpreter on target if '-c' is used, otherwise a sane default is used",
    )

    args = parser.parse_args()

    argv = os.path.basename(args.path)

    # read the elf
    with open(args.path, "rb") as elf_file:
        elf = elf_file.read()

    code_generator = Generator()

    target_architecture = _get_e_machine(elf[:20])
    # map to syscall number
    syscall = syscall_numbers.get(target_architecture)

    code_generator.syscall = syscall

    out = code_generator.generate_code(elf, argv)

    print_out(out)


if __name__ == "__main__":
    sys.exit(main())
