# import sys
#works okay is there are no envelops in the directory
import os
allfiles=os.listdir()
print ("ALLFILES--------------------------")
for filename in allfiles:
  print (filename)
mp3files=[]

for filename in allfiles:
    name=filename.split(".")[0]
    sufname=filename.split(".")[1]
    if(sufname=="mp3"):
      thismp3=name+".mp3"
      mp3files.append(thismp3)
    else: pass

print ("MP3 FILES-------------------------")
for filename in mp3files:
  print (filename)
