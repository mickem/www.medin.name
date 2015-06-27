#!/bin/python
from os import walk, makedirs, remove
from os.path import isfile, join, exists, abspath
from dateutil.parser import parse
from shutil import move

blog_folder = "content/blog"

files = []
for (dirpath, dirnames, filenames) in walk(blog_folder):
	for f in filenames:
		fpath = join(dirpath, f)
		if isfile(fpath) and f.endswith('.rst'):
			files.append(fpath)
for fpath in files:
	lines = []
	with open(fpath, 'r') as f:
		date = ''
		slug = ''
		cat = ''
		for l in f.readlines():
			if l.startswith(":date: "):
				date =parse(l[7:].strip()).strftime('%Y-%m-%d')
			elif l.startswith(":slug: "):
				slug = l[7:].strip()
			elif l.startswith(":category: "):
				cat = l[11:].strip().lower()
			else:
				lines.append(l)
	if not slug or not cat or not date:
		print "Missing metadatat in %s"%fpath
		continue
	target_path = '%s/%s/%s/%s'%(blog_folder, cat, date, slug)
	target_name = 'post.rst'
	target = join(target_path, target_name)
	if not exists(target_path):
		makedirs(target_path)
	s = abspath(fpath)
	d = abspath(target)
	if s != d:
		print fpath, " -> ", target
		remove(fpath)
		with open(target, 'w') as f:
			print 'Saving: %s'%target
			f.writelines(lines)
	else:
		print "skipping: %s"%fpath
