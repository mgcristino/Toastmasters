# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Movie Splitter
import os
import argparse
import sys
import time 
import os.path
import time
import re
from datetime import datetime
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def is_valid_file(parser, arg):
    """
    Check if arg is a valid file that already exists on the file system.

    Parameters
    ----------
    parser : argparse object
    arg : str

    Returns
    -------
    arg
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--config",
                        dest="configFile",
                        type=lambda x: is_valid_file(parser, x),
                        help="Configuration File",
                        metavar="FILE",
                        required=True)
    parser.add_argument("-s", "--source",
                        dest="sourceDir",
                        type=lambda x: is_valid_file(parser, x),
                        help="Source Directory with Clips to Split",
                        metavar="Directory",
                        required=True)
    parser.add_argument("-o", "--output",
                        dest="outputDir",
                        type=lambda x: is_valid_file(parser, x),
                        help="Output Directory for Clips Segments",
                        metavar="Directory",
                        required=True)    
    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        dest="verbose",
                        default=True,
                        help="don't print status messages to stdout")
    return parser

def printf (format,*args):
	sys.stdout.write (format % args)

def fileExists (file_path):
    return os.path.exists(file_path)

def time_to_sec(time_str):
    return sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time_str.split(":"))))
  
def isValidClip (fileName):
    
    if not fileName.lower().endswith('.mp4'):
	printf ("Line %s - File %s is not MP4\n",lineNr,fileName)
    elif not fileExists (fileName):
	printf ("Line %s - File %s does not exists\n",lineNr,fileName)
    else:
	return True
        
    return False
    
def isValidSegments (segments):
    
    for segment in segments:
	#print segment + "\n"
	try:
	    if (re.match("(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)",segment)):
		time.strptime(segment, "%H:%M:%S")
	    else:
		time.strptime(segment, "%M:%S")
	except ValueError:
	    printf ("Line %s - Segment %s format is invalid\n",lineNr,segment)
	    return False
	
    return True

def split_file(file_path):
    if os.path.isfile(file_path):
	return os.path.splitext(os.path.basename(file_path))[0]
    
def extractClip(clipMovie, segments, outputDir):
    clipNbr = 0
    segmentIni = segments[0]
    clipName = split_file(clipMovie)
    clipTime = os.path.getmtime(clipMovie)
    
    for segment in segments[1:]:
	segmentFim = segment
	newClip = outputDir + "\\" + clipName + "_" + str(clipNbr).zfill(2) + ".MP4"
	printf ("Creating Segment %s from %s to %s\n",newClip,segmentIni,segmentFim)
	ffmpeg_extract_subclip(clipMovie, time_to_sec(segmentIni), time_to_sec(segmentFim), targetname=newClip)
	
	modTime = clipTime + time_to_sec(segmentIni)
	os.utime(newClip, (modTime, modTime))
	
	segmentIni = segment
	clipNbr += 1
	
def main():
    global lineNr
    lineNr = 0
    args = get_parser().parse_args()
	
    with open(args.configFile) as f:
        for line in f:
	    lineNr += 1
            if not line.strip().startswith('#'):
                data = line.strip().split(";")
		clip = data[0]
		segments = list(data[1:])
		fileName = args.sourceDir + "\\" + clip;
		#print clip
		#print segments
		if len(segments) < 1:
		    printf ("Line %s - Must have at least 2 define segments\n",lineNr)
		elif isValidClip(fileName) and isValidSegments(segments):
		    extractClip(fileName,segments,args.outputDir)
		    #print split_file(fileName)
		#print '{0};{1}'.format(database,mystring)	
			
if __name__ == "__main__":
    try:
	main()
    except KeyboardInterrupt:
	print('\n')
#		try:
#sys.exit(0)
#except SystemExit:
#os._exit(0)