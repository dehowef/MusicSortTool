#!/usr/bin/env python
#Author: Dehowe Feng
import os
import shutil
import sys
import fnmatch


#Get source and destination from folders.in. Assumes that you're working in the current directory.
#source always comes first, and destination always comes second.
fo = open("folders.in", "rw+")
currentpath = os.path.abspath('.')
srcfolder = currentpath + fo.readline().rstrip()
dstfolder = currentpath + fo.readline().rstrip()


#command line commands
cmd = "open -a iTunes -g "

#macros
BREAKVAL = 80
NOTSYSTEMFILE = "[!.]*"
INDENT = 4
BREAKLINE = str.ljust("",BREAKVAL, '-')
NOMATCH = "File/directory not found!"
EMPTY = "EMPTY".rjust(10," ")
ESCAPECHARS = ["|",  "&",  ";",  "<",  ">",  "(",  ")", "$", "`", "\"", "'", " " ]
QUIT = "-q"
def check_match(matchparam, path):
	#checks for a match in directory, based on number name.
	filenumber = 0
	if os.path.exists(path):

		dirs = fnmatch.filter( os.listdir(path), NOTSYSTEMFILE)
		for file in dirs:
			if matchparam in [file, str(filenumber)]:
				return file

 	  		filenumber += 1


 	if matchparam in QUIT:
 		return QUIT

	return NOMATCH


#prints the directory for navigation
def print_dir(path):

	print ("/" + path[1:70]).center(BREAKVAL,'-')
	filenumber = 0

	if os.path.exists(path):

		dirs = fnmatch.filter( os.listdir(path), NOTSYSTEMFILE)
		for file in dirs:
			filename = (file[:58] + '..') if len(file) > 58 else file
			filepath = os.path.join(path, file)

			if os.path.isdir(filepath):
				ftype = " DIR  "
			else:
				ftype = " FILE "

			line = str(filenumber).rjust(INDENT," ") + ftype + filename.ljust(60, " ")
   			print line
   			filenumber += 1
   	else:
   		print EMPTY
   	print BREAKLINE

#gets the sourcefile path
def get_srcfile(path):
	global filename
	srcempty = 1

	for file in os.listdir(path):
		if not file.startswith('.'):
			srcempty = 0

	if srcempty == 1:
		print path, 'is empty'
		sys.exit("Quitting...")

	print_dir(path)

	userinput = raw_input("Enter your filename or corresponding number or -q to quit: ")
	filename = check_match(userinput,srcfolder)

	if filename in NOMATCH:
		sys.exit("No match found. try again.")

	if filename in QUIT:
		sys.exit("Quitting...")

	srcpath = srcfolder + filename
	return srcpath

#finds where to put the file
def find_dstpath(path):
	dstpath = path
	sentinel = "x"
	while sentinel not in ["y"]:

		print_dir(path)
		userinput = raw_input("Destination: ")
		check = check_match(userinput,path)

		if check in NOMATCH:
			dstpath = os.path.join(dstpath, userinput)
		else:
			filepath = os.path.join(dstpath, check)
			if not os.path.isdir(filepath):
				print check, "is not a directory. try again."
				continue
			else:
				dstpath = filepath
				#print dstpath

		while sentinel not in ["y", "n"]:
			if sentinel in "x":
				sentinel = raw_input("Place " + filename + " here (y) in " + dstpath + ", or go deeper (n)? (y/n)\n")
			elif sentinel not in "x":
				sentinel = raw_input("Please enter a valid result\n")
			if sentinel in "y":
				return dstpath + "/"

			elif sentinel in "n":
				return find_dstpath(dstpath)

	return dstpath

#cleans up the filename of escape characters and whatnot
def clean_filename(filename):
	for ch in ESCAPECHARS:
		if ch in filename:
			filename = filename.replace(ch, "\\"+ ch)

	return filename

#ensures the directory exists
def ensure_dir(path):
 	d = os.path.dirname(path)
	if not os.path.exists(d):
		os.makedirs(d)

#moves the file to the new directory
def move_file(src, dst):
	ensure_dir(dst)
	print "moving",filename, "to", dst
	shutil.move(src, dst + filename)

#adds the file to itunes. can be modified to add to other music players as well.
def open_file(dst):
	f = clean_filename(dst + filename)
	exc = cmd + f
	os.system(exc)


#the main execution of everything
while os.listdir(srcfolder):
	src = get_srcfile(srcfolder)
	dst = find_dstpath(dstfolder)
	move_file(src, dst)
	open_file(dst)
