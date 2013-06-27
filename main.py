#!env python
# created by Albert Zeyer, 2013
# code under 2-clause simplified BSD license

import sys, os
import re

AudioFileExts = ["mp3","wav","flac","ogg","wma"]

# Natural sort
# http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html
def sort_nicely( l ):
	""" Sort the given list in the way that humans expect.
	"""
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )

def m3uFilenameFromDir(path):
	return path + ".m3u"

def createM3U(path):
	m3u_filename = m3uFilenameFromDir(path)
	print("create %s" % m3u_filename)
	entries = []
	for fn in os.listdir(path):
		if os.path.isfile(path + "/" + fn):
			if os.path.splitext(fn)[1][1:].lower() in AudioFileExts:
				entries += [fn]
		elif os.path.isdir(path + "/" + fn):
			if createM3U(path + "/" + fn):
				entries += [m3uFilenameFromDir(path + "/" + fn)]
	if not entries:
		return False
	sort_nicely(entries)
	f = open(m3u_filename, "w")
	for fn in entries:
		f.write("%s\n" % fn)
	return True

def main(*args):
	assert args, "give me some directories"
	for arg in args:
		assert os.path.isdir(arg), "i want directories"
	for arg in args:
		createM3U(arg)

if __name__ == "__main__":
	main(*sys.argv[1:])
