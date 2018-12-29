#!/bin/python

import sys
reload(sys)
import eyed3
from os import walk
from optparse import OptionParser
from collections import Counter
import os


parser = OptionParser()
parser.add_option("-t", "--type", dest="type",
                  help="set the directory type for save")
parser.add_option("-a", "--auto",
                  dest="auto", default=True,
                  help="Enable the automation for organizer")

(options, args) = parser.parse_args()



sys.setdefaultencoding('utf8')
fileFormat=('.mp3','m4a','.mpga', '.flac','.wma')
#file name collection
f = []
mypath="/home/kim415/test_dir/";
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break



#Collect a list of artist/album/title in series
ftotal =[]

for f1 in f:
#   print f1
   audio = eyed3.load(f1)

   if(audio != None):
      if(audio.tag != None):

        if(audio.tag.artist != None):
            artist = audio.tag.artist;
            artist = artist.split(' &')[0]
            artist = artist.split('/')[0]
        else:
            artist = 'None';
    
        if(audio.tag.album != None):
            album = audio.tag.album;
        else:
            album = 'None';
        
   
        if(audio.tag.title != None):
            title = audio.tag.title;
        else:
            title = 'None';
         
        ftotal.append([artist,album,title]);


ftotal_t = map(list, zip(*ftotal))

fresult0 = Counter(ftotal_t[0])
fresult1 = Counter(ftotal_t[1])
fresult0 = fresult0.most_common();
fresult1 = fresult1.most_common();


#Automation (i:Album, ii:Artist)
if(options.auto == True):
    n=0;
    count=100;
    while(count > 40):
        count = 0;
        if(int(fresult0[n][1]) > 40):
            count =int(fresult0[n][1]);
            if fresult0[n][0] != "None":
                cpath="/home/kim415/test_dir/"+fresult0[n][0] + "/";
            
            if not os.path.exists(cpath):
               os.mkdir(cpath);

            for f1 in f:
                audio = eyed3.load(f1)
                if(audio != None):
                   if(audio.tag != None):
                      if(audio.tag.artist != None):
                         artist = audio.tag.artist.lower();
                         artist = artist.split(' &')[0]
                         artist = artist.split('/')[0]
                         artist = artist.lower();
                         if(artist == fresult0[n][0].lower() and f1.lower().endswith(fileFormat)):
                             msrc=mypath+f1;
                             mdest=cpath+f1;
                             os.rename(msrc,mdest)
            f = []
            mypath="/home/kim415/test_dir/";
            for (dirpath, dirnames, filenames) in walk(mypath):
               f.extend(filenames)
               break



        if(int(fresult1[n][1]) > 40):
            count =int(fresult1[n][1]); 
            if fresult1[n][0] != "None":
               cpath="/home/kim415/test_dir/"+fresult1[n][0] + "/";
            if not os.path.exists(cpath):
               os.mkdir(cpath);

            for f1 in f:
                audio = eyed3.load(f1)
                if(audio != None):
                   if(audio.tag != None):
                      if(audio.tag.album != None):
                         album = audio.tag.album;
                         album = album.lower();
                         if(album == fresult1[n][0].lower() and f1.lower().endswith(fileFormat)):
                             msrc=mypath+f1;
                             mdest=cpath+f1;
                             os.rename(msrc,mdest)
            f = []
            mypath="/home/kim415/test_dir/";
            for (dirpath, dirnames, filenames) in walk(mypath):
               f.extend(filenames)
               break

        n += 1;



#Move to the rest of files into Various_Artists folder
cpath="/home/kim415/test_dir/Various_Artists/";
if not os.path.exists(cpath):
   os.mkdir(cpath);

for f1 in f:

    if f1.lower().endswith(fileFormat):
       msrc=mypath+f1;
       mdest=cpath+f1;
       os.rename(msrc,mdest)
