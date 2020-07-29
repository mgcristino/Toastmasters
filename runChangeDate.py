#!/usr/bin/python
#
# Change File Date

import argparse
import os.path, time, datetime

dateFormat = "%Y-%m-%d %H:%M:%S"

def is_valid_date(parser, arg):
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
    try:
        return datetime.datetime.strptime(arg, dateFormat)
    except ValueError:
        parser.error("This is the incorrect date string format. It should be YYYY-MM-DD HH:MM:SS")

def is_valid_file(parser, arg):
    """
    Check if arg is a valid date format.

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
    parser.add_argument("-f", "--file",
                        dest="changeFile",
                        type=lambda x: is_valid_file(parser, x),
                        help="File",
                        metavar="FILE",
                        required=True)
    parser.add_argument("-d", "--date",
                        dest="newDate",
                        type=lambda x: is_valid_date(parser, x),
                        help="New Date using format YYYY-MM-DD HH:MM:SS",
                        metavar="Date",
                        required=True)
    return parser

def printf (format,*args):
	sys.stdout.write (format % args)

def fileExists (file_path):
    return os.path.exists(file_path)

def main():
    args = get_parser().parse_args()

    fileName = args.changeFile

    print("Last modified: %s" % time.ctime(os.path.getmtime(fileName)))
    #print("Created: %s" % time.ctime(os.path.getctime(fileName)))

    modTime = time.mktime(args.newDate.timetuple())
    os.utime(fileName, (modTime, modTime))

    print("Last modified: %s" % time.ctime(os.path.getmtime(fileName)))
    #print("Created: %s" % time.ctime(os.path.getctime(fileName)))
			
if __name__ == "__main__":
    try:
	main()
    except KeyboardInterrupt:
	print('\n')        