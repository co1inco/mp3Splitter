from pydub import AudioSegment
import eyed3
import os

filename = "Qweb[OST] Top Fairy Tail.mp3" 

artist = u"Yasuharu Takanashi"
album = u"Sad Collection"
genre = "Soundtrack"
date = "31.12.2016"
imageFront = "cover.png"
imageBack = ""
imageDesc = "---"

splitType = 2	# type1: (dosn't matter) - (Name) - 00:00:00
		# type2: 0:00:00-0:00:00 - (Name)

if imageFront == "":
    if os.path.isfile("cover.png"):
        imageFront = "cover.png"
    elif os.path.isfile("cover.jpg"):
        imageFront = "cover.jpg"


print("Start!")

try:
    os.mkdir("output")
except:
    pass

splits = open("splits.txt", "r")

names = []
times = []

for i in splits:
    print("Split for \"" + i + "\"")

    admils = 0

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
    


song = AudioSegment.from_mp3(filename)

for i, name in enumerate(names):

    print("working on \"" + name + "\"")

    if not os.path.isfile(name + ".mp3"):
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

print("ready!")  


#for i in names:
#    print(i)
#for i in times:
#    print(i)
    
#print(names)
#print(times)
