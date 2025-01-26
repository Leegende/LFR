import os
import subprocess
import re

# first is goal
toMergeSet = [61,101]
toMerge = list(set(toMergeSet))

path="./history/states/"

listt = os.listdir(path)
#listt.sort()

arges = ["java", "-jar", "pp.jar", "fotzenwolf.lua"]

def tryParse() -> str: 
    ret = subprocess.run(arges, capture_output=True)
    print(ret.stderr.decode("utf-8").replace("\r\n","\n"))
    return ret.stdout.decode("utf-8").replace("\r\n", "\n")

for i in listt:
    for s in toMerge:
        if re.match("^"+str(s)+"[^\\d]", i):
            arges.append(i)

print(arges)
content = tryParse()
print(content)
open("./history/states/" + arges[4],"w+", encoding="utf-8").write(content)

if True:
    for f in arges[5:]:
        os.remove("./history/states/" + f)