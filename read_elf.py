#!env python3
# encoding = utf-8

import elf
import sys
import getopt
from tabulate import tabulate


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        printusag()
        sys.exit(2)

    filepath = args[0]
    ef = elf.ELF(filepath)

    for opt, arg in opts:
        if opt == '-h':
            printelfhead(ef)


def printelfhead(ef):
    print("ELF Header:")
    indent = ef.elf_head.e_ident
    print("  Magic:   {}".format(hexstr(indent)))
    tablep = []
    tablep.extend([
        ["Number of program headers:", len(ef.p_headers)],
        ["  Number of section headers:", len(ef.p_headers)]
    ]
    )
    print("  " + tabulate(tablep, tablefmt='plain'))


def hexstr(s):
    return " ".join(["{:02x}".format(c) for c in s])


def printusag():
    print("Usage: read_elf.py option elf-file")
    print(" Display impormation about the coennts of ELF format files")
    print(" Options are:")
    print(" -h Display the ELF file header")


if __name__ == "__main__":
    main(sys.argv[1:])
