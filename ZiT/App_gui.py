#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os.path
import struct
import sys
from Generator import Generator
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


# create the root window
root = tk.Tk()
root.title('Open File Dialog')
root.resizable(False, False)
root.geometry('500x250')
root.config(bg='grey', )
entry = tk.Entry(root, font=40)

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


def _get_e_machine(header: bytes) -> int:
    if header[0x05] == 1:
        endianness = "<"
    else:
        endianness = ">"

    _, machine = struct.unpack(f"{endianness}16xHH", header)

    return machine


def open_file():
    path = entry.get()
    argv = os.path.basename(path)
    # read the elf
    with open(path, "rb") as elf_file:
        elf = elf_file.read()

    code_generator = Generator()

    target_architecture = _get_e_machine(elf[:20])
    # map to syscall number
    syscall = syscall_numbers.get(target_architecture)

    code_generator.syscall = syscall
    filename = os.path.basename(path)
    filename = filename.split('.')[0]
    out = code_generator.generate_code(elf, argv)
    with open(os.path.join(os.path.dirname(path), 'output_{}.py'.format(filename)), 'w+') as file:
        file.write(out)
    showinfo(
        title='Info',
        message="File opened successfully as output_{}.py".format(filename)
    )
    entry.get()


def select_file():
    clear_text()
    filetypes = (
        ('All files', '*'),
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    entry.insert(tk.END, filename)


def clear_text():
    entry.delete(0, 'end')

# select button
select_button = ttk.Button(
    root,
    text='Select file to open',
    command=select_file
)

# open button
open_button = ttk.Button(
    root,
    text='Run',
    command=open_file
)


select_button.pack(expand=True)
open_button.pack(expand=True)
entry.pack()




# run the application
root.mainloop()
