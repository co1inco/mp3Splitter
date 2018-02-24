

filename = "QwebEpic Hits _ The Best of Album Kill la Kill OST _ 1-hour Epic Music Mix _ Epic Hybrid.mp3" 

artist = u"Sawano Hiroyuki & Cyua & Benjamin Anderson & Mika Kobayashi"
album = u"Kill la Kill [Best Off]"
genre = "Soundtrack"
date = "24.02.2018"
imageFront = "cover.jpg"
imageBack = ""
imageDesc = "---"
                # set type in splits.txt whith the first line: "type:(number)"
splitType = 1	# type1: (dosn't matter) - (Name) - 00:00:00
		# type2: 0:00:00-0:00:00 - (Name)
                # type3: 0:00 (name) [time 0:00 to 00:00:00 possible]
                # type4: 0:00 - (name)      -||-



from pydub import AudioSegment
import eyed3
import os

if imageFront == "":
    if os.path.isfile("cover.png"):
        imageFront = "cover.png"
    elif os.path.isfile("cover.jpg"):
        imageFront = "cover.jpg"


print("Start!")

splits = open("splits.txt", "r")
line = splits.readline()
i = line.find("type:")
if  i > -1:
    splitType = int(line[i+5])
    print("Type: " + line[i+5])
else:
    splits = open("splits.txt", "r")
    

names = []
times = []

def type3(line, splitSymbol=" "):
    split1 = line.find(splitSymbol)
    time = line[:split1]
    tmpSec = time[-4:]
    tmpMin2 = "0"
    tmpHour = "0"
    if split1 > 4:
        tmpMin2 = time[0]
        if split1 > 6:
            tmpHour = time[-7]
    time = "0" + str(tmpHour) + ":" + str(tmpMin2) + str(tmpSec)
    name = line[split1+len(splitSymbol):]
    if name.find("\n") >= 0:
        name = name[:-1]
    return name, time
    

for i in splits:
    print("Split for \"" + i + "\"")
    print(splitType)

    addmils = 0

    if splitType == 1:
        start = i.find("-")
        start = start + 2
        i2 = i[start:]
        end = i2.find("-")
        number = i[1:start-1]
        name = i2[:end-1]
        if i2.find("\n") >= 0:
            time = i2[end+2:-1]
        else:
            time = i2[end+2:]
			
    elif splitType == 2:
        split1 = i.find("-")
        if split1 < 0:
            continue #no "-" when line emty
        i2 = i[split1+1:]
        split2 = i2.find("-")
        time = i[:split1]
        time = "0" + time
        if i2.find("\n") >= 0:
            name = i2[split2+2:-1]
        else:
            name = i2[split2+2:]
        addmils = 500

    elif splitType == 3:
        name, time = type3(i)
    elif splitType == 4:
        name, time = type3(i, " - ")

    hour = time[0:2]  # changed 0 to 1. change back when problem
    mins = time[3:5]
    sec  = time[6:8]
    hour = int(hour)
    mins = int(mins)
    sec  = int(sec)

    milisec = hour * 3600000
    milisec = milisec + mins * 	60000
    milisec = milisec + sec * 1000
    milisec = milisec + addmils
    
    
    names.append(name)
    times.append(milisec)
splits.close()

"""    
for i in names:
    print(i)
os._exit(0)
"""

song = AudioSegment.from_mp3(filename)

for i, name in enumerate(names):

    if name == "---": #if ffmpeg encode failes skipp it here
        print("---SKIPING---")
        continue
    
    print("working on \"" + name + "\"")

    if not os.path.isfile("output/" + name + ".mp3"):
        start = times[i]
        try:
            end = times[i+1]
            title = song[start:end]
        except IndexError:
            title  = song[start:]

        title.export("output/" + name + ".mp3", format="mp3")

    file = eyed3.load("output/" + name + ".mp3")

    file.tag.artist = artist
    file.tag.album = album
    file.tag.title = name
    file.tag.genre = genre
    file.tag.track_num = i + 1

       
    if imageFront != "":
        imagefile = open(imageFront, "rb").read()
        if imageFront.find(".png"):
            file.tag.images.set(3, imagefile, "image/png", imageDesc)
        else:
            file.tag.images.set(3, imagefile, "image/jpeg", imageDesc)

    if imageBack != "":
        img = open(imageBack, "rb")
        imagefile = img.read()
        img.close()
        if imageBack.find(".png"):
            file.tag.images.set(4, imagefile, "image/png", u"-")
        else:
            file.tag.inages.set(4, imageFfile, "image/jpeg", u"-")

    file.tag.save()

#print("ready!") 
input("READY!") 


#for i in names:
#    print(i)
#for i in times:
#    print(i)
    
#print(names)
#print(times)
