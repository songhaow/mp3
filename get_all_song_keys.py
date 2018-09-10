# import sys
#works okay is there are no envelops in the directory
import os
import sys
allkeys=os.listdir(".")
print ("AllProjects--------------------------")
for key in allkeys:
  print (key)
keysForMusic=[]

for key in allkeys:
    name=key.split(".")[0]
    sufname=key.split(".")[1]
    if(sufname=="mp3"):
      thismp3=name+".mp3"
      keysForMusic.append(thismp3)
    else: pass

fh1=open("KeysForMusic.txt", "w")
fh1.write('{ "The list of KeysForMusic": ')
fh1.write("\n")

print ("KeysForMusic-------------------------")
for key in keysForMusic:
  fh1.write(key)
  fh1.write("\n")
  print (key)
fh1.write("}")
fh1.close()
