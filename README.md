mp3 Spliting Tool

Need to run:

Tested with python 3.6

install with pip:

    -eyed3

      -libmagic
  
      -python_magic
  
      -python_magic_bin (windows)

    -pydub

----

-Input mp3 file

-splits.txt

        Format of a line:
  
        -Type 1: (something) - (Name of Track) - 00:00:00   Important are the dashes
  
        -Type 2: 0:00:00-0:00:00 - (Name of Track)          Important are the dashes, the sceond time in the line will be ignored

----

Optional:
  
  -Coverart (Tries cover.png/jpg if left blank
  
  -artist name, genre, releasedate, album name
  
  (uses the same data for every track)
  
  (change in the script)
