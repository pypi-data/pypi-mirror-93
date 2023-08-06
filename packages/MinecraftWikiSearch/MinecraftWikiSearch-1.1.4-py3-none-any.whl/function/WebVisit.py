import sys
import urllib.parse
import urllib.request

from JSONRead import FastLoad


def WebVisit(Entry):
    fileUrl = urllib.parse.quote(Entry)
    if FastLoad:
        url = r'https://wiki.biligame.com/mc/index.php?title=' + fileUrl + "&action=raw"
    else:
        url = r'https://minecraft-zh.gamepedia.com/index.php?title=' + fileUrl + "&action=raw"
    res = urllib.request.urlopen(url)
    htmlFile = res.read().decode('utf-8')
    with open(sys.path[-1] + "Index.txt", "w", encoding='utf-8') as f:
        f.write(htmlFile)
    return True
