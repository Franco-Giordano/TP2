import os 
import re

for cosa in os.walk("."):
        a = re.split("\W+",cosa[0])
        a.remove("")
        print(a)


print("xd")