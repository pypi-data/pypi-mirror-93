import sys

from MinecraftWikiSearch.Errors import ArgsError
from MinecraftWikiSearch.JSONRead import EasyInput
from MinecraftWikiSearch.DataReturn import DataReturn


# 主函数
def main(arg=None):
    if EasyInput:
        File = open("wiki.txt", "r", encoding="utf-8").read()
        Return = DataReturn(File)
        return Return
    else:
        if len(sys.argv) < 2 and arg is None:
            raise ArgsError("没有传入参数")
        else:
            try:
                return DataReturn(sys.argv[1])
            except IndexError:
                return DataReturn(arg)


if __name__ == '__main__':
    args = input(">>> ")
    print(main(arg=args))
