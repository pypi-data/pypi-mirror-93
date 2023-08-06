import os
import platform
import sys


if platform.platform()[0:7] == "Windows":
    sys.path.append(os.getcwd() + "\\")
else:
    sys.path.append(os.getcwd() + "/")