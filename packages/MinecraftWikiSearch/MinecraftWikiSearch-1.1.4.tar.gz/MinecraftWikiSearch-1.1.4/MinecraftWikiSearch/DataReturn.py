import re
import sys
import urllib.parse
import urllib.request

from MinecraftWikiSearch.Errors import UnprocessedEntry
from MinecraftWikiSearch.JSONRead import EasyReturn
from MinecraftWikiSearch import Special_Entry
from MinecraftWikiSearch import WebVisit


def Clear(t):
    while True:
        if "wzh:" in t:
            text_copy = t
            start_index = text_copy.index("wzh:")
            end_index = text_copy.index("|")
            if start_index < end_index:
                del_str = text_copy[start_index:end_index + 1]
                t = t.replace(del_str, "")
            else:
                index = text_copy.index("|")
                index_N1 = index - 1
                text_copy = t
                while "|" in t:
                    char = t[index_N1:index]
                    if ord(char) >= 128:
                        GotIndex = text_copy.find(char)
                        GotIndex_R = text_copy.rfind(char)
                        if GotIndex_R == GotIndex:
                            break
                        else:
                            Before = abs(text_copy.index("|") - GotIndex)
                            After = abs(text_copy.index("|") - GotIndex_R)
                            if Before < After:
                                break
                            elif Before > After:
                                Ind = text_copy.index("|")
                                IndBefore = Ind - 10
                                if t[IndBefore:Ind] in Special_Entry.Special_Entry.Special_Entry:
                                    GotIndex = GotIndex_R
                                    break
                                else:
                                    raise UnprocessedEntry(
                                        "未经过本接口专门优化的词条，请及时反馈Bug（带上unprocessed entry标签，附上词条链接）")
                    else:
                        index -= 1
                        index_N1 -= 1
                del_str = text_copy[GotIndex + 1:text_copy.index("|") + 1]
                t = t.replace(del_str, "")
        else:
            break
    while True:
        if "wzh:" in t:
            text_copy = t
            start_index = text_copy.index("wzh:")
            end_index = text_copy.index("|")
            del_str = text_copy[start_index:end_index + 1]
            t = t.replace(del_str, "")
        else:
            break
    t = t.replace('wzh:', '')
    text = t.replace('|', '')
    return text


def DataReturn(entry):
    WebVisit.WebVisit(entry)
    FileText = open(sys.path[-1] + "Index.txt", encoding="utf-8")
    Wiki = FileText.readlines()
    for text in Wiki:
        if text[0:3] == "'''":
            if "<br>" not in text:
                text = re.sub(r'(https|http)?://(\w|\.|/|\?|=|&|%)*\b', "", text, flags=re.MULTILINE)
                text = re.compile(r'<[^>]+>', re.S).sub('', text)
                text = re.sub("[\[\]\'\n]", "", text)
                text = Clear(text)
                if not EasyReturn:
                    return [text, 'https://wiki.biligame.com/mc/' + urllib.parse.quote(entry)]
                else:
                    with open("return.txt", "w") as f:
                        f.write(text + "\n" + 'https://wiki.biligame.com/mc/' + urllib.parse.quote(entry))
                    return True
        elif text[0:13] == "{{ItemSprite|":
            text = re.sub("[\[\]\'\n]", "", text)
            text = re.sub("{.*?} ", "", text)[0:-1]
            text = Clear(text)
            if not EasyReturn:
                return [text, 'https://wiki.biligame.com/mc/' + urllib.parse.quote(entry)]
            else:
                with open("return.txt", "w") as f:
                    f.write(text + "\n" + 'https://wiki.biligame.com/mc/' + urllib.parse.quote(entry))
                return True
        elif text[0:4] == "#重定向":
            text = re.sub("[\[\]\'\n]", "", text)[5:]
            TEntry = text
            WebVisit.WebVisit(entry)
            FileText = open(sys.path[-1] + "Index.txt", encoding="utf-8")
            Wiki = FileText.readlines()
            for text in Wiki:
                if text[0:3] == "'''" and "<br>" not in text:
                    text = re.sub("[\[\]\'\n]", "", text)
                    text = re.sub(r'(https|http)?://(\w|\.|/|\?|=|&|%)*\b', "", text, flags=re.MULTILINE)
                    text = re.compile(r'<[^>]+>', re.S).sub('', text)
                    text = Clear(text)
                    if not EasyReturn:
                        return [text, '[重定向' + TEntry + ']https://wiki.biligame.com/mc/' + urllib.parse.quote(TEntry)]
                    else:
                        with open("return.txt", "w") as f:
                            f.write(text + "\n" + '[重定向' + TEntry + ']https://wiki.biligame.com/mc/' + urllib.parse.quote(TEntry))
                        return True
                elif text[0:13] == "{{ItemSprite|":
                    text = re.sub("[\[\]\'\n]", "", text)
                    text = re.sub("{.*?} ", "", text)[0:-1]
                    text = Clear(text)
                    if not EasyReturn:
                        return [text, '[重定向' + TEntry + ']https://wiki.biligame.com/mc/' + urllib.parse.quote(TEntry)]
                    else:
                        with open("return.txt", "w") as f:
                            f.write(text + "\n" + '[重定向' + TEntry + ']https://wiki.biligame.com/mc/' + urllib.parse.quote(TEntry))
                        return True
        elif text[0:4] == "#RED":
            TEntry = re.sub("[\[\]\'\n]", "", text)[10:]
            WebVisit.WebVisit(entry)
            FileText = open(sys.path[-1] + "Index.txt", encoding="utf-8")
            Wiki = FileText.readlines()
            for text in Wiki:
                if text[0:3] == "'''" and "<br>" not in text:
                    text = re.sub("[\[\]\'\n]", "", text)
                    text = re.sub(r'(https|http)?://(\w|\.|/|\?|=|&|%)*\b', "", text, flags=re.MULTILINE)
                    text = re.compile(r'<[^>]+>', re.S).sub('', text)
                    text = Clear(text)
                    if not EasyReturn:
                        return [text, '[重定向' + TEntry + ']https://wiki.biligame.com/mc/' + urllib.parse.quote(TEntry)]
                    else:
                        with open("return.txt", "w") as f:
                            f.write(text + '[重定向' + TEntry + ']https://wiki.biligame.com/mc/' + urllib.parse.quote(TEntry))
                        return True
                elif text[0:13] == "{{ItemSprite|":
                    text = re.sub("[\[\]\'\n]", "", text)
                    text = re.sub("{.*?} ", "", text)[0:-1]
                    text = Clear(text)
                    if not EasyReturn:
                        return [text, '[重定向' + TEntry + ']https://wiki.biligame.com/mc/' + urllib.parse.quote(TEntry)]
                    else:
                        with open("return.txt", "w") as f:
                            f.write(text + "\n" + '[重定向' + TEntry + ']https://wiki.biligame.com/mc/' + urllib.parse.quote(TEntry))
                        return True
