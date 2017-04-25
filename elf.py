#!env python3
# encoding=utf-8
from pprint import pprint


class BaseSegment:
    offset = 0
    size = 0

    def __init__(self, f, offset, size):
        self.f = f
        self.offset = offset
        self.size = size
        self.f.seek(offset)

        self.content = self.f.read(size)
        self.f.seek(offset)

    def readInt(self, size):
        return int.from_bytes(self.f.read(size), byteorder='little')

    def read16Int(self):
        return self.readInt(2)

    def read32Int(self):
        return self.readInt(4)

    def readstr(self, size):
        return str(self.f.read(size))

    def prettyp(self):
        vardict = vars(self)
        vardict.pop("content", None)
        vardict.pop("f", None)
        pprint(vardict)


class ELF:
    """整个ELF文件
    会将整个文件读成一个elf对象
    """
    def __init__(self, filePath):
        f = open(filePath, "r+b")
        self.elf_head = ELFHead(f)
        self.program_head_table = HeaderTable(f, self.elf_head.e_phnum,
                                              self.elf_head.e_phoff,
                                              self.elf_head.e_phentsize)

        self.section_head_table = HeaderTable(f, self.elf_head.e_shnum,
                                              self.elf_head.e_shoff,
                                              self.elf_head.e_shentsize)

        self.elf_head.prettyp()
        # print(self.elf_head)
        # print(self.program_head_table)
        # print(self.section_head_table)


class ELFHead(BaseSegment):
    """文件头
    """
    def __init__(self, f):
        super().__init__(f, 0, 52)
        self.e_ident = self.readstr(16)
        self.e_type = self.read16Int()
        self.e_machine = self.read16Int()
        self.e_version = self.read32Int()
        self.e_entry = self.read32Int()
        self.e_phoff = self.read32Int()
        self.e_shoff = self.read32Int()
        self.e_flags = self.read32Int()
        self.e_ehsize = self.read16Int()
        self.e_phentsize = self.read16Int()
        self.e_phnum = self.read16Int()
        self.e_shentsize = self.read16Int()
        self.e_shnum = self.read16Int()
        self.e_shstrndx = self.read16Int()

    def add_one_shnum():
        pass


class SectionHeader(BaseSegment):
    def __init__(self, f, offset, size):
        super().__init__(f, offset, size)
        self.sh_name = self.read32Int()
        self.sh_type = self.read32Int()
        self.sh_flags = self.read32Int()
        self.sh_addr = self.read32Int()
        self.sh_offset = self.read32Int()
        self.sh_size = self.read32Int()
        self.sh_link = self.read32Int()
        self.sh_info = self.read32Int()
        self.sh_addralign = self.read32Int()
        self.sh_entsize = self.read32Int()


class HeaderTable(BaseSegment):
    def __init__(self, f, e_num, e_off, e_entsize):
        super().__init__(f, e_off, e_num * e_entsize)
        self.headers = []
        for i in range(0, e_num):
            self.headers.append(
                SectionHeader(f, e_off + i * e_entsize, e_entsize))


class Section(BaseSegment):
    pass


# class Section1:
#     def __init__(self, file_content, offset, size):
#         self.file_content = file_content
#         self.offset = offset
#         self.size = size


# class SNameSection(Section1):
#     """section名称的section"""
#     def __init__(self, file_content, offset, size):
#         Section1.__init__(self, file_content, offset, size)
#         self.names = []
#         s_begin = offset
#         self.offset = offset
#         for i in range(offset, offset + size):
#             cs = file_content[i: i + 1]
#             if cs == b'\x00':
#                 self.names.append(file_content[s_begin: i + 1].decode("ascii"))
#                 s_begin = i + 1

#     def get_name_by_index(self, index):
#         begin = self.offset + index
#         end = begin
#         while self.file_content[end: end + 1] != b'\x00':
#             end += 1

#         return self.file_content[begin: end].decode("ascii")

#     def __str__(self):
#         return str(vars(self))


# def byteArr2Int(s):
#     """将byte数组转成int
#     """
#     return int.from_bytes(s, byteorder="little", signed=False)


# def getInt(filecontent, startI, endI):
#     return byteArr2Int(filecontent[startI: endI + 1])


TEST_FILE_PATH = "/Users/yi/source/android-ndk/hello-jni/app/build/intermediates/cmake/arm7/debug/obj/armeabi-v7a/libother-hello.so"

if __name__ == "__main__":
    ELF(TEST_FILE_PATH)
