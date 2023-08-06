import json
import os
import re
import urllib.parse
import urllib.request
import sys

from bs4 import BeautifulSoup


class ArgsError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


def Info(text):
    fileUrl = urllib.parse.quote(text)
    if FastLoad:
        url = r'https://wiki.biligame.com/mc/' + fileUrl
    else:
        url = r'https://minecraft-zh.gamepedia.com/' + fileUrl
    res = urllib.request.urlopen(url)
    htmlFile = res.read().decode('utf-8')
    with open("Index.html", "w", encoding='utf-8') as f:
        f.write(htmlFile)

    soup = BeautifulSoup(open("Index.html", encoding='utf-8'))
    for tag in soup.find_all("p"):
        if str(tag)[0:6] == "<p><b>":
            if tag.parent.parent.parent.name == "tbody":
                continue
            else:
                break
        elif str(tag)[0:6] == "<p><sp":
            if tag.parent.parent.parent.name != "tbody":
                rd = re.compile(r'<[^>]+>', re.S)
                to = rd.sub('', str(tag))
                dr = re.sub(r"\[.*?]", "", to)
                if EasyReturn:
                    with open("return.txt", "w", encoding='utf-8') as f:
                        f.write(dr)
                        if dr[-1:] == "\n":
                            f.write(url)
                        else:
                            f.write("\n" + url)
                    return True
                else:
                    return [dr, url]
    html = str(tag)
    rd = re.compile(r'<[^>]+>', re.S)
    to = rd.sub('', html)
    dr = re.sub("\\[.*?]", "", to)
    if EasyReturn:
        with open("return.txt", "w", encoding='utf-8') as f:
            f.write(dr)
            if dr[-1:] == "\n":
                f.write(url)
            else:
                f.write("\n" + url)
            os.remove("Index.html")
        return True
    else:
        os.remove("Index.html")
        return [dr, url]


# 主函数
def main(arg=None):
    if os.path.exists('config.json'):
        file = open('config.json', 'r')
        content = file.read()
    else:
        Config = {
            "FasterLoad": True,
            "EasyInput": False,
            "EasyReturn": False
        }
        with open('config.json','w') as f:
            json.dump(Config, f)
    Dict = json.loads(content)
    EasyInput = Dict["EasyInput"]
    global EasyReturn
    EasyReturn = Dict["EasyReturn"]
    global FastLoad
    FastLoad = Dict["FasterLoad"]
    file.close()
    if EasyInput:
        File = open("wiki.txt", "r", encoding="utf-8").read()
        Return = Info(File)
        return Return
    else:
        if len(sys.argv) < 2 and arg is None:
            raise ArgsError("没有传入参数")
        else:
            try:
                return Info(sys.argv[1])
            except IndexError:
                return Info(arg)


if __name__ == '__main__':
    args = input()
    print(main(arg=args))
